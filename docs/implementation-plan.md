# Conduit: OpenReferral HSDS Django Data Management Platform Implementation Plan

This implementation plan provides a step-by-step guide to building the Conduit application. The plan is structured to build the application from the core backend components outwards to the user-facing frontend, ensuring a stable foundation at each stage.

## 1. Project Setup & Foundation

  - [x] Step 1: Initialize Django Project and Dependencies

      - **Task**: Create the basic Django project structure, initialize uv for dependency management, and install core libraries like Django, Psycopg2, and Django REST Framework.
      - **Files**:
          - `pyproject.toml`: Define project metadata and dependencies (Django, djangorestframework, psycopg2-binary, python-dotenv, gunicorn).
          - `README.md`: Basic project description.
          - `manage.py`: Standard Django management script.
          - `conduit/settings.py`: Initial settings configuration.
          - `conduit/urls.py`: Root URL configuration.
          - `.gitignore`: Standard Python/Django gitignore.
      - **Step Dependencies**: None.
      - **User Instructions**: Run `uv install` to create the virtual environment and install dependencies.

  - [x] Step 2: Dockerize the Development Environment

      - **Task**: Create `Dockerfile` and `docker-compose.yml` to set up a containerized development environment with a Django service and a PostgreSQL database service. This ensures consistency for all developers.
      - **Files**:
          - `Dockerfile`: Defines the image for the Django application.
          - `docker-compose.yml`: Orchestrates the `web` and `db` services.
          - `.dockerignore`: Exclude unnecessary files from the Docker build context.
          - `.env.example`: Provide a template for required environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`).
          - `conduit/settings.py`: Update to use `python-dotenv` to load settings from the environment.
      - **Step Dependencies**: Step 1.
      - **User Instructions**: Create a `.env` file from the example and run `docker-compose up --build` to start the development environment.

## 2. User Management

  - [x] Step 3: Implement Custom User Model and Roles
      - **Task**: Create a new `users` app and implement a custom `User` model that inherits from `AbstractUser`. Add a `role` field with choices for "Administrator", "Editor", and "Viewer".
      - **Files**:
          - `apps/users/models.py`: Define the `User` model with the `role` field.
          - `apps/users/admin.py`: Register the custom `User` model with the Django admin.
          - `conduit/settings.py`: Set `AUTH_USER_MODEL = 'users.User'`.
          - `apps/users/apps.py`: Standard app configuration.
      - **Step Dependencies**: Step 2.
      - **User Instructions**: Run `docker-compose run --rm web python manage.py makemigrations users` and `docker-compose run --rm web python manage.py migrate` to apply the new user model.

## 3. HSDS Core Data Models & API

  - [x] Step 4: Create Core HSDS Django Models

      - **Task**: Create the `hsds` app and define the primary Django models based on the HSDS schema: `Organization`, `Program`, `Service`, and `Location`. Use `UUIDField` for all primary keys.
      - **Files**:
          - `apps/hsds/models.py`: Define the `Organization`, `Program`, `Service`, and `Location` models with their respective fields and relationships (`ForeignKey`).
          - `apps/hsds/admin.py`: Register the new models with the Django admin for easy inspection.
          - `apps/hsds/apps.py`: Standard app configuration.
      - **Step Dependencies**: Step 3.
      - **User Instructions**: Run `docker-compose run --rm web python manage.py makemigrations hsds` and `docker-compose run --rm web python manage.py migrate`.

  - [x] Step 5: Create DRF Serializers and Viewsets for Core Models

      - **Task**: Implement DRF `ModelSerializer` and `ModelViewSet` classes for the `Organization`, `Program`, `Service`, and `Location` models. Set up the basic API routing.
      - **Files**:
          - `apps/hsds/api.py`: Create `OrganizationSerializer`, `ServiceSerializer`, etc., and corresponding `OrganizationViewSet`, `ServiceViewSet`, etc.
          - `apps/hsds/urls.py`: Create a new file for routing. Define an `api_router` using DRF's `DefaultRouter` and register the new viewsets.
          - `conduit/urls.py`: Include the `hsds` app's API URLs under the `/api/v1/` path.
          - `conduit/settings.py`: Add `rest_framework` and `django_filters` to `INSTALLED_APPS`. Configure default DRF settings.
      - **Step Dependencies**: Step 4.
      - **User Instructions**: Verify the new API endpoints are browsable at `http://localhost:8000/api/v1/`.

