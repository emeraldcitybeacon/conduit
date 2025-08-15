# Pulse — Volunteer Resource Editor Project Specification

---

## 1. Planning & Discovery

### 1.1 Core Purpose & Success

* **Mission Statement**: Enable volunteers and editors to rapidly create, validate, and maintain hyper-local HSDS data through a unified “Resource” editor without altering HSDS tables.
* **Core Purpose & Goals**:
  - Provide a stitched, single-pane editor (“Resource”) that writes correct HSDS.
  - Accelerate sibling-aware edits and safe propagation via shelves and bulk apply.
  - Make freshness, provenance, and history first-class without schema surgery.
* **Success Indicators**:
  - Time-to-edit (open → save) median < 60s (informational).
  - Review-required changes approved within 48h (process).
  - ≥80% of resources show field-level freshness within 90 days.
* **Experience Qualities**: Fast, legible, trustworthy.

### 1.2 Project Classification & Approach

* **Complexity Level**: Complex App.
* **Primary User Activity**: Acting (editing) and Interacting (reviews/merges).
* **Primary Use Cases**:
  - Volunteer opens a Resource, fixes phone/hours, auto-publishes.
  - Volunteer creates a new Resource via Wizard; editor approves draft.
  - Editor stages a phone update across a shelf of sibling resources, previews, commits, and can undo.

### 1.3 Feature-Selection Rationale

* **Core Problem**: HSDS editing is multi-entity and slow; volunteers need a single window with safe guardrails.
* **User Context**: On-site or desktop, short sessions, browser-only; no offline.
* **Critical Path**: Find → Edit inline (validated) → Save / Submit-for-review → Provenance auto-captured.
* **Key Moments**:
  - Diff preview before committing.
  - One-click “apply to siblings/shelf”.
  - Hover history + revert at field level.

### 1.4 High-Level Architecture Overview

* **Client**: HTMX + Tailwind v4 + daisyUI v5; server-rendered templates with partial swaps.
* **Server**: Django + DRF façade endpoints; permission + moderation engine; JSON Patch engine.
* **Database**: PostgreSQL (HSDS core tables untouched) + extension tables (`hsds_ext_*`).
* **Services**: GeocodeService (pluggable), Search indexing (pg_trgm), Email/Slack later (deferred).

### 1.5 Essential Features

* **Unified Resource Pane** — Stitched Org⇄Location⇄Service editor with always-on validation; daisyUI forms.
* **Create Wizard** — 3 steps with prefill from siblings; draft stored; editor approval writes HSDS.
* **Shelf & Bulk Apply** — Queue arbitrary resources; stage patch → preview → commit → undo.
* **Freshness & History** — Field-level verification events and versioning; revert.
* **Dedupe & Merge** — Live hints; split-view merge generating JSON Patch.
* **Sensitive Mode** — Read-time redaction overlay for address/contacts.

---

## 2. System Architecture & Technology

### 2.1 Tech Stack

* **Languages & Frameworks**: Python 3.12, Django 5.x, Django REST Framework.
* **Frontend**: HTMX, Tailwind CSS v4, **daisyUI v5**.
* **Database & ORM**: PostgreSQL 15+, Django ORM, `pg_trgm` extension for fuzzy search.
* **DevOps & Hosting**: Docker, docker-compose; Render/Heroku/Fly (any PaaS) or k8s later.
* **CI/CD Pipeline**: GitHub Actions (lint, tests, migrations, deploy).

### 2.2 Project Structure

