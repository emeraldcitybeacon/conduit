# Implementation Plan

## Phase 0 — Project wiring & scaffolding

* [ ] Step 0.1: Add new apps and settings

  * **Task**: Create `hsds_ext`, `resources`, and `pulse` apps; register in settings; wire URLs. Create base templates/layout for Pulse. Ensure `django-components` is enabled and set up a component registry pattern under `src/[app]/components/…`.
  * **Files**:

    * `src/hsds_ext/apps.py`: new app config
    * `src/hsds_ext/__init__.py`: new
    * `src/resources/apps.py`: new
    * `src/resources/__init__.py`: new
    * `src/pulse/apps.py`: new
    * `src/pulse/__init__.py`: new
    * `src/project/settings.py`: add apps, `django_components`, DRF defaults, HTMX middleware if used
    * `src/project/urls.py`: include `pulse.urls` and `resources.urls`
    * `src/pulse/urls.py`: base routes (`/pulse/…`)
    * `src/resources/urls.py`: base API routes (`/api/…`)
    * `src/pulse/templates/pulse/base.html`: base layout with daisyUI navbar/drawer
  * **Step Dependencies**: None
  * **User Instructions**: Confirm `INSTALLED_APPS` contains `django_components`, `rest_framework`, `hsds_ext`, `resources`, `pulse`. Ensure Tailwind build runs as in your current setup.

* [ ] Step 0.2: Database extension & env sanity

  * **Task**: Enable `pg_trgm` and add a migration to create it if not present. Ensure env vars present (`DATABASE_URL`, `SECRET_KEY`, etc.).
  * **Files**:

    * `src/hsds_ext/migrations/0001_enable_pg_trgm.py`: raw SQL migration for `CREATE EXTENSION IF NOT EXISTS pg_trgm;`
    * `docker-compose.yml`: ensure Postgres 15+ and volumes (if not already)
    * `.env.example`: document required env keys
  * **Step Dependencies**: Step 0.1
  * **User Instructions**: Run `python manage.py migrate` in your dev container.

## Phase 1 — Extension schema (no HSDS changes)

* [ ] Step 1.1: Extension models (verification, versions, overlays)

  * **Task**: Implement `VerificationEvent`, `FieldVersion`, `SensitiveOverlay` models + indexes/uniques exactly as spec; admin stubs.
  * **Files**:

    * `src/hsds_ext/models/verification.py`
    * `src/hsds_ext/models/versions.py`
    * `src/hsds_ext/models/sensitive.py`
    * `src/hsds_ext/admin.py`: register models
    * `src/hsds_ext/migrations/0002_core_ext_tables.py`
  * **Step Dependencies**: Phase 0
  * **User Instructions**: Run migrations.

* [ ] Step 1.2: Extension models (drafts, change-requests, shelves, bulk ops, taxonomy ext)

  * **Task**: Implement `DraftResource`, `ChangeRequest`, `Shelf`, `ShelfMember`, `BulkOperation`, optional `TaxonomyExtension`.
  * **Files**:

    * `src/hsds_ext/models/drafts.py`
    * `src/hsds_ext/models/change_requests.py`
    * `src/hsds_ext/models/shelves.py`
    * `src/hsds_ext/models/bulk_ops.py`
    * `src/hsds_ext/models/taxonomy_ext.py` (optional)
    * `src/hsds_ext/migrations/0003_more_ext_tables.py`
  * **Step Dependencies**: Step 1.1
  * **User Instructions**: Migrate again.

## Phase 2 — Resource façade & serializers

* [ ] Step 2.1: JSON utilities & field-path versioning

  * **Task**: Add helpers for canonical HSDS JSON assembly/splitting, JSON Patch (`jsonpatch`), and field-path version operations.
  * **Files**:

    * `src/resources/utils/json_paths.py`: dot-path helpers (`contacts.phones[0].number`)
    * `src/resources/utils/json_patch.py`: apply/compute/inverse patch
    * `src/resources/utils/etags.py`: compute weak ETags per resource + map of field versions
    * `pyproject.toml`/`requirements.txt`: add `jsonpatch`
  * **Step Dependencies**: Phase 1
  * **User Instructions**: Install deps in your container if not vendored.

* [ ] Step 2.2: Composite ResourceSerializer & façade views

  * **Task**: Implement `ResourceSerializer` (compose/decompose HSDS + overlays + field freshness). Implement `GET /api/resource/{id}` and `PATCH /api/resource/{id}` with `If-Match` and `assert_versions` contract; map auto-publish vs review-required fields.
  * **Files**:

    * `src/resources/serializers/resource.py`
    * `src/resources/views/resource.py` (DRF APIView or ViewSet)
    * `src/resources/urls.py`: add resource routes
    * `src/resources/permissions.py`: Volunteer/Editor/Admin gates
    * `src/resources/exceptions.py`: problem+json handler
    * `src/project/settings.py`: DRF exception handler hook
  * **Step Dependencies**: Step 2.1
  * **User Instructions**: None