## 4. HSDS Relational Models & API Expansion

  - [x] Step 6: Implement Remaining HSDS Relational Models

      - **Task**: Add the remaining, more granular HSDS models to `apps/hsds/models.py`. This includes `Address`, `Phone`, `Contact`, `Schedule`, `Accessibility`, `Taxonomy`, `TaxonomyTerm`, and others from the `database_postgresql.sql` schema.
      - **Files**:
          - `apps/hsds/models.py`: Add the new models, ensuring all `ForeignKey` relationships are correctly defined.
          - `apps/hsds/admin.py`: Register the new models with the admin site.
      - **Step Dependencies**: Step 4.
      - **User Instructions**: Run `docker-compose run --rm web python manage.py makemigrations hsds` and `docker-compose run --rm web python manage.py migrate`.

  - [x] Step 7: Implement DRF Serializers and Viewsets for Relational Models

      - **Task**: Create the corresponding DRF `ModelSerializer` and `ModelViewSet` classes for all the relational models added in the previous step. Update the core serializers to use nested serializers for their relationships where appropriate (e.g., nesting `AddressSerializer` within `LocationSerializer`).
      - **Files**:
          - `apps/hsds/api.py`: Add new serializers and viewsets. Update existing serializers to handle nested representations according to the `service_full.json` example.
          - `apps/hsds/urls.py`: Register the new viewsets with the `api_router`.
      - **Step Dependencies**: Step 5, Step 6.
      - **User Instructions**: Check the browsable API to ensure nested data is appearing correctly on detail views.

## 5. Frontend Setup & UI Shell

  - [ ] Step 8: Configure Frontend Tooling and Base Templates

      - **Task**: Set up Tailwind CSS for styling, and create the base templates that will include HTMX and Alpine.js from a CDN. This establishes the visual foundation for the management interface.
      - **Files**:
          - `tailwind.config.js`: Configure Tailwind CSS.
          - `static/css/input.css`: Main CSS file for Tailwind directives.
          - `templates/base.html`: Main site template including CSS, HTMX, Alpine.js, and blocks for content and navigation.
          - `templates/nav.html`: A partial for the main navigation bar.
          - `conduit/settings.py`: Configure static files and template directories.
      - **Step Dependencies**: Step 2.
      - **User Instructions**: Run the Tailwind CSS build command to generate `output.css`.

  - [ ] Step 9: Implement User Authentication Views and Templates

      - **Task**: Create login and logout views and templates for the management interface. The pages should use the `base.html` template.
      - **Files**:
          - `apps/users/views.py`: Create Django's class-based `LoginView` and `LogoutView`.
          - `apps/users/urls.py`: Define URLs for login and logout.
          - `templates/registration/login.html`: Create the login form template.
          - `conduit/urls.py`: Include the `users` app URLs and Django's auth URLs.
          - `conduit/settings.py`: Set `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL`.
      - **Step Dependencies**: Step 3, Step 8.