```

/pulse
/apps
/hsds            # existing HSDS app (read/write via canonical serializers)
/resource_api    # façade endpoints, serializers, review queue
/ext             # extension models: drafts, change_requests, versions, shelves...
/ui              # templates, HTMX partials, daisyUI components
/static
/templates
/tests

````

* **Naming Conventions**: snake_case for Python; kebab-case for templates; REST endpoints kebab-case.
* **Key Modules**: auth/roles, moderation, json_patch, geocode_service, search.

### 2.3 Component Architecture

#### Server / Backend

* **Framework**: Django + DRF ViewSets; HTMX endpoints as DRF or Django views returning partial templates.
* **Domain Objects**: `ResourceComposite` (aggregates Org, Location, Service), `ChangeRequest`, `DraftResource`, `BulkOperation`, `VerificationEvent`, `FieldVersion`, `SensitiveOverlay`, `Shelf`.
* **Error Boundaries**: Global DRF exception handler → problem+json (`type`, `title`, `detail`, `instance`).

#### Client / Frontend

* **State**: Server-driven; HTMX swaps; minimal JS (keyboard registry + shelf interactions).
* **Routing**: Django URLs; `/<resource-id>` loads pane; modals use HTML `<dialog>` with daisyUI `modal`.
* **Types**: TS not required; use JSDoc typedefs for HTMX payloads if desired.

### 2.4 Data Flow & Real-Time

* **Lifecycle**: GET resource → render façade + `etags` map → user edits → PATCH with `If-Match` and asserted field versions → success returns updated partials + new etags.
* **State Sync**: HTMX triggers (`hx-trigger="change from:input"`); server returns partial HTML (daisyUI-styled) or JSON for shelf ops.
* **Real-Time**: No sockets; optimistic UI is via quick round-trips.

---

## 3. Database & Server Logic

### 3.1 Database Schema (extensions only)

> All tables are namespaced `hsds_ext_*`; **HSDS core tables are not modified**.

**`hsds_ext_verification_events`**
- `id` PK
- `entity_type` enum(`organization`,`location`,`service`,`service_at_location`)
- `entity_id` uuid/int (FK logically)
- `field_path` text (dot path, e.g., `contacts.phones[0].number`)
- `method` enum(`called`,`website`,`onsite`,`other`)
- `note` text null
- `verified_at` timestamptz not null default now()
- `verified_by_id` FK users
- **Index**: (entity_type, entity_id), (verified_at DESC), (field_path)

**`hsds_ext_field_versions`**
- `id` PK
- `entity_type`, `entity_id`, `field_path`
- `version` bigint not null default 1
- `updated_at` timestamptz not null default now()
- `updated_by_id` FK users
- **Unique**: (entity_type, entity_id, field_path)
- **Index**: (entity_type, entity_id)

**`hsds_ext_sensitive_overlays`**
- `id` PK
- `entity_type`, `entity_id`
- `sensitive` boolean not null default false
- `visibility_rules` jsonb not null default '{}'
  - Example: `{ "address": "redact_precise", "contacts": "hotline_only" }`
- **Unique**: (entity_type, entity_id)

**`hsds_ext_draft_resources`**
- `id` PK
- `created_by_id` FK users
- `created_at` timestamptz
- `status` enum(`draft`,`approved`,`rejected`) default `draft`
- `payload` jsonb  — composite HSDS data (org/location/service with temporary IDs)
- `review_note` text null

**`hsds_ext_change_requests`**
- `id` PK
- `target_entity_type`, `target_entity_id`
- `patch` jsonb  — RFC6902 operations against canonical HSDS JSON
- `status` enum(`pending`,`approved`,`rejected`) default `pending`
- `submitted_by_id`, `submitted_at`
- `reviewed_by_id`, `reviewed_at` null
- **Index**: (status), (target_entity_type, target_entity_id)

**`hsds_ext_shelves`**
- `id` PK
- `owner_id` FK users
- `name` text
- `created_at`
- `is_shared` boolean default false

**`hsds_ext_shelf_members`**
- `shelf_id` FK → shelves
- `entity_type`, `entity_id`
- `added_by_id`, `added_at`
- **PK**: (shelf_id, entity_type, entity_id)

**`hsds_ext_bulk_operations`**
- `id` PK
- `initiated_by_id`, `initiated_at`
- `scope` enum(`shelf`,`siblings`)
- `targets` jsonb  — array of `{entity_type, entity_id}`
- `patch` jsonb   — RFC6902
- `preview` jsonb — precomputed per-target diffs/result
- `status` enum(`staged`,`committed`,`undone`) default `staged`
- `undo_token` text
- `committed_at`, `undone_at` null

**`hsds_ext_taxonomy_extensions`** (optional)
- `id` PK
- `entity_type`, `entity_id`
- `namespace` text  — e.g., `local`
- `key` text        — e.g., `subtype`
- `value` text/jsonb

**Migrations**: Standard Django migrations for new `ext` app; enable `CREATE EXTENSION pg_trgm;`.

### 3.2 Server Actions

#### Endpoints (DRF)

**Resource Façade**
- `GET /api/resource/{id}`
  Returns composite HSDS JSON + overlays + `etags` map + `field_freshness`.
- `PATCH /api/resource/{id}`
  Auto-publish fields: body contains partial updates; headers: `If-Match: W/"<resource-version>"`. Include `assert_versions` map for edited fields. Writes HSDS + updates `hsds_ext_field_versions` and `hsds_ext_verification_events` if verify buttons used.

**Drafts & Wizard**
- `POST /api/resource`
  Creates `hsds_ext_draft_resources` from wizard final payload.
- `GET /api/drafts?status=draft|pending`
  List drafts (editor view).
- `POST /api/drafts/{id}/approve`
  Writes HSDS entities via canonical serializers, sets draft `approved`.
- `POST /api/drafts/{id}/reject`

**Review Queue (Change Requests)**
- `POST /api/resource/{id}/change-request`
  Body: `{ patch: [ ... RFC6902 ... ], note? }`.
- `GET /api/review-queue?status=pending`
- `POST /api/review-queue/{id}/approve`
- `POST /api/review-queue/{id}/reject`

**Shelves & Bulk Ops**
- `POST /api/shelves` | `GET /api/shelves/{id}` | `POST /api/shelves/{id}/add`
- `POST /api/shelves/{id}/stage-patch` → creates `hsds_ext_bulk_operations` (status: staged)
- `GET /api/bulk-ops/{id}/preview`
- `POST /api/bulk-ops/{id}/commit`
- `POST /api/bulk-ops/{id}/undo` (validate `undo_token`)

**Search & Dedupe**
- `GET /api/search?q=` (name/phone/street/tag; pg_trgm)
- `GET /api/resource/{id}/dup-hints` → candidates with confidence
- `POST /api/merge` → body `{ left_id, right_id, patch }` → apply patch to survivor; archive duplicate properly.

**Sensitive Overlays**
- `PATCH /api/resource/{id}/sensitive` → review-required; writes to `hsds_ext_sensitive_overlays` on approval.

**Freshness / Verify Buttons**
- `POST /api/resource/{id}/verify`
  Body: `{ field_path, method, note? }` → append verification event.

**Headers & ETags**
- Responses include `ETag: W/"<resource-version>"` and body includes
  `"etags": { "contacts.phones[0].number": "v12", "hours": "v4", ... }`

#### ORM/Query Examples

- Increment field version:

```python
FieldVersion.objects.update_or_create(
  entity_type=et, entity_id=eid, field_path=path,
  defaults={"version": F("version") + 1, "updated_by": user}
)
````

