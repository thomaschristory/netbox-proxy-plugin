# netbox-proxy-plugin

[![CI](https://github.com/thomaschristory/netbox-proxy-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/thomaschristory/netbox-proxy-plugin/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/netbox-proxy-plugin)](https://pypi.org/project/netbox-proxy-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netbox-proxy-plugin)](https://pypi.org/project/netbox-proxy-plugin/)
[![License](https://img.shields.io/github/license/thomaschristory/netbox-proxy-plugin)](https://github.com/thomaschristory/netbox-proxy-plugin/blob/main/LICENSE)

A [NetBox](https://github.com/netbox-community/netbox) plugin for managing HTTP proxy configurations through the NetBox web interface and REST API.

On NetBox 4.5+, the plugin integrates with NetBox's [proxy routing system](https://github.com/netbox-community/netbox/pull/18681) (`PROXY_ROUTERS`), allowing you to define and manage proxy configurations from the database instead of static configuration files. On NetBox 4.4, the plugin provides the management UI and API but proxy routing is not available (4.4 only supports the static `HTTP_PROXIES` setting).

## Compatibility

| NetBox Version | Plugin Version | Proxy Routing |
|----------------|----------------|---------------|
| 4.4.x          | 0.1.x          | UI & API only |
| 4.5+           | 0.1.x          | Full routing  |

## Features

- Create, edit, and delete proxy configurations via the NetBox UI
- Support for HTTP, HTTPS, SOCKS4, and SOCKS5 protocols
- **Routing scoping** — assign proxies to specific NetBox subsystems (webhooks, data backends, etc.) or leave empty for a catch-all proxy
- Proxy router for NetBox 4.5+ `PROXY_ROUTERS` integration
- REST API for programmatic proxy management
- Bulk import/edit/delete operations
- Filtering by protocol, routing, server, and name
- Tags and custom fields support

## Requirements

- NetBox 4.4 or later
- Python 3.10 or later
- PostgreSQL (required by NetBox; the routing field uses PostgreSQL `ArrayField`)

## Installation

### 1. Install the package

```bash
pip install netbox-proxy-plugin
```

Or for development:

```bash
cd netbox-proxy-plugin
pip install -e .
```

### 2. Enable the plugin

Add to your NetBox `configuration.py`:

```python
PLUGINS = [
    "netbox_proxy_plugin",
]
```

### 3. Run migrations

```bash
cd /opt/netbox/netbox
python manage.py migrate
```

### 4. Restart NetBox

```bash
sudo systemctl restart netbox netbox-rq
```

## Configuration

### Enabling Proxy Routing (NetBox 4.5+)

NetBox 4.5 introduced the `PROXY_ROUTERS` setting, which lets plugins provide proxy configurations dynamically. To enable routing from the plugin database, add the `PluginProxyRouter` to your `configuration.py`:

```python
PROXY_ROUTERS = [
    "netbox_proxy_plugin.proxy_router.PluginProxyRouter",
    "utilities.proxy.DefaultProxyRouter",
]
```

The plugin router is listed first so it takes priority. If no matching proxy is found in the plugin database, the default router falls back to the static `HTTP_PROXIES` configuration.

> **NetBox 4.4 note:** The `PROXY_ROUTERS` setting does not exist in NetBox 4.4. The plugin installs and works on 4.4 (you can manage proxies through the UI and API), but the proxy routing integration is only active on 4.5+.

### How Proxy Routing Works

NetBox 4.5's `resolve_proxies()` function is called whenever NetBox makes an outbound HTTP request that may need proxy configuration. It iterates over each router in `PROXY_ROUTERS` and returns the first non-empty result.

The `PluginProxyRouter` receives three arguments:

| Argument   | Description |
|------------|-------------|
| `url`      | The target URL for the outbound request |
| `protocol` | The protocol to use (or `None` to auto-detect from the URL) |
| `context`  | A dict with caller metadata; typically `{"client": <calling_object>}` |

The router:

1. **Detects the protocol** from the URL if not explicitly provided.
2. **Identifies the subsystem** making the request (see [Routing Choices](#routing-choices) below).
3. **Queries the database** for proxies matching the protocol. If a subsystem was identified, results are narrowed to proxies whose `routing` field includes that subsystem *or* whose `routing` is empty (catch-all).
4. **Returns a dict** mapping protocols to proxy URLs, e.g. `{"https": "https://proxy:8443"}`, or `None` if no proxies match.

### Subsystem Detection

The router identifies the calling subsystem in two ways:

1. **Client class inspection** (primary) — NetBox 4.5 passes the calling object as `context["client"]`. The router maps the object's class to a routing tag:

   | Client class | Routing tag |
   |-------------|-------------|
   | `extras.models.webhooks.Webhook` | `webhooks` |
   | `core.data_backends.GitBackend` | `data_backends` |
   | `core.data_backends.S3Backend` | `data_backends` |
   | `core.data_backends.LocalBackend` | `data_backends` |
   | `extras.dashboard.widgets.RSSFeedWidget` | `dashboard_feed` |

   The router also walks the MRO, so subclasses of these backends are matched automatically.

2. **URL heuristic** (fallback) — Some callers (census, release check, plugin catalog) don't pass a `context`. For these, the router matches based on the target URL:
   - URLs containing `github` → `release_check`
   - URLs containing `plugin` or `catalog` → `plugin_catalog`

### Routing Choices

Each proxy can be scoped to one or more NetBox subsystems via the `routing` field. Available choices:

| Value | Label | Description |
|-------|-------|-------------|
| `webhooks` | Webhooks | Outbound webhook HTTP requests |
| `data_backends` | Data Backends | Git, S3, and HTTP data source sync |
| `release_check` | Release Check | NetBox version check against GitHub |
| `plugin_catalog` | Plugin Catalog | Plugin catalog queries |
| `dashboard_feed` | Dashboard Feed | RSS feed widget on the dashboard |

When `routing` is **empty** (the default), the proxy acts as a catch-all and is considered for all subsystems.

When `routing` contains one or more values, the proxy is only used for those specific subsystems. This lets you route different traffic through different proxies — for example, sending webhooks through a dedicated egress proxy while using a general proxy for everything else.

## Usage

### Web Interface

After installation, a **Proxies** menu appears in the NetBox navigation. From there you can:

- **List** all configured proxies with protocol, server, port, and routing columns
- **Add** a new proxy with protocol, server, port, optional credentials, and routing scope
- **Edit** or **delete** existing proxies
- **Bulk import** proxies from CSV
- **Filter** by protocol, routing, server, or name

### REST API

The plugin exposes a REST API at `/api/plugins/proxies/proxies/`.

**List proxies:**

```bash
curl -H "Authorization: Token <your-token>" \
  http://netbox.example.com/api/plugins/proxies/proxies/
```

**Create a proxy (catch-all):**

```bash
curl -X POST \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "general-proxy",
    "protocol": "http",
    "server": "proxy.corp.com",
    "port": 8080
  }' \
  http://netbox.example.com/api/plugins/proxies/proxies/
```

**Create a proxy scoped to webhooks and data backends:**

```bash
curl -X POST \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "egress-proxy",
    "protocol": "https",
    "server": "egress.corp.com",
    "port": 8443,
    "routing": ["webhooks", "data_backends"]
  }' \
  http://netbox.example.com/api/plugins/proxies/proxies/
```

**Filter proxies by routing:**

```bash
curl -H "Authorization: Token <your-token>" \
  "http://netbox.example.com/api/plugins/proxies/proxies/?routing=webhooks"
```

## Model Reference

### Proxy

| Field       | Type        | Required | Description |
|-------------|-------------|----------|-------------|
| name        | string      | Yes      | Unique name for the proxy |
| protocol    | choice      | Yes      | `http`, `https`, `socks4`, `socks5` |
| server      | string      | Yes      | Proxy server address (e.g. `proxy.example.com`) |
| port        | integer     | Yes      | Proxy server port |
| username    | string      | No       | Authentication username |
| password    | string      | No       | Authentication password |
| routing     | string[]    | No       | Subsystems this proxy serves; empty = all. Values: `webhooks`, `data_backends`, `release_check`, `plugin_catalog`, `dashboard_feed` |
| description | string      | No       | Optional description |
| tags        | tag[]       | No       | NetBox tags |

The proxy URL is constructed automatically from the fields: `{protocol}://{username}:{password}@{server}:{port}` (credentials are included only when `username` is set).

## Development

### Dev Environment

A Docker-based development environment is provided in the `dev/` directory:

```bash
# Start NetBox with the plugin loaded
./dev/start.sh

# NetBox will be available at http://localhost:8000
# Login: admin / admin

# Follow logs
docker compose -f dev/docker-compose.yml logs -f netbox

# Stop
docker compose -f dev/docker-compose.yml down
```

The `start.sh` script copies the plugin source into the Docker build context and builds a custom NetBox image with the plugin installed.

### Running Tests

Tests run inside the Docker container using NetBox's test runner:

```bash
docker compose -f dev/docker-compose.yml exec netbox \
  python /opt/netbox/netbox/manage.py test netbox_proxy_plugin --keepdb
```

### Code Style

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting:

```bash
pip install ruff
ruff check netbox_proxy_plugin/
ruff format netbox_proxy_plugin/
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
