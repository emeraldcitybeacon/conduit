# Conduit: OpenReferral HSDS Django Data Management Platform Project Specification

-----

## 1. Planning & Discovery

### 1.1 Core Purpose & Success

  * **Mission Statement**: To provide a robust and intuitive open-source platform for managing and sharing human services data conformant with the OpenReferral HSDS standard.
  * **Core Purpose & Goals**:
      * Create a canonical, single source of truth for human services data for an organization or a network of organizations.
      * Simplify the process of creating, editing, and maintaining HSDS-compliant data through a user-friendly interface.
      * Enable seamless data sharing and interoperability by providing a standardized, well-documented API.
      * Reduce data silos and improve the accuracy and availability of community resource information.
  * **Success Indicators**:
      * **Adoption Rate**: Number of organizations actively using the platform to manage their data.
      * **Data Quality**: Reduction in data entry errors and stale information, measured by validation reports or user feedback.
      * **API Usage**: Volume and frequency of API calls from external applications, indicating successful data integration.
      * **User Satisfaction**: Positive feedback from data managers on the ease of use and efficiency of the data management interface.
  * **Experience Qualities**:
      * **Efficient**: The interface should minimize clicks and streamline repetitive data entry tasks.
      * **Clear**: The data structure and forms should be unambiguous, guiding users to enter correct, HSDS-compliant information.
      * **Reliable**: The system must ensure data integrity and consistency between the UI and the API.

### 1.2 Project Classification & Approach

  * **Complexity Level**: Complex App. While the core functionality is CRUD, the strict adherence to a complex data specification (HSDS), the dual-interface requirement (HTMX frontend and DRF API), and the need for tight synchronization elevate the complexity.
  * **Primary User Activity**: Creating and Acting. Data managers are primarily *creating* and curating resource data. Developers are *acting* upon this data via the API.
  * **Primary Use Cases**:
      * A data manager logs in, adds a new organization, defines the services it offers, and specifies its locations, schedules, and contact information.
      * An editor updates an existing service's description and eligibility criteria. The changes are immediately available via the API.
      * An external application (e.g., a public-facing service finder) queries the API to retrieve a list of all active counseling services within a specific geographic area.
      * An administrator adds a new "Editor" user account and assigns them permissions to manage a specific set of organizations.

### 1.3 Feature-Selection Rationale

  * **Core Problem Analysis**: Managing human services data is complex and often done in isolated, non-standardized systems. This makes it difficult to maintain, share, and use the data effectively to connect people with resources.
  * **User Context**: Data managers will use this application as a primary tool during their workday. The interface needs to be robust enough for bulk data entry but also intuitive for infrequent updates. Developers will integrate with the API asynchronously.
  * **Critical Path**: `User logs in` -\> `Mapss to "Organizations"` -\> `Creates a new Organization record` -\> `Adds a Service to the Organization` -\> `Adds a Location to that Service` -\> `The new service is now available via the /services API endpoint`.
  * **Key Moments**:
    1.  **Seamless Form Interaction**: A data manager edits a complex entity (like a `Service` with multiple related `Schedules` and `Contacts`) on a single page, with HTMX providing smooth, inline additions and updates without a full page reload.
    2.  **Instant API Parity**: After saving a change in the UI, a developer immediately sees the updated data reflected in a query to the DRF API, confirming the system's integrity.

### 1.4 High-Level Architecture Overview

```
+-------------------+      +---------------------------------+      +------------------------+
|      Users        |      |      Django Web Application     |      |                        |
| (Data Managers,   | <--> |  (Hosted on Docker Container)   | <--> |   PostgreSQL Database  |
|  Admins, Editors) |      |                                 |      |                        |
+-------------------+      |---------------------------------|      +------------------------+
                         | 1. Django Auth & Permissions    |
                         | 2. HTMX Views & Templates       |
                         |    - Renders data entry forms   |
                         |    - Consumes internal DRF API  |
                         | 3. Django Rest Framework (DRF)  |
                         |    - HSDS-compliant API         |
                         |    - Endpoints (/services, etc.)|
                         | 4. Django Models & Validation   |
                         |    - HSDS Schema implementation |
                         +---------------------------------+
                                      ^
                                      |
+-------------------+                 |
| External Systems/ |                 |
|   Applications    | <---------------' (API Consumers)
+-------------------+
```

-----

## 2. System Architecture & Technology