* JSON Patch apply (server):

```python
doc = canonical_hsds_json(resource_id)
patched = jsonpatch.apply_patch(doc, patch, in_place=False)
validate_with_serializers(patched)  # DRF validators
write_back_to_hsds(patched)         # split to org/location/service
```

---

## 4. Feature Specifications

### 4.1 Unified Resource Pane

**User Story**: As a volunteer, I can view and edit a single Resource (service-at-location + org context) with inline validation and visibility of freshness/history.

**Implementation Details**

* Template: `ui/resource/detail.html` (HTMX-enabled).
* Sections (daisyUI):

  * **Navbar** (`navbar`) with breadcrumbs (`breadcrumbs`).
  * **Tabs** (`tabs tabs-box`): Overview | Contacts | Hours | Access | Eligibility | Notes | History.
  * Forms: `input`, `select`, `textarea`, `toggle`, `validator`.
  * Status: `toggle` (active/temp closed/defunct as segmented controls via `join` + `btn`).
  * Freshness badges: `badge badge-info|success|warning|error`.
  * Save: `btn btn-primary`; Keyboard `⌘S`.
  * Diff preview modal: `modal` + `diff` (before save).
* Server: `GET /api/resource/{id}` render composite; HTMX partials for each tab.
* Validation: DRF serializer errors mapped to `.validator` hints.

**Edge Cases**

* Concurrent edits → show merge chips inline; ask user to re-apply.
* Redacted sensitive resource → address/contacts masked; editing restricted per permissions.

**UI/UX Notes**

* Use `label` + `input` parent wrapper pattern from daisyUI.
* Display ID chips with `badge-ghost`.

### 4.2 Create Wizard (Org → Location → Service)

**User Story**: Create a new Resource quickly with sibling-prefill and a final diff preview; saved as Draft.

**Implementation**

