# Conduit: OpenReferral HSDS Django Data Management Platform

## Description
This project aims to create a Django application for managing and editing human services data that conforms to the OpenReferral HSDS specification. The application will provide a user-friendly interface for data entry and editing using HTMX and Alpine.js, and will also expose a Django Rest Framework (DRF) API for serving the data in a standardized way. The goal is to create a seamless system where the data management interface and the API are tightly integrated to prevent data and logic from becoming out of sync.

## Target Audience
 * Data Managers: Individuals responsible for inputting, updating, and maintaining human services data. They need an intuitive and efficient interface for their work.
 * Developers: Software developers who will be building and maintaining the application, as well as those who will be consuming the HSDS data via the API.
 * Organizations: Non-profits, government agencies, and other organizations that provide human services and need a standardized way to manage their resource directory information.

## Desired Features
Data Modeling
 * [ ] HSDS-Compliant Models: Create Django models that accurately represent the HSDS schema.
   * [ ] Use the provided docs/openreferral/database/database_postgresql.sql as a starting point for the model structure.
   * [ ] Refer to docs/openreferral/schema_reference.md for authoritative definitions of all objects and fields.
 * [ ] Relationships: Implement the relationships between models (e.g., organization to service, service to location) as defined in the HSDS schema.
User Management
 * [ ] Authentication: Implement a standard user authentication system.
 * [ ] Authorization: Create a role-based authorization system.
   * [ ] Administrator: Can manage users and has full CRUD access to all data.
   * [ ] Editor: Can create, read, and update data.
   * [ ] Viewer: Can only read data.
Data Management Interface
 * [ ] CRUD Operations: Provide a web interface for creating, reading, updating, and deleting all HSDS data, respecting user roles.
 * [ ] HTMX & Alpine.js: Use HTMX for dynamic, partial-page updates and Alpine.js for client-side interactivity.
 * [ ] User-Friendly Forms: Design forms that are easy to use and guide data managers in entering accurate information.
HSDS API
 * [ ] DRF API: Implement a Django Rest Framework API to serve the HSDS data.
 * [ ] OpenAPI Compliance: Ensure the API is compliant with the HSDS OpenAPI specification found in docs/openreferral/schema/openapi.json.
 * [ ] API Endpoints: Create the necessary API endpoints for all the core HSDS objects (e.g., /services, /organizations, /locations).
 * [ ] Filtering and Pagination: Implement the filtering and pagination options as specified in the api_reference.md.
Data Export
 * [ ] HSDS Export: Provide a mechanism to export the data in the HSDS JSON format.
 * [ ] Tabular Export: Consider an option to export the data in the HSDS tabular (CSV) format as described in docs/openreferral/examples/tabular.json.
Data Import (Post-MVP)
 * [ ] CSV Import: Develop a feature to import data from a CSV file.
 * [ ] HSDS JSON Import: Develop a feature to import data from an HSDS-compliant JSON file.
Search Functionality
 * [ ] Basic Search (MVP): Implement a simple text-based search across all relevant fields.
 * [ ] Advanced Search (Future): Plan for future enhancements to allow for filtering by specific fields and taxonomies.
Localization
 * [ ] Data Localization: Support for storing and managing data in multiple languages, as specified by the HSDS language object.
 * [ ] Interface Localization: The user interface should be translatable into multiple languages.
Design Requests
 * [ ] API as the Source of Truth: The primary architectural approach will be to have the HTMX-powered views and forms act as consumers of the local DRF API.
   * [ ] HTMX views should make internal HTTP requests to the DRF endpoints to fetch and submit data.
 * [ ] Centralized Validation: Validation logic should be centralized in the Django models or a shared service layer to ensure consistency between the data management interface and the API.
   * [ ] DRF serializers and Django forms should both utilize this shared validation logic.
 * [ ] Error Handling: Gracefully handle API errors in the HTMX views and provide clear feedback to the user.
Other Notes
 * Synchronization: A key challenge will be keeping the Django models, DRF serializers, and HTMX forms/templates in sync. A strict development process with code reviews focused on this aspect will be necessary.
 * Performance: Caching strategies should be considered at the API layer to ensure good performance.
 * Future-Proofing: The system should be designed with the potential for future extensions and profiles of HSDS in mind, as discussed in docs/openreferral/extending.md.
