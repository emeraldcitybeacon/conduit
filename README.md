# Conduit: OpenReferral HSDS Data Management Platform with Pulse

[](https://www.google.com/search?q=https://github.com/your-repo/conduit/actions)
[](https://www.google.com/search?q=https://codecov.io/gh/your-repo/conduit)
[](https://opensource.org/licenses/MIT)

Conduit is a Django application for managing and editing human services data that conforms to the **OpenReferral Human Services Data Specification (HSDS)**. It features **Pulse**, a volunteer resource editor that enables rapid creation, validation, and maintenance of hyper-local HSDS data through a unified "Resource" editor interface.

## Key Features

- **Unified Resource Editor**: Stitched Organization ⇄ Location ⇄ Service editor with real-time validation
- **Create Wizard**: 3-step resource creation with sibling prefill and draft approval workflow
- **Shelf & Bulk Operations**: Queue resources, stage changes, preview diffs, commit with undo capability
- **Field-Level History**: Track verification events, freshness indicators, and field versioning
- **Dedupe & Merge**: Live duplicate detection with split-view merging
- **Sensitive Mode**: Read-time redaction overlay for addresses and contacts
- **Review Queue**: Editor approval workflow for volunteer submissions

The primary goal is to enable volunteers and editors to rapidly maintain community resource directories while preserving HSDS compliance and data integrity.

## Core Technologies

  - **Backend**: Django 5.x, Django Rest Framework
  - **Frontend**: HTMX, Alpine.js, Tailwind CSS v4, daisyUI v5
  - **Database**: PostgreSQL 15+ with pg_trgm extension for fuzzy search
  - **DevOps**: Docker, Docker Compose

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

  - Docker
  - Docker Compose

### Local Development Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-repo/conduit.git
    cd conduit
    ```

2.  **Configure Environment Variables:**
    Copy the example environment file. The default values are suitable for local development.

    ```bash
    cp .env.example .env
    ```

3.  **Build and Run the Docker Containers:**
    This command will build the Django image, start the web and database containers, and run the application.

    ```bash
    docker-compose up -d --build
    ```

4.  **Run Database Migrations:**
    Apply the initial database schema.

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a Superuser:**
    Create an administrator account to log into the Django admin and the management interface.

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

### Accessing the Application

Once the setup is complete, you can access the following URLs:

  - **Pulse Resource Editor**: [http://localhost:8000/pulse](https://www.google.com/search?q=http://localhost:8000/pulse)
  - **Web Application**: [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  - **Django Admin**: [http://localhost:8000/admin](https://www.google.com/search?q=http://localhost:8000/admin)
  - **HSDS API Root**: [http://localhost:8000/api/v1/](https://www.google.com/search?q=http://localhost:8000/api/v1/)

## Application Structure

### Core Apps

- **`hsds/`**: OpenReferral HSDS core models and API endpoints
- **`pulse/`**: Volunteer resource editor with unified interface
- **`hsds_ext/`**: Extension models for drafts, change requests, field versions, verification events, shelves, and sensitive overlays
- **`resources/`**: Additional resource management utilities
- **`users/`**: User management with role-based permissions (Volunteer, Editor, Admin)

### Key Pulse Features

- **Resource Façade API**: Composite HSDS JSON + overlays + ETags + field freshness
- **Change Tracking**: Field-level versioning with verification events and audit trail
- **Bulk Operations**: Stage patches across multiple resources with preview and undo
- **Draft Workflow**: Volunteer submissions require editor approval before writing to HSDS
- **Sensitive Data**: Read-time redaction overlay for protected information

## Running Tests

To run the test suite, execute the following command from your host machine:

```bash
docker-compose exec web pytest
```

To generate a coverage report:

```bash
docker-compose exec web pytest --cov=apps --cov-report=html
```

The report will be available in the `htmlcov/` directory.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details.
