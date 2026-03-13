# CLAUDE.md

Project reference for AI agents working on this codebase.

## Project

**netbox-proxy-plugin** — A NetBox plugin for managing HTTP proxy configurations via web UI and REST API. On NetBox 4.5+, integrates with `PROXY_ROUTERS` for dynamic proxy resolution. On NetBox 4.4, provides the management UI and API only.

- **Package**: `netbox_proxy_plugin`
- **Version**: defined in both `pyproject.toml` and `netbox_proxy_plugin/__init__.py` (keep in sync)
- **Python**: >=3.10
- **NetBox**: >=4.4.0
- **License**: Apache-2.0
- **Build backend**: Hatchling

## Quick Reference

```
netbox_proxy_plugin/           # Main plugin package
├── __init__.py                # PluginConfig, version
├── models.py                  # Proxy model, ChoiceSets (protocol, routing)
├── views.py                   # Web UI views (list, detail, edit, delete, bulk)
├── forms.py                   # ProxyForm, ProxyImportForm, ProxyFilterForm
├── filtersets.py              # ProxyFilterSet (custom routing filter for ArrayField)
├── tables.py                  # ProxyTable, RoutingColumn
├── urls.py                    # Web UI URL routing
├── navigation.py              # Menu items (under Plugins submenu)
├── proxy_router.py            # PluginProxyRouter for PROXY_ROUTERS integration
├── api/
│   ├── views.py               # ProxyViewSet (REST API)
│   ├── serializers.py         # ProxySerializer
│   └── urls.py                # API route registration
├── migrations/                # Django migrations
└── templates/
    └── netbox_proxy_plugin/
        └── proxy.html         # Detail view template
```

## Development Commands

### Dev environment (Docker)

```bash
./dev/start.sh                                              # Start (NetBox at localhost:8000, admin/admin)
docker compose -f dev/docker-compose.yml down               # Stop
```

### Linting and formatting

```bash
ruff check netbox_proxy_plugin/                             # Lint
ruff format netbox_proxy_plugin/                            # Format
ruff check --fix netbox_proxy_plugin/                       # Lint with auto-fix
```

### Testing

```bash
docker compose -f dev/docker-compose.yml exec netbox \
  python /opt/netbox/netbox/manage.py test netbox_proxy_plugin --keepdb
```

### Building

```bash
uv build                                                    # Build sdist + wheel
```

## Code Conventions

- Follow NetBox base classes: `NetBoxModel`, `NetBoxTable`, `NetBoxModelForm`, `NetBoxModelSerializer`, `NetBoxModelViewSet`, `NetBoxModelFilterSet`.
- Register views with `@register_model_view()`.
- Use `ChoiceSet` for choice fields.
- Ruff config: line-length 120, rules E/F/I/W, target Python 3.10.
- Import order: stdlib → third-party → django → netbox → local.
- Keep it simple. No over-engineering, no speculative features, no dead code.
- Type hints on function signatures where they add clarity. No docstrings on trivial methods.
- The `routing` field is a PostgreSQL `ArrayField` — filtering requires wrapping values in lists (`routing__contains=[value]`).

## Key Design Details

- **Routing choices**: `webhooks`, `data_backends`, `release_check`, `plugin_catalog`, `dashboard_feed`. Empty routing = catch-all proxy.
- **Proxy router** (`proxy_router.py`): detects subsystem via client class inspection (MRO walking) with URL heuristic fallback. Only activates on NetBox 4.5+.
- **Dual compatibility**: plugin UI/API works on 4.4; proxy routing activates on 4.5+ when added to `PROXY_ROUTERS`.

## Git & Release

- Atomic commits, imperative messages, reference issues: `Fix proxy form validation (#12)`.
- Feature branches: `feature/<short-description>` → merge to `main`.
- Release: bump version in `pyproject.toml` + `__init__.py`, tag `v0.1.x`, push tag to trigger PyPI publish.
- See `.github/GUIDELINES.md` for full workflow details.
