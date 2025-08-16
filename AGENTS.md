# Conduit — LLM Agent Guide

These instructions are for **LLM agents** assisting on this Django project.

## 1. Project Context & Role

  - **Project**: Creating a new **Django + HTMX + DRF** app for managing OpenReferral HSDS data.
  - **Current Phase**: Initial setup and development.
  - **Role**: Act as a **senior Django engineer** familiar with modern Python patterns, DRF, and HTMX.
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

  - App: [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  - Admin: [http://localhost:8000/admin](https://www.google.com/search?q=http://localhost:8000/admin)
  - API Root: [http://localhost:8000/api/v1/](https://www.google.com/search?q=http://localhost:8000/api/v1/)

## 3. Workflow Expectations

1.  **Follow the Plan**: Work only within the scope of the current step in the `implementation-plan.md`. Do not work ahead.
2.  **Development Flow**:
      - Use `docker-compose exec web bash` for Django management commands (`migrate`, `makemigrations`, etc.).
      - Run `pytest` to ensure all tests pass before finalizing changes.
      - Check `docker-compose logs -f web` for debugging server-side issues.
3.  **Code Changes**:
      - Provide complete, ready-to-use code snippets.
      - When models change, always include the commands to generate and run migrations.
      - Write tests for new business logic and API endpoints.
      - Follow conventional commit message standards (`feat:`, `fix:`, `docs:`, etc.).

## 4. Technical Standards

| Topic | Standard |
|---|---|
| Python | 3.11+, type hints where appropriate. |
| Dependencies | Managed via `pyproject.toml` and `poetry`. |
| Testing | `pytest-django` for backend testing. |
| API | Django Rest Framework, adhering to `openreferral/schema/openapi.json`. |
| Frontend | HTMX for server-rendered partials, Alpine.js for light interactivity. |
| Styling | Tailwind CSS. |
| Commits | Conventional (`feat:`, `fix:`, `docs:`, etc.). |

## 5. Core Models & Logic

### Schema Source of Truth

  - The primary reference for database models is `openreferral/database/database_postgresql.sql`.
  - The `openreferral/schema_reference.md` provides detailed field definitions.
  - All primary keys **must** be `UUIDField`.

### Admin Interface

  - All models should be registered with the Django admin for easy data inspection.

### Accounts & Auth Flow

  - The system uses a custom `User` model (`apps.users.User`) with a `role` field (`Administrator`, `Editor`, `Viewer`).
  - Authorization logic in views should respect these roles.

## 6. Frontend Workflow

  - **Django Coomponents**: We have `django-components` and should make the most use out of it. Components go in `src/[app name]/components/[component name].{py,html}`. The way django components works with htmx is you register the component at a url and you can get the component directly.
  - **Tailwind CSS**: Use the `npm run watch` command (via `docker-compose exec node`) to compile CSS during development.
  - **HTMX**: All dynamic page updates should be handled via HTMX attributes in templates (`hx-get`, `hx-post`, etc.).
  - **Alpine.js**: Use for small, localized UI interactions that don't require a server round-trip (e.g., toggling a dropdown, managing modal visibility). Use the `x-data`, `x-show`, and `@click` directives. See `docs/frameworks/alpine-js.md`.
  - **Daisy UI**: Our primary component library. Use pre-built components whenever possible. See `docs/frameworks/daisyui.md`.

## 7. Testing Strategy

```bash
# Run the full test suite from within the container
pytest

# Run tests for a specific app
pytest apps/hsds/

# Run tests with coverage report
pytest --cov=apps --cov-report=html
```

### Key Points

  - New features require corresponding tests.
  - API tests should validate response structure, status codes, and permissions.
  - Model tests should validate custom methods and validation logic.

## 8. Common References

  - **Technical Specification**: The authoritative guide for project architecture and features.
  - **Implementation Plan**: The step-by-step development sequence.
  - **HSDS API Reference**: [docs/openreferral/api\_reference.md](https://www.google.com/search?q=docs/openreferral/api_reference.md)
  - **HSDS Schema Reference**: [docs/openreferral/schema\_reference.md](https://www.google.com/search?q=docs/openreferral/schema_reference.md)
  - **Django 5.0 Docs**: [https://docs.djangoproject.com/en/5.0/](https://docs.djangoproject.com/en/5.0/)
  - **Django Rest Framework**: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
  - **HTMX**: [https://htmx.org/](https://htmx.org/)

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

Before implementing a feature, verify:

1.  Does the change align with the current step in the implementation plan?
2.  Are new dependencies added to `pyproject.toml`?
3.  Are tests included for any new logic?
4.  Are new environment variables documented in `.env.example`?

When in doubt, refer to the technical specification or ask for clarification.

-----

*Update this guide when project conventions or requirements change.*