## Phase 3 — Pulse shell & django-components foundation

* [ ] Step 3.1: Component base classes & registration

  * **Task**: Set up `django-components` scaffolding, with a pattern to register components at URLs for HTMX (`/pulse/c/<component>`). Include a daisyUI form control wrapper and a diff viewer placeholder.
  * **Files**:

    * `src/pulse/components/ui/__init__.py`
    * `src/pulse/components/ui/form_field.py` + `form_field.html` (label, help, error, daisy `input|select|textarea`)
    * `src/pulse/components/ui/diff.py` + `diff.html` (placeholder)
    * `src/pulse/views/components.py`: component endpoint dispatcher
    * `src/pulse/urls.py`: `path("c/<slug:name>/", …)`
    * `src/pulse/templates/pulse/partials/toast.html` (daisy `toast`)
  * **Step Dependencies**: Phase 2
  * **User Instructions**: None

* [ ] Step 3.2: Unified Resource Pane skeleton (tabs/sections)

  * **Task**: Create the Resource detail page with daisy `navbar`, `tabs`, and stubbed sections. Wire HTMX targets and partial endpoints.
  * **Files**:

    * `src/pulse/templates/pulse/resource/detail.html`
    * `src/pulse/views/resource.py`: HTMX views render sections via façade `GET`
    * `src/pulse/urls.py`: add route `path("r/<uuid:id>/", …)`
    * `src/pulse/components/resource/freshness_badge.py` + `freshness_badge.html`
    * `src/pulse/components/resource/verify_button.py` + `verify_button.html`
  * **Step Dependencies**: Step 3.1
  * **User Instructions**: Navigate to `/pulse/r/<id>` for a known HSDS record.

## Phase 4 — Always-on validation & save/diff flow

* [ ] Step 4.1: Inline edit forms + serializer error mapping

  * **Task**: For Contacts and Hours tabs, implement edit forms that `hx-patch` to façade, show errors via component `validator` hints, and show diff modal before commit.
  * **Files**:

    * `src/pulse/templates/pulse/resource/contacts_tab.html`
    * `src/pulse/templates/pulse/resource/hours_tab.html`
    * `src/pulse/components/ui/validator.py` + `validator.html`
    * `src/pulse/components/ui/modal.py` + `modal.html` (daisy `modal`)
    * `src/pulse/static/pulse/js/keys.js` (⌘S handler → open diff modal / submit)
  * **Step Dependencies**: Phase 3
  * **User Instructions**: Test edits to phones/hours; confirm errors appear inline.

* [ ] Step 4.2: Provenance & verification events

  * **Task**: Add verify buttons (`Called`, `Website`, `On-site`) writing `VerificationEvent`; freshness chips next to labels with tooltips/timeline popover.
  * **Files**:

    * `src/resources/views/verify.py`: POST handler
    * `src/resources/urls.py`: add `/api/resource/{id}/verify`
    * `src/pulse/components/resource/freshness_popover.py` + `freshness_popover.html`
    * `src/pulse/templates/pulse/resource/history_panel.html`
  * **Step Dependencies**: Step 4.1

## Phase 5 — Create Wizard & Drafts

* [ ] Step 5.1: Wizard UI (Org → Location → Service)

  * **Task**: daisy `steps` with sibling-prefill banners and validation per step; final diff preview. Saves a `DraftResource`.
  * **Files**:

    * `src/pulse/templates/pulse/wizard/start.html`
    * `src/pulse/templates/pulse/wizard/step_org.html`
    * `src/pulse/templates/pulse/wizard/step_location.html`
    * `src/pulse/templates/pulse/wizard/step_service.html`
    * `src/pulse/views/wizard.py`
    * `src/pulse/urls.py`: add `/pulse/new` routes
    * `src/resources/views/drafts.py`: `POST /api/resource` (create draft), list drafts
  * **Step Dependencies**: Phase 4

* [ ] Step 5.2: Draft approval path

  * **Task**: Implement editor-only approve/reject endpoints that write canonical HSDS via serializers, set draft status, and log versions/provenance.
  * **Files**:

    * `src/resources/views/drafts_review.py`: approve/reject
    * `src/resources/urls.py`: `/api/drafts/{id}/approve|reject`
    * `src/pulse/templates/pulse/review/drafts_list.html`
    * `src/pulse/views/review.py`: list/show drafts
  * **Step Dependencies**: Step 5.1

## Phase 6 — Shelf & Bulk Apply

