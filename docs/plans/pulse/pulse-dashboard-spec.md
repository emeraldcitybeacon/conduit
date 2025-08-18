# Pulse Dashboard (Editors & Volunteers) Project Specification

---

## 1. Planning & Discovery

### 1.1 Core Purpose & Success

* **Mission Statement**: Enable editors and volunteers to rapidly improve HSDS data via a focused dashboard that streamlines change requests, merge drafts, and draft creation.
* **Core Purpose & Goals**: Deliver the fastest path from intent → approved change/merge with minimal ceremony; reuse existing Diff and ETag to prevent data clobber.
* **Success Indicators**:
  - Time-to-approve median decreases.
  - Approvals/day and merges/day increase (without increased conflicts).
  - Conflict rate handled gracefully (≥95% resolved on first retry).
* **Experience Qualities**: Fast, accessible, un-fancy.

### 1.2 Project Classification & Approach

* **Complexity Level**: Complex App (but with lean v1 scope).
* **Primary User Activity**: Acting (reviewing/approving) and Creating (drafts/CRs).
* **Primary Use Cases**:
  - Editor: open dashboard → Jump In → approve/reject change or merge draft.
  - Volunteer: create draft / make inline edit → submit → track status.
  - Any user: find a record → fix high-signal fields quickly.

### 1.3 Feature-Selection Rationale

* **Core Problem**: Approval friction and context-switching slow data improvement.
* **User Context**: Short sessions, task-focused; desktop-first but responsive.
* **Critical Path**: Dashboard → Jump In → Diff → Approve/Reject.
* **Key Moments**:
  1. Drift warning with one-click resolve/retry.
  2. Merge survivor choice with field-level keeps.
  3. Quick-create draft with smart helpers (phone/url/hours).

### 1.4 High-Level Architecture Overview

* **Client**: Server-rendered HTML (Django templates + django-components) enhanced with HTMX.
* **Server**: Django app `pulse` (views/serializers/services); DRF for JSON endpoints backing HTMX fragments.
* **Database**: PostgreSQL for Pulse models; canonical HSDS lives in its own app/schema.
* **Third-party**: None for v1 (analytics/notifications deferred).

### 1.5 Essential Features

* **Editor Review Hub**
  - Counters + “Jump In”; CR review; Merge Draft review.
* **Workbench**
  - Create Draft; Inline edits → CR; Duplicates → Merge Draft; Find & Improve.
* **Validation**
  - Unit/integration tests for approval flows; E2E happy-path for Jump In; accessibility checks.

---

## 2. System Architecture & Technology

### 2.1 Tech Stack

* **Languages & Frameworks**: Python 3.12+, Django 5.x, DRF, HTMX, TailwindCSS, daisyUI, django-components.
* **Libraries**: python-json-patch (for RFC6902), django-filter, psycopg2-binary, whitenoise (static), pytest + pytest-django, Playwright (E2E).
* **Database**: PostgreSQL 14+ (UUID PKs).
* **DevOps & Hosting**: Docker-based dev; Render/Fly/Heroku-style deploy; Nginx/Gunicorn.
* **CI/CD**: GitHub Actions (lint, test, migrate, deploy).

### 2.2 Project Structure

