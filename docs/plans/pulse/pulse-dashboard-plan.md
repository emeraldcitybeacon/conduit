# Implementation Plan

## A. Bootstrap & App Wiring

* [ ] Step A1: Ensure `pulse` app exists and is installed

  * **Task**: Create `src/pulse/` scaffold if missing; add to `INSTALLED_APPS`; add base `urls.py` include; create empty `templates` and `components` dirs.
  * **Files**:

    * `src/pulse/__init__.py`: new
    * `src/pulse/apps.py`: `PulseConfig`
    * `src/pulse/urls.py`: include API and dashboard routes
    * `src/project/settings.py`: add `"pulse"` to `INSTALLED_APPS`
    * `src/project/urls.py`: `path("pulse/", include("pulse.urls"))`
    * `src/pulse/templates/pulse/dashboard.html`: placeholder template
    * `src/pulse/components/__init__.py`: new
  * **Step Dependencies**: None
  * **User Instructions**: If the project root/app names differ, adapt paths accordingly.

* [ ] Step A2: Base navigation entry & access control

  * **Task**: Add a nav link (visible to authenticated users) to `/pulse/dashboard/`; enforce login-required on all Pulse views.
  * **Files**:

    * `src/pulse/urls.py`: route `path("dashboard/", views.dashboard, name="pulse-dashboard")`
    * `src/pulse/views.py`: `dashboard` view with `@login_required`
    * `src/base/templates/_nav.html` (or equivalent): add “Pulse” link (feature flag safe)
  * **Step Dependencies**: A1
  * **User Instructions**: Ensure your base layout location; adjust include path if different.

---

## B. Data Model & Migrations

* [ ] Step B1: Define Pulse models

  * **Task**: Implement models with statuses, ETag fields, and basic constraints.
  * **Files**:

    * `src/pulse/models.py`: add `DraftResource`, `ChangeRequest`, `MergeDraft`, `DuplicateFlag`, `ReviewAction` (+ timestamp mixin)
  * **Step Dependencies**: A1
  * **User Instructions**: None

* [ ] Step B2: Initial migrations & pg\_trgm (optional)

  * **Task**: Create migrations; optionally enable `pg_trgm` for search.
  * **Files**:

    * `src/pulse/migrations/0001_initial.py`: auto-generated
    * `src/pulse/migrations/0002_enable_pg_trgm.py`: `RunSQL("CREATE EXTENSION IF NOT EXISTS pg_trgm;")`
  * **Step Dependencies**: B1
  * **User Instructions**: Run `python manage.py makemigrations pulse && python manage.py migrate`

* [ ] Step B3: DB indexes & constraints

  * **Task**: Add composite indexes and unique constraints per spec.
  * **Files**:

    * `src/pulse/migrations/0003_indexes.py`: `indexes=[models.Index(...)]`; unique together for MergeDraft `(survivor_id, contender_id)`
  * **Step Dependencies**: B2
  * **User Instructions**: Run `python manage.py migrate`

---

## C. Permissions & Roles

* [ ] Step C1: Permissions module and checks

  * **Task**: Define helpers to check Editor vs Volunteer.
  * **Files**:

    * `src/pulse/permissions.py`: `is_editor(user)`, `is_volunteer(user)` based on Groups/Perms
  * **Step Dependencies**: A1
  * **User Instructions**: None

* [ ] Step C2: Idempotent role setup command

  * **Task**: Management command to create “Editors” and “Volunteers” groups with model permissions.
  * **Files**:

    * `src/pulse/management/commands/pulse_setup_roles.py`: creates groups & assigns perms
    * `src/pulse/management/__init__.py`: new
    * `src/pulse/management/commands/__init__.py`: new
  * **Step Dependencies**: C1
  * **User Instructions**: Run `python manage.py pulse_setup_roles`; assign users to groups via Django admin or shell.

---

## D. Service Layer

* [ ] Step D1: HSDS adapter scaffold

  * **Task**: Abstract canonical HSDS R/W with ETag support.
  * **Files**:

    * `src/pulse/services/hsds_adapter.py`: `hsds_read(kind,id)`, `hsds_write(kind,id,payload,if_match)`, `hsds_merge(kind,survivor,contender,payload,if_match)`
    * `src/pulse/services/__init__.py`: new
  * **Step Dependencies**: B1
  * **User Instructions**: Add env vars if needed (e.g., `HSDS_BASE_URL`, tokens) in `.env` and settings.