* [ ] Step 6.1: Shelf model UI + add/remove from shelf

  * **Task**: Right-hand `drawer` with list of resources, add/remove controls, plus server endpoints.
  * **Files**:

    * `src/resources/views/shelves.py`: CRUD + add/remove
    * `src/resources/urls.py`: `/api/shelves…`
    * `src/pulse/components/shelf/drawer.py` + `drawer.html`
    * `src/pulse/components/shelf/member_row.py` + `member_row.html`
  * **Step Dependencies**: Phase 5

* [ ] Step 6.2: Stage/preview/commit/undo bulk operations

  * **Task**: Modal to build a patch for phones/hours/etc. Preview table with per-target result and diff; commit + time-limited undo with inverse patches.
  * **Files**:

    * `src/resources/views/bulk_ops.py`: stage, preview, commit, undo
    * `src/resources/urls.py`: `/api/bulk-ops…`
    * `src/pulse/templates/pulse/shelf/stage_form.html`
    * `src/pulse/templates/pulse/shelf/preview.html`
    * `src/pulse/templates/pulse/shelf/commit_result.html`
  * **Step Dependencies**: Step 6.1

## Phase 7 — Dedupe & Merge

* [ ] Step 7.1: Live duplicate hints

  * **Task**: On name/phone/address edits, show toast with candidate duplicates from search endpoint.
  * **Files**:

    * `src/resources/views/search.py`: `/api/search?q=`
    * `src/pulse/components/ui/toast_card.py` + `toast_card.html`
  * **Step Dependencies**: Phase 6

* [ ] Step 7.2: Split-view merge flow

  * **Task**: Two-column comparison, checkbox-per-field; server computes final patch and applies to survivor.
  * **Files**:

    * `src/resources/views/merge.py`: `POST /api/merge`
    * `src/pulse/templates/pulse/merge/split_view.html`
    * `src/pulse/components/merge/conflict_badge.py` + `conflict_badge.html`
  * **Step Dependencies**: Step 7.1

## Phase 8 — Sensitive Mode (review-required)

* [ ] Step 8.1: Sensitive overlay endpoints + UI

  * **Task**: Toggle requires review; on approval, apply `SensitiveOverlay`. Read-time redaction in façade.
  * **Files**:

    * `src/resources/views/sensitive.py`: `PATCH /api/resource/{id}/sensitive`
    * `src/pulse/components/resource/sensitive_banner.py` + `sensitive_banner.html`
    * `src/resources/serializers/resource.py`: redact paths per `visibility_rules`
  * **Step Dependencies**: Phase 7

## Phase 9 — Navigation, Worklists, Quick-open

* [ ] Step 9.1: Sibling switchers + hotkeys

  * **Task**: Add sibling lists (“services at this location/org”) and keyboard shortcuts (`g o`, `g l`, `[`/`]`, `J/K`).
  * **Files**:

    * `src/pulse/components/resource/siblings_nav.py` + `siblings_nav.html`
    * `src/pulse/static/pulse/js/keys.js`: extend bindings
    * `src/resources/views/siblings.py`: helper endpoints if needed
  * **Step Dependencies**: Phase 8

* [ ] Step 9.2: Worklists & ⌘K quick-open

  * **Task**: Ad-hoc, shareable saved searches; ⌘K fuzzy search (pg\_trgm) across name/phone/street/tag.
  * **Files**:

    * `src/resources/views/worklists.py`: CRUD and open-next/prev
    * `src/pulse/components/worklist/picker.py` + `picker.html` (⌘K modal)
    * `src/pulse/templates/pulse/worklists/index.html`
  * **Step Dependencies**: Step 9.1

## Phase 10 — Moderation & Review Queue (review-required fields)

* [ ] Step 10.1: ChangeRequest submission & queue list

  * **Task**: From Resource pane, review-required edits become `ChangeRequest` (stores patch + note). Build reviewer list UI.
  * **Files**:

    * `src/resources/views/change_requests.py`: submit/list
    * `src/pulse/templates/pulse/review/queue.html`
    * `src/pulse/components/review/request_row.py` + `request_row.html`
  * **Step Dependencies**: Phase 9

* [ ] Step 10.2: Approve/reject with human-readable diffs

  * **Task**: Diff panel, apply patch to HSDS upon approval, log versions/provenance.
  * **Files**:

    * `src/resources/views/change_requests_review.py`: approve/reject
    * `src/pulse/templates/pulse/review/detail.html`
    * `src/pulse/components/ui/diff.py` + `diff.html` (upgrade to field-level diffs)
  * **Step Dependencies**: Step 10.1

## Phase 11 — Concurrency & optimistic locking polish

* [ ] Step 11.1: Merge chips & ETag drift handling

  * **Task**: On `412 Precondition Failed` or version mismatch, surface “merge chips” inline; allow re-apply from current value.
  * **Files**:

    * `src/pulse/components/ui/merge_chip.py` + `merge_chip.html`
    * `src/resources/views/resource.py`: return mismatch metadata & latest etags
    * `src/pulse/templates/pulse/resource/_field_block.html`: integrate chip
  * **Step Dependencies**: Phase 10