```

src/
pulse/
components/
review/       # Diff wrapper, CR row, Merge row, counters
workbench/    # Draft form, quick-edit controls, search results
templates/pulse/
dashboard.html
*review**.html
*workbench**.html
api/
**init**.py
serializers.py
views.py
urls.py
services/
hsds\_adapter.py   # commit CRs/merges into canonical; ETag handling
diff.py           # helpers to feed existing Diff component
merge.py          # merge logic, survivor/field rules
search.py         # fast search w/ highlights
models.py
urls.py
permissions.py
tests/

````

* **Naming**: snake_case for Python, kebab-case for HTMX fragment names, BEM-ish utility classes handled by Tailwind.

### 2.3 Component Architecture

#### Server / Backend

* **Domain Objects**:
  - `DraftResource`
  - `ChangeRequest` (RFC6902)
  - `MergeDraft`
  - `DuplicateFlag`
  - `ReviewAction` (audit)
* **Error Boundaries**:
  - Central `APIError` mapped to JSON (status/message/code).
  - 409 Conflict for ETag drift; 422 for validation; 403 for perms.

#### Client / Frontend

* **State Management**: Server state via HTMX swaps; minimal client JS.
* **Routing**: `/pulse/dashboard/` main; fragments loaded via `hx-get` to `/pulse/api/...`.
* **Types**: Not TypeScript; rely on typed serializers and clear JSON contracts.

### 2.4 Data Flow & Real-Time

* **Lifecycle**: User action (HTMX) → DRF view → DB change or canonical write via `hsds_adapter` → HTML/JSON fragment → swap.
* **State Sync**: After approve/reject, update counters and load next item (Jump In).
* **Real-Time**: None in v1 (no websockets).

---

## 3. Database & Server Logic

### 3.1 Database Schema (Pulse)

**Common**
- `id UUID PK`
- `created_at`, `updated_at` (indexes)
- `created_by FK auth.User`
- `status ENUM`: `draft | pending | changes_requested | approved | rejected` (indexed)

**DraftResource**
- `target_kind ENUM('organization','location','service')`
- `target_hsds_id UUID NULL` (when editing existing, else null)
- `payload JSONB` (proposed full/partial HSDS object)
- `note TEXT NULL`

**ChangeRequest**
- `target_kind ENUM('organization','location','service')`
- `target_hsds_id UUID NOT NULL`
- `patch JSONB` (RFC6902 list)
- `base_etag TEXT NOT NULL` (last seen)
- `note TEXT NULL`

**MergeDraft**
- `survivor_kind ENUM('organization','location','service')`
- `survivor_id UUID NOT NULL`
- `contender_id UUID NOT NULL`
- `field_map JSONB` (per-field keep/override decisions)
- `base_etag_survivor TEXT NOT NULL`
- `base_etag_contender TEXT NOT NULL`

**DuplicateFlag**
- `kind ENUM('organization','location','service')`
- `a_id UUID NOT NULL`
- `b_id UUID NOT NULL`
- `confidence NUMERIC(3,2)` (0–1)
- `comment TEXT NULL`
- `flagged_by FK auth.User`

**ReviewAction**
- `subject_type ENUM('change_request','merge_draft','draft_resource')`
- `subject_id UUID`
- `action ENUM('approved','rejected','edited_then_approved')`
- `actor FK auth.User`
- `metadata JSONB` (e.g., survivor_id, merged_ids)
- `created_at`

**Indexes**
- `(status, created_at)`
- `(target_kind, target_hsds_id)`
- `(survivor_id, contender_id)` with unique constraint in `MergeDraft`

### 3.2 Server Actions

#### Endpoints (HTMX/DRF)

- `GET  /pulse/dashboard/` → main page
- `GET  /pulse/api/review/counters` → `{change_requests_pending:int, merge_drafts_pending:int}`
- `GET  /pulse/api/review/jump-in?type=cr|merge` → returns next item fragment
- `GET  /pulse/api/review/change-requests` (filters: type/org/location/service/q)
- `GET  /pulse/api/review/change-requests/{id}` → CR detail fragment + Diff
- `POST /pulse/api/review/change-requests/{id}/approve` → commits via `hsds_adapter`
- `POST /pulse/api/review/change-requests/{id}/reject` → note required
- `GET  /pulse/api/review/merge-drafts` → list
- `GET  /pulse/api/review/merge-drafts/{id}` → merge detail fragment
- `POST /pulse/api/review/merge-drafts/{id}/approve`
- `POST /pulse/api/review/merge-drafts/{id}/reject`

- `GET  /pulse/api/workbench/my-drafts`
- `GET  /pulse/api/workbench/draft/new?kind=organization|location|service`
- `POST /pulse/api/workbench/draft` → create/update draft
- `POST /pulse/api/workbench/draft/{id}/submit`
- `GET  /pulse/api/workbench/find?q=...&filters=...`
- `POST /pulse/api/workbench/cr` → create CR from inline edit
- `POST /pulse/api/workbench/dup/flag` → create DuplicateFlag
- `POST /pulse/api/workbench/merge-draft` → create MergeDraft from volunteer

#### ORM/Service Examples (sketch)

```python
# services/hsds_adapter.py
def apply_change_request(cr: ChangeRequest, editor: User) -> AppliedResult:
    current, etag = hsds_read(cr.target_kind, cr.target_hsds_id)
    if etag != cr.base_etag:
        raise ETagConflict()
    proposed = jsonpatch.apply_patch(current, cr.patch, in_place=False)
    new_obj, new_etag = hsds_write(cr.target_kind, cr.target_hsds_id, proposed, if_match=etag)
    return AppliedResult(id=new_obj["id"], etag=new_etag)