* [ ] Step D2: Merge logic & Diff helpers

  * **Task**: Provide utilities to resolve field maps and feed Diff component.
  * **Files**:

    * `src/pulse/services/merge.py`: `resolve(survivor, contender, field_map)`; validation of survivor selection
    * `src/pulse/services/diff.py`: normalize current/proposed payloads for component
  * **Step Dependencies**: D1
  * **User Instructions**: None

* [ ] Step D3: Search service

  * **Task**: Text search & stale/suspect highlighting.
  * **Files**:

    * `src/pulse/services/search.py`: functions for `find(q, filters)` and heuristics flags (e.g., phone not E.164)
  * **Step Dependencies**: B2
  * **User Instructions**: None

---

## E. API: Serializers & URLs

* [ ] Step E1: Serializers

  * **Task**: Represent models and input payloads for HTMX/DRF views.
  * **Files**:

    * `src/pulse/api/serializers.py`: serializers for `ChangeRequest`, `MergeDraft`, `DraftResource`, DTOs for counters and search results
  * **Step Dependencies**: B1
  * **User Instructions**: None

* [ ] Step E2: API URL map

  * **Task**: Wire API endpoints per spec.
  * **Files**:

    * `src/pulse/api/urls.py`: routes for review and workbench endpoints
    * `src/pulse/urls.py`: `include("pulse.api.urls", namespace="pulse-api")`
  * **Step Dependencies**: E1, A1
  * **User Instructions**: None

---

## F. Views: Review Hub (Editors-only)

* [ ] Step F1: Counters & Jump-In endpoints

  * **Task**: Implement counters JSON and jump-in fragment loader.
  * **Files**:

    * `src/pulse/api/views.py`: `review_counters`, `review_jump_in`
    * `src/pulse/templates/pulse/_review_counters.html`: HTMX fragment
    * `src/pulse/templates/pulse/_review_item_shell.html`: container swapped by Jump-In
  * **Step Dependencies**: E2, C1
  * **User Instructions**: None

* [ ] Step F2: Change Request list & detail

  * **Task**: List with filters/chips; detail with Diff; approve/reject.
  * **Files**:

    * `src/pulse/api/views.py`: `cr_list`, `cr_detail`, `cr_approve`, `cr_reject`
    * `src/pulse/templates/pulse/_cr_list.html`
    * `src/pulse/templates/pulse/_cr_detail.html` (uses Diff component include)
  * **Step Dependencies**: F1, D1, D2
  * **User Instructions**: None

* [ ] Step F3: Merge Drafts list & detail

  * **Task**: List queue; detail split view; approve/reject.
  * **Files**:

    * `src/pulse/api/views.py`: `merge_list`, `merge_detail`, `merge_approve`, `merge_reject`
    * `src/pulse/templates/pulse/_merge_list.html`
    * `src/pulse/templates/pulse/_merge_detail.html`
  * **Step Dependencies**: F1, D1, D2
  * **User Instructions**: None

---

## G. Views: Workbench (Volunteers & Editors)

* [ ] Step G1: Draft create/edit/submit

  * **Task**: New draft form (kind switch), save-as-draft, submit-to-pending; “My Drafts” list.
  * **Files**:

    * `src/pulse/api/views.py`: `draft_new`, `draft_save`, `draft_submit`, `my_drafts`
    * `src/pulse/templates/pulse/_draft_form.html`
    * `src/pulse/templates/pulse/_my_drafts.html`
  * **Step Dependencies**: E2, B1
  * **User Instructions**: None

* [ ] Step G2: Inline edit → Change Request endpoint (server-side patch)

  * **Task**: Endpoint to accept inline-edit payloads, generate RFC6902, render Diff for confirm, then create CR.
  * **Files**:

    * `src/pulse/api/views.py`: `cr_from_inline_edit`, `cr_confirm_create`
    * `src/pulse/templates/pulse/_cr_preview_diff.html`
  * **Step Dependencies**: D2, E2
  * **User Instructions**: Point existing inline-edit UIs to this endpoint for submit.

* [ ] Step G3: Duplicates (flag + create merge draft)

  * **Task**: Flag dupes and optionally open a pre-filled MergeDraft.
  * **Files**:

    * `src/pulse/api/views.py`: `dup_flag`, `merge_draft_create`
    * `src/pulse/templates/pulse/_dup_flag_success.html`
  * **Step Dependencies**: B1, E2
  * **User Instructions**: None

* [ ] Step G4: Find & Improve

  * **Task**: Search endpoint and results list with stale/suspect highlights and quick-fix affordances (open CR flow).
  * **Files**:

    * `src/pulse/api/views.py`: `find`
    * `src/pulse/templates/pulse/_find_results.html`
  * **Step Dependencies**: D3, E2
  * **User Instructions**: None