## Phase 12 — Data Health tiles (lite)

* [ ] Step 12.1: Tiles & filters

  * **Task**: In-app dashboard showing “No phone,” “No hours,” “Not geocoded,” “Stale fields,” with links to worklists.
  * **Files**:

    * `src/resources/views/health.py`: simple queries
    * `src/pulse/templates/pulse/health/index.html`
    * `src/pulse/components/health/stat_tile.py` + `stat_tile.html` (daisy `stat`)
  * **Step Dependencies**: Phase 11

## Phase 13 — Keyboard overlay & checklist

* [ ] Step 13.1: Keyboard overlay

  * **Task**: `?` opens `modal` with key bindings rendered from a small JSON registry (scope-aware).
  * **Files**:

    * `src/pulse/components/ui/key_overlay.py` + `key_overlay.html`
    * `src/pulse/static/pulse/js/keys.js`: overlay trigger
    * `src/pulse/static/pulse/keys.json`: registry
  * **Step Dependencies**: Phase 12

* [ ] Step 13.2: Verification checklist

  * **Task**: Inline `checkbox` list that writes provenance on check (Phone/Hours/Intake).
  * **Files**:

    * `src/pulse/components/resource/verify_checklist.py` + `verify_checklist.html`
    * `src/resources/views/verify.py`: extend to accept checklist item events
  * **Step Dependencies**: Step 13.1

## Phase 14 — Permissions, security, accessibility

* [ ] Step 14.1: Roles & gates

  * **Task**: Add simple role enum (Volunteer/Editor/Admin) and view/serializer permission checks. Add CSRF/HTMX headers utilities.
  * **Files**:

    * `src/core/models/users.py` (or extend existing): `role` field
    * `src/resources/permissions.py`: finalize gates per field-level publish rules
    * `src/pulse/templates/pulse/base.html`: ensure CSRF token + HX headers
  * **Step Dependencies**: Phase 13
  * **User Instructions**: If you don’t already have a custom user model, migrate early and set `AUTH_USER_MODEL`.

* [ ] Step 14.2: Accessibility & ARIA pass

  * **Task**: ARIA roles on tabs/modals/steps, labelled inputs, focus traps; axe checks.
  * **Files**:

    * `src/pulse/templates/pulse/resource/*.html`: ARIA updates
    * `tests/a11y/test_accessibility.py`: basic axe/Playwright checks
  * **Step Dependencies**: Step 14.1

## Phase 15 — Tests, CI, and deployment

* [ ] Step 15.1: Unit & integration tests

  * **Task**: Serializer tests (façade mapping), extension tables behavior, bulk ops commit/undo, draft approval path, ETag/version assertions.
  * **Files**:

    * `tests/resources/test_resource_serializer.py`
    * `tests/resources/test_patch_and_versions.py`
    * `tests/resources/test_drafts.py`
    * `tests/resources/test_bulk_ops.py`
    * `tests/resources/test_sensitive.py`
  * **Step Dependencies**: Phase 14

* [ ] Step 15.2: E2E Playwright flows

  * **Task**: Edit-save, wizard create→approve, shelf stage→preview→commit→undo, sensitive view as Volunteer.
  * **Files**:

    * `e2e/pulse/specs/resource_edit.spec.ts`
    * `e2e/pulse/specs/wizard_draft_approve.spec.ts`
    * `e2e/pulse/specs/shelf_bulk.spec.ts`
    * `e2e/pulse/specs/sensitive_mode.spec.ts`
  * **Step Dependencies**: Step 15.1

* [ ] Step 15.3: CI/CD wiring

  * **Task**: GitHub Actions workflow for lint/tests/migrations; build/push Docker image; deploy staging.
  * **Files**:

    * `.github/workflows/ci.yml`
    * `Dockerfile` (finalize)
    * `docker-compose.yml` (staging profile if needed)
  * **Step Dependencies**: Step 15.2
  * **User Instructions**: Add secrets in your CI host, set container registry, and staging host configuration.

---

## Summary

You’ll implement Pulse as a volunteer-focused editor that *wraps* HSDS with an extension schema: drafts, change-requests, field versions, verification events, sensitive overlays, shelves, and bulk ops. The façade serializer keeps validation centralized; HTMX + `django-components` produce fast, daisyUI-native partials. ETags + field-level versions give safe, optimistic concurrency; JSON Patch enables review-required diffs and undo. The plan proceeds in small, shippable steps—schema → façade → UI shell → wizard → shelves/bulk → freshness/history → merge → sensitive → navigation/worklists → review queue → concurrency polish → health tiles → keyboard overlay → security/accessibility → tests/CI—so you can verify correctness and performance at each stage and keep the entire apparatus legible and trustworthy.