## 6. Data Management CRUD Interface (HTMX)

  - [ ] Step 10: Build Organization CRUD Interface

      - **Task**: Create the views and templates to list, view, create, and edit `Organization` records. Use HTMX for form submissions and partial page updates.
      - **Files**:
          - `apps/hsds/views.py`: Create `OrganizationListView`, `OrganizationDetailView`, `organization_create_view`, and `organization_edit_view` functions/classes.
          - `apps/hsds/urls.py`: Add URL patterns for the new management views under a `/manage/` prefix.
          - `templates/hsds/organization_list.html`: Displays a table of organizations.
          - `templates/hsds/organization_detail.html`: Displays an organization's details.
          - `templates/hsds/includes/organization_form.html`: A partial template for the create/edit form.
      - **Step Dependencies**: Step 7, Step 9.

  - [ ] Step 11: Build Service CRUD Interface with Nested Forms

      - **Task**: Implement the CRUD interface for the `Service` model. This is more complex and will require handling related objects like `Phone` and `Schedule` using HTMX to dynamically add/remove nested forms.
      - **Files**:
          - `apps/hsds/views.py`: Add views for `Service` CRUD operations and additional views to handle HTMX requests for adding/removing related objects.
          - `apps/hsds/urls.py`: Add URLs for the `Service` management views.
          - `templates/hsds/service_detail.html`: Display service details and lists of related objects.
          - `templates/hsds/includes/service_form.html`: The main form for editing a service.
          - `templates/hsds/includes/phone_form.html`: A partial for a single phone form, used for dynamic additions.
      - **Step Dependencies**: Step 10.

  - [ ] Step 12: Implement Remaining CRUD Interfaces

      - **Task**: Systematically build out the remaining CRUD interfaces for all other HSDS models (`Location`, `Contact`, `Taxonomy`, etc.), following the patterns established in the previous two steps.
      - **Files**:
          - `apps/hsds/views.py`: Add views for the remaining models.
          - `apps/hsds/urls.py`: Add URLs for the remaining views.
          - `templates/hsds/...`: Corresponding list, detail, and form partial templates for each model.
      - **Step Dependencies**: Step 11.

## 7. Final Features & Polish

  - [ ] Step 13: Centralize Validation and API Filtering

      - **Task**: Refine the HTMX views to use the DRF serializers for all validation logic. Implement filtering on the API endpoints using `django-filter`.
      - **Files**:
          - `apps/hsds/views.py`: Update all form-handling views to instantiate the corresponding serializer, call `.is_valid(raise_exception=True)`, and then `.save()`.
          - `apps/hsds/api.py`: Add `filterset_fields` or custom `FilterSet` classes to the `ViewSets` to enable API filtering.
      - **Step Dependencies**: Step 12.

  - [ ] Step 14: Implement Search and Data Export

      - **Task**: Add a basic search bar to the management UI. Create Django management commands to export all data to HSDS-compliant JSON and a set of CSVs.
      - **Files**:
          - `apps/hsds/views.py`: Create a `SearchView`.
          - `templates/nav.html`: Add the search form to the navigation bar.
          - `templates/hsds/search_results.html`: Template to display search results.
          - `apps/hsds/management/commands/export_hsds_json.py`: Command for JSON export.
          - `apps/hsds/management/commands/export_hsds_csv.py`: Command for CSV export.
      - **Step Dependencies**: Step 13.

  - [ ] Step 15: Add Localization Support

      - **Task**: Integrate `django-modeltranslation` to allow for translatable model fields. Add Django's i18n to the templates to allow for UI translation.
      - **Files**:
          - `apps/hsds/translation.py`: Configure which model fields are translatable.
          - `conduit/settings.py`: Add `modeltranslation` to `INSTALLED_APPS` and configure languages.
          - `templates/**/*.html`: Update all templates to use the `{% trans %}` template tag for static text.
      - **Step Dependencies**: Step 12.
      - **User Instructions**: Run `makemessages` and compile language files.

## 8. Testing & Deployment

  - [ ] Step 16: Write Tests

      - **Task**: Write a suite of tests covering model validation, API endpoint responses, and view permissions.
      - **Files**:
          - `apps/hsds/tests.py`: Add `TestCase` or `APITestCase` classes for testing models, API endpoints, and view logic.
          - `apps/users/tests.py`: Add tests for the custom user model and roles.
      - **Step Dependencies**: All previous steps.

  - [ ] Step 17: Configure CI/CD Pipeline

      - **Task**: Create a GitHub Actions workflow that automatically runs tests on every push and pull request to the main branch.
      - **Files**:
          - `.github/workflows/ci.yml`: Define the workflow to install dependencies, run `pytest`, and potentially build a Docker image.
      - **Step Dependencies**: Step 16.