---

## H. Dashboard Page & Components

* [ ] Step H1: Dashboard template and section gating

  * **Task**: Compose the two stacked sections; hide Editor Review Hub for non-editors.
  * **Files**:

    * `src/pulse/templates/pulse/dashboard.html`: top/bottom sections; HTMX `hx-get` to load fragments
    * `src/pulse/views.py`: `dashboard` populates initial context (is\_editor flag)
  * **Step Dependencies**: F1–F3, G1–G4
  * **User Instructions**: None

* [ ] Step H2: Counter auto-refresh & Jump-In UX

  * **Task**: Add `hx-trigger="load, revealed"` for counters; wire “Jump In” button to choose `cr` first then `merge` fallback; provide skip/next controls.
  * **Files**:

    * `src/pulse/templates/pulse/_review_counters.html`
    * `src/pulse/templates/pulse/_review_item_shell.html`
    * `src/pulse/static/pulse/jumpin.js` (optional tiny helper, or inline `hx-vals`)
  * **Step Dependencies**: H1
  * **User Instructions**: None

* [ ] Step H3: Diff component wrapper include

  * **Task**: Create a tiny include that adapts our Diff data to the existing Diff component API.
  * **Files**:

    * `src/pulse/components/review/diff_wrapper.py` (django-components registration)
    * `src/pulse/components/review/diff_wrapper.html`
  * **Step Dependencies**: D2
  * **User Instructions**: If your Diff component has a different registration path, adjust import.

---

## I. ETag Conflict UX & Errors

* [ ] Step I1: Standardize API errors & 409 flow

  * **Task**: Add a small exception + handler and a reusable conflict banner partial with “Refresh & Re-apply”.
  * **Files**:

    * `src/pulse/exceptions.py`: `APIError`, `ETagConflict`
    * `src/pulse/api/views.py`: use exceptions; map to 409/422/403
    * `src/pulse/templates/pulse/_conflict_banner.html`
  * **Step Dependencies**: F2–F3, G2
  * **User Instructions**: None

---

## J. Security & Access Control

* [ ] Step J1: Decorators and per-endpoint checks

  * **Task**: Enforce editor-only routes for Review Hub; volunteers for Workbench.
  * **Files**:

    * `src/pulse/permissions.py`: decorators `@editor_required`, `@volunteer_or_editor`
    * `src/pulse/api/views.py`: apply decorators
  * **Step Dependencies**: C1, F/G
  * **User Instructions**: None

* [ ] Step J2: CSRF/HTMX setup sanity

  * **Task**: Ensure CSRF tokens posted on HTMX forms; add `hx-headers` snippet to base template if needed.
  * **Files**:

    * `src/templates/base.html` (or equivalent): add CSRF header script
    * `src/pulse/templates/pulse/_form_base.html`: include `{% csrf_token %}`
  * **Step Dependencies**: H1
  * **User Instructions**: Verify your base template path.

---

## K. Styling & Accessibility

* [ ] Step K1: DaisyUI components & focus states

  * **Task**: Apply daisyUI classes to tables, buttons, tabs, modals, badges; ensure clear focus outlines.
  * **Files**:

    * `src/pulse/templates/pulse/_cr_list.html`
    * `src/pulse/templates/pulse/_cr_detail.html`
    * `src/pulse/templates/pulse/_merge_list.html`
    * `src/pulse/templates/pulse/_merge_detail.html`
    * `src/pulse/templates/pulse/_draft_form.html`
  * **Step Dependencies**: F/G
  * **User Instructions**: None

* [ ] Step K2: ARIA labels & error bindings

  * **Task**: Add `aria-labelledby`, `aria-describedby` links for form errors and modal focus traps.
  * **Files**:

    * `src/pulse/templates/pulse/_draft_form.html`
    * `src/pulse/templates/pulse/_cr_detail.html`
    * `src/pulse/templates/pulse/_merge_detail.html`
  * **Step Dependencies**: K1
  * **User Instructions**: None

---

## L. Tests

* [ ] Step L1: Unit tests (services & models)

  * **Task**: Validate merge resolution, diff prep, HSDS adapter conflict handling; status transitions; constraints.
  * **Files**:

    * `src/pulse/tests/test_services_merge.py`
    * `src/pulse/tests/test_services_diff.py`
    * `src/pulse/tests/test_services_hsds_adapter.py`
    * `src/pulse/tests/test_models.py`
  * **Step Dependencies**: D1–D3, B1–B3
  * **User Instructions**: Run `pytest -q`