* Steps UI: `steps steps-horizontal`; each step is a `fieldset`.
* Prefill banners: `alert alert-info alert-soft` with “Undo prefill” (`btn btn-ghost btn-xs`).
* Final screen: `diff` showing “about to create” vs empty baseline.
* `POST /api/resource` stores composite JSON in `hsds_ext_draft_resources`.

**Validation**

* Real-time on each step; cannot proceed on hard errors.

**Edge Cases**

* Existing org/location detection via fuzzy search; warn on potential duplicates (`alert-warning` + link to open in split view).

### 4.3 Shelf & Bulk Apply

**User Story**: As an editor/volunteer, I add resources to a shelf (global queue), stage a phone/hours update, preview per-target changes, commit, and can undo.

**Implementation**

* Shelf UI: Right-hand `drawer` with a `list` of members; actions in `join` group.
* Stage Patch modal: `modal` with a small form (target field pickers using `select`) → server builds JSON Patch.
* Preview: `table table-sm` listing targets + result summary; optional `diff` per row.
* APIs as defined; `undo` available for 5–10 minutes.

**Edge Cases**

* Cross-org confirmation `modal` with `alert-error` note.
* Targets that fail validation are skipped with per-row `badge-error` and explanation.

### 4.4 Freshness & History

**User Story**: See when each field was last verified; quickly mark verify actions.

**Implementation**

* Freshness chips next to labels (`badge badge-soft` + tooltip).
* Verify buttons (`btn btn-ghost btn-xs`): “Called”, “Website”, “On-site”.
* History hover: popover/list (`timeline timeline-compact`) showing last N events; “Revert field” (`btn btn-outline btn-xs`).

**Edge Cases**

* Revert attempts that conflict with current field version prompt a rebase modal.

### 4.5 Dedupe & Merge

**User Story**: Get duplicate hints while typing; review candidates in split view; merge safely.

**Implementation**

* Hints: `toast toast-top toast-end` with candidate cards (`card card-sm`).
* Split-view merge: two columns with checkboxes; final JSON Patch produced and applied via `/api/merge`.
* Keep child objects with conflict badges (`badge-warning`).

**Edge Cases**

* Circular merges are prevented; surviving entity must be explicit.

### 4.6 Sensitive Mode

**User Story**: Mark resource sensitive; enforce redaction rules at read-time.

**Implementation**

* Sensitive toggle is review-required; show `alert-warning` that address/contacts will be redacted.
* Read-time overlay applies `visibility_rules` to response payload.

### 4.7 Checklists & Keyboard Overlay

**Checklist**

* Inline `list` with checkboxes (`checkbox checkbox-sm`), each item writes a verification event.

**Keyboard Overlay**

* `?` opens a `modal` listing actions using `kbd` tokens (e.g., `<kbd class="kbd kbd-xs">⌘</kbd><kbd class="kbd kbd-xs">S</kbd>`).
* Registry stored as JSON; rendered server-side.

---

## 5. Design System

### 5.1 Visual Tone & Identity

* Clear, minimal, utilitarian; high-contrast and accessible.

### 5.2 Color Strategy

* Use daisyUI semantic tokens: `base-*` for surfaces, `primary` for CTAs, `info/success/warning/error` for statuses. Respect theme switching later.

### 5.3 Typography System

* System fonts; readable sizes; consistent `label` usage; avoid custom fonts initially.

### 5.4 Visual Hierarchy & Layout

* Single-column forms; `divider` between sections; use whitespace generously.

### 5.5 Animations

* Minimal motion; use native focus/hover states; avoid bespoke animations.

### 5.6 UI Elements & Components (daisyUI notes)

* **Nav & Shell**: `navbar`, `drawer`
* **Forms**: `input`, `select`, `textarea`, `toggle`, `validator`, `label`
* **Feedback**: `alert`, `badge`, `toast`, `modal`
* **Navigation**: `breadcrumbs`, `tabs`, `steps`
* **Data**: `table`, `timeline`, `diff`, `stat`
* **Utility**: `join`, `kbd`, `divider`, `skeleton`

### 5.7 Visual Consistency Framework

* Component-based; no custom CSS if possible; Tailwind utilities for adjustments.

### 5.8 Accessibility & Readability

* WCAG AA; ARIA on tabs/steps/modals; validator hints tied to inputs via `aria-describedby`.

---

## 6. Security & Compliance