### 2.1 Tech Stack

  * **Languages & Frameworks**: Python 3.11+, Django 5.x, Django Rest Framework 3.14+
  * **Frontend Libraries**: HTMX 1.9+, Alpine.js 3.x, Tailwind CSS 3.x
  * **Database & ORM**: PostgreSQL 15+, Django ORM
  * **DevOps & Hosting**: Docker, Docker Compose (for local development and production deployment), Gunicorn/Uvicorn
  * **CI/CD Pipeline**: GitHub Actions for running tests, linting, and building Docker images.

### 2.2 Project Structure

A monolithic Django project structure is recommended.

```
/conduit/
|-- .dockerignore
|-- .gitignore
|-- docker-compose.yml
|-- Dockerfile
|-- manage.py
|-- poetry.lock
|-- pyproject.toml
|-- README.md
|-- /conduit/             # Django Project Root
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|-- /apps/
|   |-- /core/            # Shared utilities, base models, etc.
|   |-- /hsds/            # The main app for HSDS models, API, views
|   |   |-- /migrations/
|   |   |-- /management/
|   |   |-- /static/
|   |   |-- /templates/
|   |   |   |-- /hsds/
|   |   |   |   |-- includes/  # HTMX partials
|   |   |   |   |-- base.html
|   |   |   |   |-- service_form.html
|   |   |   |   |-- ...
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- api.py        # DRF ViewSets and Serializers
|   |   |-- apps.py
|   |   |-- models.py     # All HSDS Django models
|   |   |-- tests.py
|   |   |-- urls.py       # URLs for both API and HTMX views
|   |   |-- views.py      # HTMX-serving views
|   |-- /users/           # Custom User model, authentication views
|       |-- ...
|-- /static/              # Global static files
|-- /templates/           # Global templates (e.g., 404.html)
```

### 2.3 Component Architecture

#### Server / Backend

  * **Framework**: Django with DRF.
  * **Data Models & Domain Objects**: Models will be defined in `apps/hsds/models.py`, directly translating the provided PostgreSQL schema (`openreferral/database/database_postgresql.sql`) into Django's ORM. All primary keys will be UUIDs as per the HSDS specification.
  * **Error Boundaries**: DRF will handle API exception handling, returning standard 4xx/5xx responses. HTMX views will catch exceptions from internal API calls and render user-friendly error messages or partials. A global Django middleware can be used for logging unhandled exceptions.

#### Client / Frontend

  * **State Management**: Minimal client-side state is required. Alpine.js will handle localized UI state within components (e.g., toggling a dropdown, showing/hiding a modal). Server-side state is the source of truth, fetched via HTMX.
  * **Routing**: Django's standard URL routing will be used. Separate URL namespaces for the API (`/api/v1/`) and the web interface (`/manage/`) will be used.
  * **Type Definitions**: Not applicable for the frontend stack.

### 2.4 Data Flow & Real-Time

  * **Request/Response Lifecycle (HTMX Views)**:
    1.  User interacts with a UI element (e.g., clicks "Add Contact").
    2.  HTMX sends a `GET` request to a Django view (e.g., `/manage/services/1/add-contact/`).
    3.  The Django view makes an internal request to the DRF API is not strictly necessary for simple form rendering. The view can directly render an empty form partial.
    4.  The rendered HTML partial (e.g., a `contact_form.html`) is returned to the browser.
    5.  HTMX swaps the new form into the DOM.
    6.  User submits the form. HTMX sends a `POST` request to another Django view.
    7.  The view receives the form data, calls the corresponding DRF serializer to validate and save the data. This enforces the "API as Source of Truth" for business logic.
    8.  If validation fails, the view re-renders the form partial with error messages.
    9.  If successful, the view returns a new partial showing the newly created contact, which HTMX swaps into the list of contacts.
  * **State Sync**: The UI is always a reflection of the database state. Any action that modifies data will trigger an HTMX request that returns an updated view of that data.
  * **Real-Time Updates**: Not required for MVP.

-----

## 3. Database & Server Logic

### 3.1 Database Schema

The Django models will be generated based on the `openreferral/database/database_postgresql.sql` file. All `id` fields will be `models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`. Foreign key relationships will use `models.ForeignKey` with `on_delete=models.CASCADE` (or other appropriate strategies).

**Example Model Translation (`service` table):**

```python
# apps/hsds/models.py
import uuid
from django.db import models

class Service(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        DEFUNCT = 'defunct', 'Defunct'
        TEMPORARILY_CLOSED = 'temporarily closed', 'Temporarily Closed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='services')
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    name = models.TextField()
    alternate_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    interpretation_services = models.TextField(blank=True, null=True)
    application_process = models.TextField(blank=True, null=True)
    fees_description = models.TextField(blank=True, null=True)
    # ... other fields from the schema ...
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ... other models like Organization, Location, Contact, etc.
```