def apply_merge(md: MergeDraft, editor: User) -> MergeResult:
    surv, s_etag = hsds_read(md.survivor_kind, md.survivor_id)
    cont, c_etag = hsds_read(md.survivor_kind, md.contender_id)
    if s_etag != md.base_etag_survivor or c_etag != md.base_etag_contender:
        raise ETagConflict()
    merged = merge.resolve(surv, cont, md.field_map)
    result = hsds_merge(md.survivor_kind, survivor=surv, contender=cont, payload=merged, if_match=(s_etag, c_etag))
    return result
````

---

## 4. Feature Specifications

### 4.1 Editor Review Hub

**User Story**: As an editor, I see pending counts and hit “Jump In” to review the next CR or merge draft, approve/reject quickly, and auto-load the next item.

**Implementation**

* **Counters**: `hx-get="/pulse/api/review/counters"` on dashboard load; update after every action.
* **Jump In**: `hx-get="/pulse/api/review/jump-in?type=cr|merge"`; returns fragment with action buttons and the Diff block.
* **CR Review**

  * List: server pagination + filters; chips (phones/hours/urls) as query params.
  * Detail: render current vs proposed via existing Diff component (django-components).
  * Approve: POST → `apply_change_request()`; on success, mark CR approved, write ReviewAction, swap in next item.
  * Reject: POST with note; CR → rejected; ReviewAction saved.
  * Edit then Approve: open modal with fields, update patch, approve.
* **Merge Draft Review**

  * List: pending merges by oldest-first.
  * Detail: split compare; survivor dropdown disabled (must be explicit in creation or set here).
  * Approve: `apply_merge()`; log survivor and merged IDs; ReviewAction saved.

**Edge Cases & Errors**

* 409 ETag conflict → show alert with “Refresh & Re-apply” button that fetches the latest, re-renders Diff, and replays edits if possible.
* Validation errors from canonical serializers → inline field errors mapped onto the panel.

**Accessibility**

* Tabs, tables, modals: ARIA roles, labelled buttons, focus trap in modals.

### 4.2 Workbench

**User Story**: As a volunteer/editor, I can create a draft, make simple inline edits that produce a CR, flag duplicates, and search for records to improve.

**Implementation**

* **Create Draft Resource**

  * Form segmented by kind (org/location/service).
  * Helpers: phone validator, URL checker, hours builder (client-light; server validates).
  * Save as draft; submit sets status → pending.
* **Inline Edits & CRs**

  * Reuse existing inline-edit fields (already present).
  * On submit, construct RFC6902 patch on the server; show Diff; confirm → create CR (pending).
* **Duplicates**

  * Button “Flag duplicate” on record view → `DuplicateFlag`.
  * “Create merge draft” (if permitted) pre-fills field\_map with suggested keeps (survivor defaults to older or higher quality signal).
* **Find & Improve**

  * `/find` uses `search.py` with trigram/ILIKE; stale/suspect highlights driven by simple heuristics (e.g., phone not E.164, URL invalid, hours missing).

**Errors**

* Draft validation returns 422; highlight fields with daisyUI input-error class.
* CR overlap: if an active CR exists on same target/field, warn and allow continue (editor will resolve).

**UX Notes**

* Big primary CTAs: Create Draft, Submit Change.
* “My Drafts” view for volunteers: statuses and links back.

---

## 5. Design System

### 5.1 Visual Tone & Identity

* **Branding & Theme**: Existing Pulse theme; neutral palette; functional UI.
* **Emotional Response**: Competent, quick, trustworthy.
* **Personality**: Pragmatic.

