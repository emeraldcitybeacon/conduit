# Conduit: OpenReferral HSDS Data Management Platform

[](https://www.google.com/search?q=https://github.com/your-repo/conduit/actions)
[](https://www.google.com/search?q=https://codecov.io/gh/your-repo/conduit)
[](https://opensource.org/licenses/MIT)

Conduit is a Django application for managing and editing human services data that conforms to the **OpenReferral Human Services Data Specification (HSDS)**. It provides a user-friendly, HTMX-powered interface for data managers and a compliant Django Rest Framework (DRF) API for seamless data sharing.

The primary goal of this project is to create a robust, open-source tool that simplifies the management of community resource directories, reduces data silos, and promotes interoperability through a standardized API.

## Core Technologies

  - **Backend**: Django 5.x, Django Rest Framework
  - **Frontend**: HTMX, Alpine.js, Tailwind CSS
  - **Database**: PostgreSQL
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

  - **Web Application**: [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  - **Django Admin**: [http://localhost:8000/admin](https://www.google.com/search?q=http://localhost:8000/admin)
  - **HSDS API Root**: [http://localhost:8000/api/v1/](https://www.google.com/search?q=http://localhost:8000/api/v1/)

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