### 3.2 Server Actions

#### Database Actions

  * **CRUD Operations**: Will be handled by DRF `ModelViewSet`s. Each HSDS object (Organization, Service, Location, etc.) will have its own `ViewSet`.
  * **Endpoints / DRF Serializers**:
      * Serializers will be defined for each model, controlling the JSON representation. Nested serializers will be used to represent relationships as seen in `service_full.json`.
      * Endpoints will follow the HSDS API reference, e.g., `/api/v1/services/`, `/api/v1/services/{id}/`, `/api/v1/organizations/`.
  * **ORM/Query Examples**:
      * **Filtering**: DRF's `filter_backends` will be used to implement query parameter filtering (e.g., `?organization_id=...`).
      * `django-filter` library will be used for advanced filtering.

#### Other Backend Logic

  * **Centralized Validation**: Model methods (`clean()`) and custom validators will hold business logic. Serializers and Forms will call `instance.full_clean()` to ensure model-level validation is always run.
  * **Localization**: Django's built-in internationalization (i18n) and localization (l10n) framework will be used for the UI. For data, a library like `django-modeltranslation` can be used to provide translations for character fields on models (like `name` and `description`).

-----

## 4. Feature Specifications

### User Management

  * **User Story & Requirements**: As an Administrator, I need to be able to create, edit, and assign roles (Administrator, Editor, Viewer) to users so that I can control access to the data.
  * **Implementation Details**:
    1.  Extend Django's `AbstractUser` model to add a `role` field.
    2.  Use Django's built-in admin for user management initially.
    3.  Implement a custom middleware or use a library like `django-guardian` to enforce object-level permissions if needed, or simple role-based permissions on views.
    4.  DRF API endpoints will use `permissions.IsAdminUser`, `permissions.IsAuthenticated`, etc.
  * **UI/UX Considerations**: A simple table of users with actions to edit or delete.

### Data Management Interface (HTMX)

  * **User Story & Requirements**: As a Data Manager, I want to be able to view a list of all services, click on one to see its details, and edit its fields inline without leaving the page, so I can work efficiently.
  * **Implementation Details**:
    1.  Create a `ServiceListView` that renders a list of services.
    2.  Each service in the list has an `hx-get` attribute to load its detail view into a target div.
    3.  The detail view will have "edit" buttons next to fields or sections.
    4.  Clicking "edit" will `hx-get` a form partial and swap it with the display content.
    5.  Submitting the form will `hx-post` the data. The view will process the data via the DRF serializer, and on success, return the updated display partial.
  * **Edge Cases & Error Handling**: If the API call from the view fails (e.g., validation error), the view should return the form partial again, now populated with error messages from the serializer. The response should have a `400` status code, which HTMX can handle.

### HSDS API (DRF)

  * **User Story & Requirements**: As a developer, I need to be able to retrieve a paginated list of services by making a GET request to `/api/v1/services/`, and filter the results by organization, so that I can build an external application using this data.
  * **Implementation Details**:
    1.  Create a `ServiceSerializer` and a `ServiceViewSet`.
    2.  The `ServiceViewSet` will inherit from `ModelViewSet`.
    3.  Configure `django-filter` with a `ServiceFilterSet` to enable filtering by `organization_id`, `taxonomy_term_id`, etc., as per the API specification.
    4.  Configure DRF's pagination classes (`PageNumberPagination`) to match the pagination structure (`total_items`, `total_pages`, etc.) defined in the HSDS API reference.

-----

## 5. Design System

### 5.1 Visual Tone & Identity

  * **Branding & Theme**: Clean, professional, and data-focused. Minimalist aesthetic to prioritize content and usability.
  * **Emotional Response**: Trustworthy, organized, efficient.
  * **Design Personality**: Classic and utilitarian.
  * **Simplicity Spectrum**: Minimal. The UI should be a clean shell around the data.

### 5.2 Color Strategy

  * **Scheme**: Monochromatic with a single accent color.
  * **Primary**: A neutral gray for text and backgrounds.
  * **Accent**: A clear, accessible blue for links, buttons, and focus states.

### 5.3 Typography System

  * **Font Pairing Strategy**: Use a single, highly-readable sans-serif font family like Inter or Source Sans Pro, available from Google Fonts.
  * **Typographic Hierarchy**: Clear hierarchy using font size, weight (regular, medium, bold), and color.

