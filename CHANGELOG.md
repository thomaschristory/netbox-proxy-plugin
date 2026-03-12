# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-03-12

### Added

- Proxy model with name, protocol (HTTP/HTTPS/SOCKS4/SOCKS5), server, port, and optional credentials
- Web UI for listing, creating, editing, and deleting proxies
- Bulk import, edit, and delete operations
- REST API at `/api/plugins/proxies/proxies/`
- Filtering by protocol, server, port, and name
- `PluginProxyRouter` for integration with NetBox's `PROXY_ROUTERS`
- Navigation menu under "Proxies > Proxy Management"
- Tags and custom fields support

[Unreleased]: https://github.com/thomaschristory/netbox-proxy-plugin/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/thomaschristory/netbox-proxy-plugin/releases/tag/v0.1.0
