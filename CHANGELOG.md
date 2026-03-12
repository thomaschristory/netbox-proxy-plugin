# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-03-12

### Changed

- Rewrite README with routing choices, subsystem detection, 4.4 vs 4.5 differences, and dev environment docs
- Expand CHANGELOG with routing, ArrayField filter, and dual compatibility entries
- Fix GUIDELINES project structure and correct PROXY_ROUTERS version reference

## [0.1.0] - 2025-03-12

### Added

- Proxy model with name, protocol (HTTP/HTTPS/SOCKS4/SOCKS5), server, port, and optional credentials
- Routing field (PostgreSQL `ArrayField`) to scope proxies to specific NetBox subsystems
- Routing choices: `webhooks`, `data_backends`, `release_check`, `plugin_catalog`, `dashboard_feed`
- `PluginProxyRouter` for integration with NetBox 4.5+ `PROXY_ROUTERS`
  - Client class inspection to detect the calling subsystem
  - URL heuristic fallback for callers without context (census, release check, plugin catalog)
  - MRO walking for subclass matching
- Web UI for listing, creating, editing, and deleting proxies
- Routing column in proxy list table and routing badges in detail view
- Bulk import, edit, and delete operations
- REST API at `/api/plugins/proxies/proxies/` with routing field support
- Filtering by protocol, routing, server, port, and name
- Custom `filter_routing` method for correct PostgreSQL `ArrayField` filtering
- Navigation menu under "Proxies"
- Tags and custom fields support
- Docker-based development environment (`dev/`)
- Dual compatibility: installs on NetBox 4.4 (UI & API), full routing on 4.5+

[Unreleased]: https://github.com/thomaschristory/netbox-proxy-plugin/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/thomaschristory/netbox-proxy-plugin/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/thomaschristory/netbox-proxy-plugin/releases/tag/v0.1.0