### 5.6 UI Elements & Components

  * **Framework**: Tailwind CSS.
  * **Common Elements**: Buttons, form inputs, labels, and modals will have consistent styling defined in a base CSS file or through Tailwind's `@apply` directive.
  * **Component States**: All interactive elements must have clear `:hover`, `:focus`, `:disabled`, and error states.

### 5.8 Accessibility & Readability

  * **Accessibility Considerations**: All forms will use `<label>` tags. ARIA attributes will be used where necessary. The application should be navigable via keyboard.
  * **Contrast Goal**: All text/background color combinations must meet WCAG AA standards.

-----

## 6. Security & Compliance

  * **Authentication**: Use Django's built-in session authentication for the web interface and token authentication (e.g., `TokenAuthentication`) for the DRF API.
  * **Permissions**: As defined in the User Management section, view-level permission checks will be enforced.
  * **Data Security**: Use Django's built-in protections against CSRF, XSS, and SQL injection. All sensitive credentials will be stored in environment variables, not in code.
  * **Secrets Management**: Use a `.env` file for local development and the hosting provider's secret management system for production.

-----

## 8. Environment Configuration & Deployment

  * **Local Setup**: A `docker-compose.yml` file will orchestrate the Django application container and a PostgreSQL database container. A `.env.example` file will document required environment variables.
  * **Staging / Production Environments**: Docker images will be built by the CI/CD pipeline and deployed to a container hosting service (e.g., AWS ECS, Heroku, or DigitalOcean App Platform).
  * **CI/CD**: A GitHub Actions workflow will be configured to:
    1.  Run on every push to `main` and on pull requests.
    2.  Install dependencies.
    3.  Run the test suite (`pytest`).
    4.  Build and push the Docker image to a registry.

-----

## 9. Testing & Quality Assurance

  * **Unit Testing**: `pytest-django` will be used to test models, validators, and utility functions.
  * **Integration Testing**: Tests will cover the interaction between views, serializers, and models. API endpoints will be tested to ensure they return the correct data structure and status codes.
  * **End-to-End Testing**: Not in scope for MVP, but the "API as Source of Truth" architecture simplifies this, as the frontend and API can be tested independently.

-----

## 10. Edge Cases, Implementation Considerations & Reflection

  * **Potential Obstacles**:
      * **Schema Complexity**: The HSDS schema is large and has many interconnected tables. Ensuring all relationships are correctly modeled and handled in forms and serializers will be complex.
      * **Synchronization Drift**: The user rightly identified the risk of the DRF API and HTMX frontend logic diverging. The chosen architecture (HTMX views using API serializers for validation) is the key mitigation strategy.
  * **Edge-Case Handling**:
      * **Orphaned Data**: What happens if a `Service` is deleted? All related objects (schedules, contacts, etc.) should cascade delete as defined by the model's `on_delete` policy.
      * **Data Validation**: The system must handle complex validation rules, such as ensuring `valid_to` is after `valid_from` in `schedule` objects.
  * **Technical Constraints**: The reliance on HTMX means the application will not function without JavaScript enabled. This is acceptable for a data management back-office tool.
  * **Critical Questions**: How will the initial data be populated? While import is post-MVP, a strategy for seeding the database for development is needed (e.g., using Django data migrations or management commands).
  * **Approach Suitability**: The Django + HTMX/Alpine stack is an excellent fit. It leverages Django's strengths in data modeling and APIs while providing a modern, dynamic frontend experience without the complexity of a full JavaScript framework.

-----

## 11. Summary & Next Steps

  * **Recap**: This specification outlines a Django application, "Conduit," for managing HSDS data. It features a dual interface: a data management UI built with HTMX and a DRF-powered API. The core architectural principle is to use the API's serializers as the single source of truth for validation and business logic, which the HTMX views will consume, thus minimizing code duplication and preventing synchronization drift. The project includes role-based access control, localization support, and a plan for future data import/export features.
  * **Open Questions**:
    1.  What is the initial dataset? Will there be an existing dataset to migrate? None.
    2.  Are there any specific performance requirements for the API (e.g., response times for large queries)? Not really.
  * **Future Enhancements**:
      * Full-featured data import/export tools.
      * Advanced search and filtering capabilities in the UI.
      * A public-facing dashboard for data quality metrics.
      * Support for HSDS Profiles to extend the core schema for local needs.
