# Development Guidelines

Guidelines for AI agents and contributors working on this project.

## Project Overview

**netbox-proxy-plugin** is a NetBox plugin that provides a web UI and REST API for managing HTTP proxy configurations. On NetBox 4.5+, the plugin integrates with NetBox's `PROXY_ROUTERS` system to dynamically resolve proxies from the database. On NetBox 4.4, the plugin provides the management UI and API only (4.4 does not have `PROXY_ROUTERS`).

- **Target compatibility**: NetBox 4.4, 4.5, and newer
- **Python package name**: `netbox_proxy_plugin`
- **Repository**: `thomaschristory/netbox-proxy-plugin`

## Code Principles

1. **Keep it simple.** No over-engineering. If three lines of code work, don't create an abstraction.
2. **Follow NetBox conventions.** Use NetBox's base classes (`NetBoxModel`, `NetBoxTable`, `NetBoxModelForm`, `NetBoxModelSerializer`, `NetBoxModelViewSet`, `NetBoxModelFilterSet`). Don't reinvent what the framework provides.
3. **Minimal changes.** Only add what is needed. No speculative features, no unused code, no dead comments.
4. **No AI artifacts in the repo.** Do not commit `.mcp.json`, AI conversation logs, prompt files, or any AI-related configuration. These must be in `.gitignore`.

## Git Workflow

### Atomic Commits

- Each commit should represent **one logical change** (e.g., "Add Proxy model", "Add proxy list view").
- Do not bundle unrelated changes in a single commit.
- Write clear, imperative commit messages: `Add proxy model with protocol and URL fields`.

### Branch Strategy

- `main` is the default branch. All work targets `main`.
- Use feature branches for non-trivial work: `feature/<short-description>`.
- Keep commits on feature branches atomic as well.

### GitHub Issues

- **Create GitHub issues for bugs and tasks** encountered during development.
- Reference issue numbers in commit messages when applicable: `Fix proxy form validation (#12)`.
- Use issues to track work across multiple sessions or agents.

## Project Structure

```
netbox-proxy-plugin/           # Repository root
├── .github/
│   └── GUIDELINES.md          # This file
├── dev/                       # Docker-based dev environment
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── start.sh
├── netbox_proxy_plugin/       # Python package
│   ├── api/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   │   └── ...
│   ├── templates/
│   │   └── netbox_proxy_plugin/
│   │       └── proxy.html     # Detail view template
│   ├── __init__.py            # PluginConfig
│   ├── filtersets.py
│   ├── forms.py
│   ├── models.py              # Proxy model, ChoiceSets
│   ├── navigation.py
│   ├── proxy_router.py        # PluginProxyRouter (PROXY_ROUTERS)
│   ├── tables.py
│   ├── urls.py
│   └── views.py
├── .gitignore
├── pyproject.toml
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Coding Standards

### Python

- Follow PEP 8.
- Use type hints only where they add clarity (function signatures). Don't annotate everything.
- No docstrings on trivial methods. Only add comments where logic isn't self-evident.
- Import order: stdlib, third-party, django, netbox, local.

### Models

- Inherit from `NetBoxModel` (or appropriate subclass like `PrimaryModel`).
- Use `ChoiceSet` for choice fields.
- Keep model names in CapWords without underscores.

### Views

- Use NetBox generic views: `ObjectView`, `ObjectListView`, `ObjectEditView`, `ObjectDeleteView`, `BulkImportView`, `BulkEditView`, `BulkDeleteView`.
- Register views with `@register_model_view()`.

### Templates

- Extend NetBox's base templates (`generic/object.html`, `generic/object_list.html`, etc.).
- Only create custom templates when the generic ones are insufficient.

### API

- Use `NetBoxModelSerializer` and `NetBoxModelViewSet`.
- Use `NetBoxRouter` for URL routing.

### Forms

- Use `NetBoxModelForm` for create/edit forms.
- Use `NetBoxModelFilterSetForm` for filter forms.
- Use `NetBoxModelImportForm` for CSV import.

### Tables

- Use `NetBoxTable` as the base class.
- Define `fields` and `default_columns` in Meta.

## Testing

- Tests go in `netbox_proxy_plugin/tests/`.
- Test models, views, API endpoints, and the proxy router.
- Run tests with the NetBox test runner.

## What NOT to Commit

These must be in `.gitignore`:

- `.mcp.json` and any MCP configuration
- AI conversation logs or prompt files
- `__pycache__/`, `*.pyc`
- `.eggs/`, `*.egg-info/`, `dist/`, `build/`
- Virtual environments (`venv/`, `.venv/`, `env/`)
- IDE files (`.idea/`, `.vscode/`, `.fleet/`)
- OS files (`.DS_Store`, `Thumbs.db`)

## Change Workflow

Every non-trivial change follows this process:

1. **Issue** — Create a GitHub issue describing the problem or feature.
2. **Code** — Implement the fix or feature, referencing the issue number.
3. **Test** — Verify the change works (Docker dev environment, API tests).
4. **Push** — Commit with a message referencing the issue: `Fix navigation nesting (#8)`.
5. **Tag** — Bump version, create an annotated tag: `git tag -a v0.1.2 -m "v0.1.2"`.
6. **Release** — Push the tag: `git push origin main --tags`.

Trivial fixes (typos, formatting) can skip the issue step.

## Release Process

- Version is defined in `pyproject.toml` and `netbox_proxy_plugin/__init__.py`.
- Tag releases with `v` prefix: `v0.1.0`.
- Follow semantic versioning.