* **Auth**: Django session auth; CSRF-protected HTMX calls; role-based permissions (Volunteer, Editor, Admin).
* **Authorization**:

  * Auto-publish field writes allowed to Volunteers.
  * Review-required fields create ChangeRequests; approvals restricted to Editors/Admins.
* **Auditability**: All writes produce FieldVersion rows; verification events recorded with actor and time.
* **PII**: Avoid storing personal data in notes; PII checker deferred (disabled in v1).
* **Secrets**: Environment variables via Docker secrets; no keys in repo.
* **Encryption**: HTTPS everywhere (TLS) in production.

---

## 7. Optional Integrations

*Defer payments entirely.*

### 7.2 Analytics Integration

* Minimal server logs + optional pageview counters.
* Future: Matomo or PostHog with event names like `resource_edit_saved`, `change_request_submitted`, `bulk_commit`.

---

## 8. Environment Configuration & Deployment

* **Local Setup**

  * Docker services: `web` (Django), `db` (Postgres with `pg_trgm`), `redis` (optional).
  * ENV: `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.

* **Tailwind + daisyUI 5**

  * CSS file:

    ```css
    @import "tailwindcss";
    @plugin "daisyui";
    ```
  * Optional theme config:

    ```css
    @plugin "daisyui" {
      themes: light --default, dark --prefersdark;
    }
    ```

* **CI/CD**

  * GitHub Actions: lint (flake8), tests (pytest), migrations; build/push Docker image; deploy to staging/prod.

* **Monitoring & Logging**

  * Django logging to stdout; structured JSON logs; Sentry optional later.

---

## 9. Testing & Quality Assurance

* **Unit Tests**

  * Serializers: façade mapping, validation errors, JSON Patch application.
  * Extension models: version increments, sensitive overlays, verification events.

* **Integration Tests**

  * `PATCH /api/resource/{id}` with If-Match and version assertions.
  * Draft approval path writes correct HSDS rows.
  * Bulk op commit + undo.

* **End-to-End (Playwright)**

  * Resource inline edit save (happy path + validator errors).
  * Wizard create → draft → approve.
  * Shelf stage/preview/commit/undo.
  * Sensitive-mode redaction visible to Volunteer.

* **Accessibility**

  * axe-playwright: no critical violations on editor, wizard, review queue.

* **Security Tests**

  * CSRF enforced for unsafe methods.
  * Role-based access checks (negative tests).

---

## 10. Edge Cases, Implementation Considerations & Reflection

* **Potential Obstacles**

  * Conflicts during rapid edits; ensure merge chips are clear and non-blocking.
  * Complex HSDS splits (e.g., multiple phones/schedules) — ensure deterministic field paths.

* **Edge-Case Handling**

  * Missing geocode: allow “mailing-only” flag; capture as soft warning.
  * Duplicate creation in wizard: force explicit “Create anyway” confirmation.

* **Technical Constraints**

  * No HSDS schema changes; all overlays external.
  * No map UI; background geocode only.

* **Scalability**

  * JSONB patches and extension tables scale horizontally; pg_trgm indexes for quick search.

* **Testing Focus**

  * JSON Patch idempotency; inverse patch generation for undo.
  * ETag/version drift across tabs and shelf ops.

* **Critical Questions**

  * Geocode provider selection and SLA (defer).
  * Notification channels for review approvals (defer).

* **Approach Suitability**

  * Preserves HSDS purity; adds velocity via overlays; reversible, auditable changes.

* **Assumptions to Challenge**

  * Field-path granularity is sufficient for all conflicts.
  * Volunteers comfortable with shelf mental model.

* **Exceptional Outcome**

  * Volunteers can fix a phone number across siblings in under 20 seconds with full audit and undo.

---

## 11. Summary & Next Steps

* **Recap**

  * Composite Resource façade over HSDS with extension tables for drafts, change-requests, versions, shelves, sensitive overlays.
  * Real-time validation; field-level history/freshness; shelf-based bulk with diff and undo.
  * HTMX + Tailwind v4 + **daisyUI v5** with explicit component mapping.

* **Open Questions**

  * Choose GeocodeService provider and quota.
  * Define final review UI polish (filters, grouping).
  * Future: notifications (email/Slack), exports.

* **Future Enhancements**

  * Editor workload dashboards; reminderless worklists evolution.
  * PII lint for notes; attachment support.
  * Dark theme tuning and custom daisyUI theme.

---
