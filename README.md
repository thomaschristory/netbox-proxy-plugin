# netbox-proxy-plugin

A [NetBox](https://github.com/netbox-community/netbox) plugin for managing HTTP proxy configurations through the NetBox web interface and REST API.

This plugin integrates with NetBox's [proxy routing system](https://github.com/netbox-community/netbox/pull/18681) (`PROXY_ROUTERS`), allowing you to define and manage proxy configurations from the database instead of static configuration files.

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
| 4.2+           | 0.1.x          |

## Features

- Create, edit, and delete proxy configurations via the NetBox UI
- Support for HTTP, HTTPS, SOCKS4, and SOCKS5 protocols
- REST API for programmatic proxy management
- Bulk import/edit/delete operations
- Filtering and search
- Optional proxy router that resolves proxies from the plugin database
- Tags and custom fields support

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

### Using the Plugin Proxy Router

To have NetBox resolve proxies from the plugin database, add the `PluginProxyRouter` to your `PROXY_ROUTERS` setting in `configuration.py`:

```python
PROXY_ROUTERS = [
    "netbox_proxy_plugin.proxy_router.PluginProxyRouter",
    "utilities.proxy.DefaultProxyRouter",
]
```

The plugin router is listed first so it takes priority. If no matching proxy is found in the database, the default router falls back to the `HTTP_PROXIES` static configuration.

### How Proxy Routing Works

NetBox's proxy routing system (introduced in [PR #18681](https://github.com/netbox-community/netbox/pull/18681)) calls `resolve_proxies()` whenever an outbound HTTP request needs proxy configuration. Each router in `PROXY_ROUTERS` is tried in order. The first router to return a non-empty result wins.

The `PluginProxyRouter` queries the plugin's `Proxy` model and returns matching entries as a dictionary:

```python
{"http": "http://proxy.example.com:8080", "https": "https://proxy.example.com:8443"}
```

## Usage

### Web Interface

After installation, a **Proxies** menu appears in the NetBox navigation. From there you can:

- **List** all configured proxies
- **Add** a new proxy with protocol, server, port, and optional credentials
- **Edit** or **delete** existing proxies
- **Bulk import** proxies from CSV
- **Filter** by protocol, server, or name

### REST API

The plugin exposes a REST API at `/api/plugins/proxies/proxies/`.

**List proxies:**
```bash
curl -H "Authorization: Token <your-token>" \
  http://netbox.example.com/api/plugins/proxies/proxies/
```

**Create a proxy:**
```bash
curl -X POST \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "corp-proxy", "protocol": "http", "server": "proxy.corp.com", "port": 8080}' \
  http://netbox.example.com/api/plugins/proxies/proxies/
```

## Model Reference

### Proxy

| Field       | Type    | Required | Description                          |
|-------------|---------|----------|--------------------------------------|
| name        | string  | Yes      | Unique name for the proxy            |
| protocol    | choice  | Yes      | `http`, `https`, `socks4`, `socks5`  |
| server      | string  | Yes      | Proxy server address                 |
| port        | integer | Yes      | Proxy server port                    |
| username    | string  | No       | Authentication username              |
| password    | string  | No       | Authentication password              |
| description | string  | No       | Optional description                 |

## License

Apache License 2.0. See [LICENSE](LICENSE).
