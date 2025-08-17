# Conduit — LLM Agent Guide

These instructions are for **LLM agents** assisting on this Django project focused on the **Pulse volunteer resource editor**.

## 1. Project Context & Role

  - **Project**: Django + HTMX + DRF app for managing OpenReferral HSDS data with **Pulse** volunteer resource editor.
  - **Current Phase**: Pulse development and refinement - unified resource editing interface with extension models.
  - **Role**: Act as a **senior Django engineer** familiar with modern Python patterns, DRF, HTMX, and component-based UI.
  - **Focus**: Pulse volunteer resource editor that enables rapid creation, validation, and maintenance of HSDS data.
  - **Tone**: Concise, actionable guidance; cite official docs when helpful.

## 2. Development Environment

### Prerequisites

  - Docker & Docker Compose
  - Python 3.11+ (as defined in the container)
  - 4GB+ RAM, 2GB+ disk space

### Quick Start Commands

```bash
# Setup from project root
cp .env.example .env
docker-compose up -d --build

# Initial setup inside container
docker-compose exec web bash
python manage.py migrate
python manage.py createsuperuser
```

### Key URLs

  - **Pulse Editor**: [http://localhost:8000/pulse](https://www.google.com/search?q=http://localhost:8000/pulse)
  - App: [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  - Admin: [http://localhost:8000/admin](https://www.google.com/search?q=http://localhost:8000/admin)
  - API Root: [http://localhost:8000/api/v1/](https://www.google.com/search?q=http://localhost:8000/api/v1/)
  - **Resource Façade API**: [http://localhost:8000/api/resource/{id}](https://www.google.com/search?q=http://localhost:8000/api/resource/{id})

## 3. Workflow Expectations

1.  **Follow the Pulse Specification**: Work within the scope of the Pulse volunteer resource editor (`docs/plans/pulse/pulse-technical-specification.md`).
2.  **Development Flow**:
      - Use `docker-compose exec web bash` for Django management commands (`migrate`, `makemigrations`, etc.).
      - Run `pytest` to ensure all tests pass before finalizing changes.
      - Check `docker-compose logs -f web` for debugging server-side issues.
      - Test Pulse features through the unified resource editor interface.
3.  **Code Changes**:
      - Provide complete, ready-to-use code snippets.
      - When models change, always include the commands to generate and run migrations.
      - Write tests for new business logic and API endpoints.
      - Follow conventional commit message standards (`feat:`, `fix:`, `docs:`, etc.).
      - Maintain separation between HSDS core tables and `hsds_ext_*` extension tables.

## 4. Technical Standards

| Topic | Standard |
|---|---|
| Python | 3.11+, type hints where appropriate. |
| Dependencies | Managed via `pyproject.toml` and `uv`. |
| Testing | `pytest-django` for backend testing, Playwright for E2E. |
| API | Django Rest Framework + Resource Façade pattern for composite HSDS JSON. |
| Frontend | HTMX for server-rendered partials, Alpine.js for light interactivity, Tailwind CSS v4 + daisyUI v5. |
| Database | PostgreSQL 15+ with `pg_trgm` extension, HSDS core tables + `hsds_ext_*` extensions. |
| Commits | Conventional (`feat:`, `fix:`, `docs:`, etc.). |

## 5. Core Models & Logic

### Schema Source of Truth

  - **HSDS Core**: The primary reference for database models is `openreferral/database/database_postgresql.sql` and `openreferral/schema_reference.md`.
  - **Pulse Extensions**: All extension tables are namespaced `hsds_ext_*` and defined in `src/hsds_ext/models/`.
  - **Primary Keys**: All primary keys **must** be `UUIDField`.
  - **No HSDS Modifications**: HSDS core tables are never modified directly.

### Extension Models (hsds_ext)

  - **Verification Events**: Track field-level verification with method, timestamp, and user.
  - **Field Versions**: Maintain version numbers for field-level change tracking.
  - **Sensitive Overlays**: Apply read-time redaction rules for protected data.
  - **Draft Resources**: Store composite HSDS data pending editor approval.
  - **Change Requests**: RFC6902 JSON Patch operations requiring review.
  - **Shelves & Bulk Operations**: Group resources for batch updates with preview/undo.

### Admin Interface

  - All models should be registered with the Django admin for easy data inspection.

### Accounts & Auth Flow

  - The system uses a custom `User` model (`src.users.User`) with a `role` field (`Administrator`, `Editor`, `Volunteer`).
  - Authorization logic in views should respect these roles, especially for auto-publish vs review-required fields.

## 6. Frontend Workflow

  - **Django Components**: We use `django-components` extensively. Components go in `src/[app_name]/components/[component_name].{py,html}`. Pulse has many reusable components for forms, modals, badges, etc.
  - **Tailwind CSS v4 + daisyUI v5**: Use `npm run watch` for CSS compilation. Follow daisyUI component patterns (`navbar`, `modal`, `tabs`, `input`, `badge`, etc.).
  - **HTMX**: All dynamic updates via HTMX attributes (`hx-get`, `hx-post`, `hx-trigger`). Pulse uses server-rendered partials extensively.
  - **Alpine.js**: Use for small, localized UI (dropdowns, modals, client-side validation). Directives: `x-data`, `x-show`, `@click`. See `docs/frameworks/alpine-js.md`.
  - **Resource Façade Pattern**: Unified editor that aggregates Org ⇄ Location ⇄ Service data with ETags, field versions, and freshness indicators.

### Key Pulse Components

  - **Resource Editor**: Tabbed interface with real-time validation (`src/pulse/templates/pulse/resource/`)
  - **Create Wizard**: 3-step resource creation with sibling prefill
  - **Shelf Drawer**: Right-hand panel for bulk operations
  - **Freshness Badges**: Field-level verification indicators
  - **Diff Previews**: Before/after comparisons for changes
  - **Merge Interface**: Split-view for duplicate resolution

## 7. Testing Strategy

```bash
# Run the full test suite from within the container
pytest

# Run tests for specific Pulse features
pytest src/pulse/
pytest src/hsds_ext/

# Run tests with coverage report
pytest --cov=src --cov-report=html

# End-to-end Playwright tests for Pulse workflows
pytest e2e/pulse/
```

### Key Points

  - New Pulse features require corresponding tests (unit, integration, E2E).
  - API tests should validate Resource Façade responses, ETags, field versions.
  - Model tests should validate extension models (verification events, field versions, etc.).
  - E2E tests should cover core Pulse workflows (resource editing, wizard, bulk operations).

### Pulse-Specific Testing Focus

  - **Resource Façade**: Composite HSDS JSON + overlays + ETags mapping
  - **Change Tracking**: Field version increments and verification events
  - **Bulk Operations**: Staging, preview, commit, and undo workflows
  - **Draft Approval**: Volunteer submissions → editor approval → HSDS writes
  - **Sensitive Overlays**: Read-time redaction based on visibility rules

## 8. Common References

  - **Pulse Technical Specification**: [docs/plans/pulse/pulse-technical-specification.md](https://www.google.com/search?q=docs/plans/pulse/pulse-technical-specification.md) - Authoritative guide for Pulse architecture and features.
  - **HSDS API Reference**: [docs/openreferral/api\_reference.md](https://www.google.com/search?q=docs/openreferral/api_reference.md)
  - **HSDS Schema Reference**: [docs/openreferral/schema\_reference.md](https://www.google.com/search?q=docs/openreferral/schema_reference.md)
  - **Framework Documentation**:
    - Django 5.0: [https://docs.djangoproject.com/en/5.0/](https://docs.djangoproject.com/en/5.0/)
    - Django Rest Framework: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
    - HTMX: [https://htmx.org/](https://htmx.org/)
    - daisyUI v5: [https://daisyui.com/](https://daisyui.com/)
    - Tailwind CSS v4: [https://tailwindcss.com/](https://tailwindcss.com/)

## 9. Troubleshooting

### Common Commands

```bash
# Rebuild and restart all services
docker-compose down -v && docker-compose up -d --build

# Access the running web container shell
docker-compose exec web bash

# View real-time logs for the web service
docker-compose logs -f web

# Run database migrations
docker-compose exec web python manage.py migrate
```

## 10. Next Actions

Before implementing a Pulse feature, verify:

1.  Does the change align with the Pulse technical specification?
2.  Are new dependencies added to `pyproject.toml`?
3.  Are tests included for any new logic (especially extension models)?
4.  Are new environment variables documented in `.env.example`?
5.  Does the feature maintain separation between HSDS core and extension tables?
6.  Are daisyUI components used appropriately for UI consistency?

### Key Pulse Development Guidelines

- **Resource Façade Pattern**: Always use composite HSDS JSON with overlays for the unified editor.
- **Field-Level Tracking**: Implement version increments and verification events for all field changes.
- **Review Workflows**: Distinguish between auto-publish (volunteers) and review-required (sensitive) fields.
- **Extension Models**: Use `hsds_ext_*` tables for all new functionality without modifying HSDS core.
- **Component-Based UI**: Leverage existing Pulse components and follow daisyUI patterns.

When in doubt, refer to the Pulse technical specification or ask for clarification.

-----

*This guide reflects the current Pulse volunteer resource editor implementation. Update when project conventions or requirements change.*