### 5.2–5.7 (Color, Type, Layout, Animations, Components, Consistency)

* **Tailwind + daisyUI**; follow existing tokens.
* Tables, badges, buttons, inputs, modals, tabs, alerts from daisyUI.
* States: hover/focus/disabled/error defined by daisyUI classes.
* Layout: single page, two sections; content width `max-w-7xl`; responsive stacking; minimal motion.

### 5.8 Accessibility & Readability

* WCAG AA; use `aria-*` on tabs/modals; `sr-only` labels; form errors bound via `aria-describedby`.
* Contrast audited on primary/secondary buttons and links.

---

## 6. Security & Compliance

* **Auth**: Django auth; session cookies; CSRF enabled for POST.
* **Permissions**:

  * Volunteers: Workbench endpoints only.
  * Editors: All endpoints; Merge approval restricted to editors.
* **Transport**: HTTPS everywhere.
* **Threats & Mitigations**:

  * CSRF → built-in + double-submit for HTMX forms.
  * Insecure direct object reference → check permissions on every target ID.
  * Race conditions → ETag/If-Match on canonical writes; DB transactions around status updates.
* **Audit**: `ReviewAction` logs with actor/time/subject; admin-only read.

---

## 7. Optional Integrations

*None in v1.* (Notifications/analytics deferred.)

---

## 8. Environment Configuration & Deployment

* **Local**: `.env` for DB URL, SECRET\_KEY; `make up` for docker-compose; `./manage.py tailwind start` if applicable.
* **Staging/Prod**: Separate DBs; DEBUG off; secure cookies; static via WhiteNoise/CDN.
* **CI/CD**: GitHub Actions → run tests, `makemigrations --check`, deploy on main.
* **Monitoring/Logging**: Django logging to stdout;  structured JSON logs; optional Sentry hook.

---

## 9. Testing & Quality Assurance

* **Unit**:

  * Services: `hsds_adapter`, `merge`, `diff` helpers.
  * Models: status transitions; unique constraints (MergeDraft pairs).
* **Integration**:

  * Approve CR happy-path + ETag conflict.
  * Approve MergeDraft with survivor mapping.
  * Draft create/submit and CR create from inline edit.
* **E2E (Playwright)**:

  * Editor: Dashboard → Jump In → approve → next item loads.
  * Volunteer: Create draft → submit → appears in My Drafts.
* **Performance/Security**:

  * Simple load: counters and list endpoints under 200ms P95 on staging data.
  * Bandit/pip-audit; basic OWASP checklist pass.
* **Accessibility**:

  * axe checks on dashboard, CR detail, merge detail, draft form.

---

## 10. Edge Cases, Implementation Considerations & Reflection

* **Edge Cases**

  * ETag drift after user loads Diff → 409 then “Refresh & Re-apply.”
  * MergeDraft where contender already merged elsewhere → surface error, mark obsolete.
  * Duplicate flags spam → dedupe unique (a\_id,b\_id) per user/day; soft merge into one queue item.
* **Constraints**

  * Inline-edit fields are “as-is” from current code.
  * No batch approvals; no undo; no notifications.
* **Scalability**

  * Index pending/status; lazy-load detail panels; paginate lists.
* **Testing Focus**

  * Patch application correctness; survivor determinations; permission gates.
* **Approach Fit**

  * Server-rendered HTMX keeps latency low and complexity down; leverages existing components and serializers.

---

## 11. Summary & Next Steps

* **Recap**: This spec defines a two-section Pulse Dashboard with Editor Review Hub (CR + MergeDraft approvals) and Workbench (drafts, inline edits, dupes, search). It specifies models, endpoints, HTMX flows, ETag-aware write paths, diff reuse, and accessibility.
* **Open Questions**:

  * Exact API contract of the existing Diff component (props/context names).
  * Precise list of inline-edit fields currently wired.
  * Canonical HSDS adapter function names and serializer paths.
* **Future Enhancements**:

  * Notifications (in-app), batch approvals, undo window for merges/CRs, analytics, HSDS stats dashboard for 211 imports, automated dedupe suggestions.