* [ ] Step L2: Integration tests (endpoints)

  * **Task**: Approve CR happy path + conflict; approve MergeDraft; Draft create/submit; CR from inline edit; permission gates.
  * **Files**:

    * `src/pulse/tests/test_api_review_cr.py`
    * `src/pulse/tests/test_api_review_merge.py`
    * `src/pulse/tests/test_api_workbench_drafts.py`
    * `src/pulse/tests/test_api_workbench_cr_inline.py`
    * `src/pulse/tests/test_permissions.py`
  * **Step Dependencies**: F, G, J
  * **User Instructions**: Run `pytest -q`

* [ ] Step L3: E2E tests (Playwright)

  * **Task**: Editor: Dashboard → Jump In → approve; Volunteer: Create draft → submit → My Drafts.
  * **Files**:

    * `e2e/pulse/editor_jumpin.spec.ts`
    * `e2e/pulse/volunteer_draft.spec.ts`
    * `playwright.config.ts`
  * **Step Dependencies**: H (UI complete)
  * **User Instructions**: `npx playwright install && npx playwright test`

* [ ] Step L4: Accessibility checks

  * **Task**: Add axe checks for dashboard, CR detail, merge detail, draft form.
  * **Files**:

    * `e2e/pulse/a11y.spec.ts` (axe-playwright)
  * **Step Dependencies**: H
  * **User Instructions**: Ensure `@axe-core/playwright` installed.

---

## M. DevOps & CI

* [ ] Step M1: Env configuration

  * **Task**: Add HSDS adapter env vars and defaults.
  * **Files**:

    * `.env.example`: `HSDS_BASE_URL=`, `HSDS_TOKEN=`
    * `src/project/settings.py`: read env vars
  * **Step Dependencies**: D1
  * **User Instructions**: Update real values in `.env`

* [ ] Step M2: GitHub Actions CI

  * **Task**: Lint, test, migrate check, build.
  * **Files**:

    * `.github/workflows/ci.yml`: run `pytest`, `python manage.py makemigrations --check`
  * **Step Dependencies**: L1–L2
  * **User Instructions**: None

* [ ] Step M3: Deploy pipeline

  * **Task**: Add container build or platform config; collectstatic; run migrations on deploy.
  * **Files**:

    * `Dockerfile` (if not present or needs updates)
    * `render.yaml` / `fly.toml` (choose your host)
    * `src/project/wsgi.py` (verify)
  * **Step Dependencies**: M2
  * **User Instructions**: Configure secrets (DB URL, HSDS creds) on your host.

---

## N. Final Fit & Polish

* [ ] Step N1: Metrics-lite & My Items badges

  * **Task**: Add personal statuses (My Drafts counts) to Workbench header; keep global counters minimal.
  * **Files**:

    * `src/pulse/templates/pulse/_my_drafts.html`
    * `src/pulse/templates/pulse/_workbench_header.html` (new)
    * `src/pulse/api/views.py`: counts query
  * **Step Dependencies**: G1
  * **User Instructions**: None

* [ ] Step N2: Content & copy pass

  * **Task**: Ensure labels, error text, and tooltips are direct and jargon-free.
  * **Files**:

    * `src/pulse/templates/pulse/*.html` (copy tweaks)
  * **Step Dependencies**: H, K
  * **User Instructions**: None

* [ ] Step N3: Smoke checklist & release notes

  * **Task**: Create a short checklist and CHANGELOG entry for v1.
  * **Files**:

    * `docs/pulse-smoke-checklist.md`
    * `CHANGELOG.md`
  * **Step Dependencies**: All prior
  * **User Instructions**: Review, tag a release.

---

### Summary

This plan stands up the Pulse Dashboard with a clear separation of concerns: thin DRF views, a robust `services/` layer for HSDS calls and merge logic, and HTMX-powered fragments for fast, accessible UX. We implement models, endpoints, and templates for both Editor Review Hub and Workbench, wire ETag conflict handling, and add a minimal permissions model that mirrors your editor/volunteer split. Tests span unit, integration, and E2E, with accessibility checks baked in. CI ensures migrations don’t drift and that core flows remain stable.

Key complexities: integrating the existing Diff component (solved via a wrapper include) and honoring ETag across CR/merge writes (handled in `hsds_adapter` with 409 UX). Future add-ons like notifications, batch approvals, undo windows, and HSDS stats can sit atop this foundation without rework.
