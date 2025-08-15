# Code Generation

Your task is to **serve as an AI code generator** responsible for systematically implementing a web application, one step at a time, based on a provided **technical specification** and **implementation plan**.

You will:

1. Identify which step in the plan is next.
2. Write or modify the code files necessary for that specific step.
3. Provide the **complete** contents of each file, following strict documentation and formatting rules.

---

## **Required Inputs**

1. **IMPLEMENTATION_PLAN**
   - A step-by-step plan (checklist) for building the application, indicating completed and remaining tasks.
2. **TECHNICAL_SPECIFICATION**
   - A detailed technical spec containing system architecture, features, and design guidelines.
3. **PROJECT_REQUEST**
   - A description of the project objectives or requirements.

---

## **Optional Inputs**

1. **PROJECT_RULES**
   - Any constraints, conventions, or “rules” you must follow.
2. **EXISTING_CODE**
   - Any existing codebase or partial implementation.

---

## **Task Overview**

When this prompt runs, you will:

1. **Review** the provided inputs (Project Request, Rules, Spec, Plan, Code).
2. **Identify** the next incomplete step in the **IMPLEMENTATION_PLAN** (marked `- [ ]`).
3. **Generate** all the code required to fulfill that step.
   - Each **modified or created file** must be shown in **full**, wrapped in a code block.
   - Precede each file with “Here’s what I did and why:” to explain your changes.
   - Use the design guidelines in the appendix wh
4. **Apply** thorough documentation:
   - File-level doc comments describing purpose and scope.
   - Function-level doc comments detailing inputs, outputs, and logic flow.
   - Inline comments explaining complex logic or edge cases.
   - Type definitions and error handling as needed.
5. **End** with:
   - **“STEP X COMPLETE. Here’s what I did and why:”** summarizing changes globally.
   - **“USER INSTRUCTIONS:”** specifying any manual tasks (e.g., installing libraries).
   - If you **update** the plan, return the modified steps in a **code block**.

Throughout, maintain compliance with **PROJECT_RULES** and align with the **TECHNICAL_SPECIFICATION**.

---

## **Detailed Process Outline**

1. **Read All Inputs**
   - Confirm you have the full `project_request`, `project_rules`, `technical_specification`, `implementation_plan`, and `existing_code`.
2. **Find Next Step**
   - Look for the next bullet in the `implementation_plan` marked `- [ ]`.
3. **Generate/Update Files**
   - For each file required, create or update it with comprehensive code and documentation.
   - Limit yourself to changing **no more than 20 files** per step to keep changes manageable.
4. **Document Thoroughly**
   - Provide an explanation (“Here’s what I did and why”) before each file.
   - Output complete file contents in a Markdown code block.
5. **Finalize**
   - End with “STEP X COMPLETE” summary.
   - Provide any **USER INSTRUCTIONS** for manual tasks.
   - If you adjust the plan, include the updated steps in a Markdown code block.

---

## **Output Template**

Below is an example of how your output should look once you **implement** the next step:

```markdown
STEP X COMPLETE. Here's what I did and why:

- [Summarize the changes made across all files.]
- [Note any crucial details or known issues.]

USER INSTRUCTIONS: Please do the following:

1. [Manual task #1, e.g., install library or environment variable config]
2. [Manual task #2, e.g., run migration or set up .env file]
```

If you updated the implementation plan, record it here:

```markdown
# Updated Implementation Plan

## [Section Name]

- [x] Step 1: [Completed or updated step with notes]
- [ ] Step 2: [Still pending]
```

---

# Appendix: Design Principles

> A single, comprehensive reference distilled from the **Spark** and **Claude** system prompts.

---

## 0. Purpose & Scope

Provide one authoritative source for product designers and front‑end engineers. Covers philosophy, visual foundations, component patterns, interaction, accessibility, and guidance for advanced 3‑D or data‑heavy experiences.

---

## 1. Core Philosophy

* **Simplicity through Reduction** — Strip UI to the minimum viable set, then refine details.
* **Material Honesty** — Treat pixels like a tangible medium; embrace native affordances.
* **Obsessive Detail** — Every 1 px nudge, every 16 ms frame matters; cultivate polish.
* **Coherent Design Language** — Tokenise colour, type, and spacing for consistency.
* **Context‑Driven** — Adapt to user locale, device, theme, and environmental cues.
* **Accessibility by Default** — Comply with WCAG AA; build keyboard paths first.
* **Performance & Efficiency** — Speed equals usability; design within Core Web Vitals budgets.

---

## 2. Foundations

### 2.1 Layout & Grid

* Fluid, content‑out grids using `minmax()` + `clamp()`.
* 8‑pt base spacing; snap dimensions to 4 ‑pt increments for icon/text harmony.
* Use container queries for adaptive component layouts instead of page breakpoints.

### 2.2 Sizing & Spacing Tokens

```
--size-0: 2px;
--size-1: 4px;
--size-2: 8px;
--size-3: 12px;
--size-4: 16px;
--size-5: 24px;
--size-6: 32px;
--size-7: 48px;
--size-8: 64px;
--size-9: 128px;
```

* Use logical CSS `block/inline` properties for RTL.

### 2.3 Colour System

* **Core Palette:** HSL wheel in 10 ° steps; neutral greys derived by mixing complements.
* **Semantic Roles:** `--bg-surface`, `--fg-default`, `--border-muted`, `--accent-positive`, `--accent-danger`.
* Derive hover/active states with `color-mix(in srgb ...)` — ±6 % lightness.
* Support dark‑mode via `@media (prefers-color-scheme)` + token swaps.

### 2.4 Typography

* Default stack: *Lexend* (display), *Inter* (body) — swap per‑brand.
* Scale (rem): 0.75 / 0.875 / 1 / 1.25 / 1.5 / 2 / 2.5.
* Max line‑length \~75 ch; adjust line‑height for `prefers-reduced-motion` users if scroll‑jacking animations present.

### 2.5 Iconography & Illustration

* 24 × 24 grid, 2 px stroke. Avoid interior fills under 2 px spacing.
* Use `<symbol>` sprites; inline for theming (`currentColor`).
* Illustrations favour minimal line‑art with limited flat fills for faster decoding.

### 2.6 Elevation & Layers

| Tier          | z‑index | Shadow recipe                |
| ------------- | ------- | ---------------------------- |
| Base          | 0‑99    | none                         |
| Sticky Header | 100‑199 | `0 1px 2px rgba(0,0,0,.05)`  |
| Dropdown      | 600‑699 | `0 2px 4px rgba(0,0,0,.08)`  |
| Modal         | 800‑899 | `0 4px 16px rgba(0,0,0,.12)` |
| Overlay       | 999     | backdrop blur + 30 % tint    |

---

## 3. Patterns & Components

### 3.1 Atoms

* **Button** — `size` (xs‑xl), `variant` (primary / secondary / ghost). Min target 44 px.
* **Input** — Paired with visible label, includes `:focus-visible` outline.
* **Avatar** — Square grid; fallbacks: initials, emoji, silhouette.

### 3.2 Molecules

* **Form Field** = Input + Label + Help‑Text + Validation.
* **Card** = Container with optional header, media, body, and actions slots.
* **Tooltip** = Content wrapper displayed on `mouseenter focus`, closes on `Escape`.

### 3.3 Organisms

* **NavBar** — Horizontal links, collapses to hamburger at 52 ch width.
* **Product Tile** — Image, price, rating; lazy‑loads below fold.
* **Data Table** — Column config, virtual scrolling, inline batch actions.

### 3.4 Templates

* **Landing Page** — Hero headline, benefit grid, social proof, CTA.
* **Dashboard** — Sticky sidebar, card masonry, auto‑refresh widgets.
* **Checkout** — Stepper, address form, summary sidebar; resume via localStorage.

---

## 4. Interaction & Motion

### 4.1 Feedback States

* `:hover` communicates affordance; avoid on touch‑only.
* `:focus-visible` outlines use brand accent at 2 px, offset 2 px.
* `:active` may compress element 2 % for tactile feel.

### 4.2 Motion Principles

* Duration 120‑200 ms for small UI shifts, 300‑500 ms for full‑screen.
* Prefer transform/opacity; no `top/left` layout thrashing.
* Default curves: `ease-out` (content entry), `ease-in` (exit), custom `overshoot` for playful UI.

### 4.3 Micro‑Interactions

* Form submit → loading bar at top; 30 ms delay before showing to avoid flash.
* Copy‑to‑clipboard → icon morph + toast “Copied!”.
* Empty states animated doodles loop under 3 s; pause on `prefers-reduced-motion`.

### 4.4 Accessible Motion

* Honor `@media (prefers-reduced-motion: reduce)` by disabling parallax, reducing durations to 0.01s, and avoiding auto‑playing video.

---

## 5. Accessibility & Inclusive Design

1. **Semantic HTML first**; ARIA only when structural semantics lacking.
2. **Keyboard paths**: Tab order follows DOM; include “Skip to main”.
3. **Contrast**: ≥ 4.5:1 for body, 3:1 for 24 px+ headlines.
4. **Readable copy**: Target 9th grade reading level; avoid idioms.
5. **Form UX**: Inline validation, announce errors via `aria-live="polite"`.
6. **I18n**: Tokens avoid embedding language (e.g., no `--color-success-green`).

---

## 6. Complex Experiences (3‑D, VR, Data‑Heavy)

* Keep **FPS ≥ 60**; budget < 1,000 draw calls/ frame; use `requestAnimationFrame`.
* Employ **object pooling** for sprites, reuse geometry buffers.
* **Reduce latency** via WebGL instancing, GPU batching, and culling.
* Provide **assistive camera controls**: auto‑alignment, snap‑back, or guided tours.
* Simplify **data grids**: virtual scrolling, column pinning, keyboard navigation.

---




---

## **Context**

<implementation_plan>
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
</implementation_plan>

<technical_specification>
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
</technical_specification>

<project_request>
# Pulse — Volunteer Resource Editor

A browser-based, real-time-validated interface that lets volunteers and editors create and maintain HSDS records through a single stitched “Resource” form (Service-at-Location + Organization context). Emphasis on sibling-aware navigation, shelf-based bulk apply, and field-level history. **All implementation uses extension tables and overlay services; HSDS tables remain unmodified.**

## Target Audience

- Volunteers updating hyper-local, fast-changing resources not yet reflected in 211.
- Editors/Admins who review flagged changes and manage merges.
- Ops staff who monitor data health and coordinate neighborhood sweeps.

## Desired Features

### Unified Resource Pane (HSDS façade)
- [ ] Single “Resource” pane that stitches HSDS entities (Organization ⇄ Location ⇄ Service; IDs visible)
  - [ ] Core contacts: phone(s), email, website, intake URL
  - [ ] Hours: regular + exceptions/closures
  - [ ] Access bits: walk-in/appointment, fees, languages
  - [ ] Eligibility cheatsheet (short)
  - [ ] Status: active / temporarily closed / defunct
  - [ ] Notes & provenance: method, timestamp, who verified
- [ ] **ResourceSerializer** composes/decomposes across HSDS + extension overlays; validation centralized

### Creation & Drafting
- [ ] **Create Wizard:** Org → Location → Service with prefill banners from siblings and final diff preview
- [ ] New resources save as **Draft** with a **Review** flag (stored in extension tables until approved)
- [ ] Clone-and-edit: duplicate a resource; keep contacts/hours; clear name/description

### Navigation, Worklists, and Shelf
- [ ] Sibling switchers: “other services at this location” / “other services in this org”
  - [ ] Hotkeys: `g l` (go location), `g o` (go org), `[`/`]` (prev/next sibling)
- [ ] Quick-open (⌘K): fuzzy search by name, phone, street, or tag
- [ ] **Worklists:** ad-hoc, shareable queues (e.g., “ZIP 98118 clinics”); `J/K` next/prev
- [ ] **Shelf (global queue):** add any records (cross-org allowed), stage changes, then **Apply to All on Shelf** with diff preview and undo window

### Smart Propagation
- [ ] One-click propagate of shared fields (phones, hours, website) to siblings or to entire Shelf
- [ ] Auto-prefill on create when org/location exists; inline “Undo prefill” per block

### Validation (always-on)
- [ ] **Hard checks:** phone/email/URL format; non-overlapping schedules; geocode resolves; temp closures need reopen date or “unknown”
- [ ] **Soft nudges:** missing contact; missing languages; missing taxonomy
  - [ ] Quick-fix chips (e.g., “Add Spanish”, “Mark Walk-in”)
- [ ] Inline errors/warnings via HTMX partials; hard errors block save

### Freshness & History (visible to all)
- [ ] Field-level freshness badges (e.g., “Phone verified 9 days ago”)
- [ ] Two-tap verify buttons: “Called and confirmed” / “Website updated” (writes provenance + timestamp)
- [ ] Per-field history panel + **revert this field** action

### Dedupe & Merge
- [ ] Live duplicate hints while typing (name/phone/address)
- [ ] Split-view merge: checkbox per field; preserve child objects (phones, schedules) with conflict badges

### Sensitive Mode
- [ ] “Sensitive Resource” flag:
  - [ ] Hide precise address (display neighborhood/area only)
  - [ ] Restrict visible contact methods (e.g., hotline only)

### Checklists & Keyboard Overlay
- [ ] Inline verification checklist (optional): “Phone verified → Hours verified → Intake tested”
  - [ ] Checking items writes provenance notes automatically
- [ ] `?` keyboard overlay; core shortcuts: Save (⌘S), Next/Prev (J/K), Add contact (A), Toggle status (T), Go org (`g o`), Go location (`g l`), Prev/Next sibling (`[`,`]`)

### Moderation & Publication
- [ ] Roles: Admin / Editor / Volunteer
- [ ] **Field Publish Rules (final):**
  - [ ] **Auto-publish:** phones, emails, websites, intake URL, hours (incl. exceptions), access bits (walk-in/appointment), languages, fees flag, temporary closure toggle + reason + reopen date
  - [ ] **Review-required:** service name, description, eligibility details, taxonomy, location address/geo, **defunct toggle (add/remove)**, sensitive flag, org/program linkages
- [ ] Review queue with human-readable diffs; in-app approval (notifications later)

### Concurrency & Safety
- [ ] Optimistic locking per field; non-blocking “merge chips” when concurrent edits detected
- [ ] Undo window after shelf/bulk apply (e.g., 5–10 minutes)
- [ ] Bulk scope guardrails: confirm when applying cross-org via Shelf

### Data Health (lite, in-app)
- [ ] Tiles: “No phone,” “No hours,” “Not geocoded,” “Stale fields”
- [ ] Median days-since-verify by service type & area
- [ ] Flow metric: edit → approval time; % changes propagated

## Design Requests
- [ ] Single-column, mobile-friendly layout; large tap targets
- [ ] Compact chips for languages/taxonomy/access bits
- [ ] Clear banners for inherited/prefilled data with one-click undo
- [ ] Diff preview modal before Save
- [ ] WCAG AA contrast; labeled inputs and visible focus states

## Architecture & Implementation Notes (No HSDS table changes)

- **Extension schema (separate tables, namespaced; examples):**
  - [ ] `hsds_ext_verification_events`
        - `id, entity_type, entity_id, field_path, method(enum: called|website|onsite|other), note, verified_at, verified_by`
        - Drives field-level freshness; feeds provenance log.
  - [ ] `hsds_ext_field_versions`
        - `id, entity_type, entity_id, field_path, version, updated_at, updated_by`
        - Powers **optimistic locking** and ETag generation per field.
  - [ ] `hsds_ext_sensitive_overlays`
        - `id, entity_type, entity_id, sensitive:boolean, visibility_rules(jsonb)`
        - Read-time overlay to redact precise address/contacts when flagged.
  - [ ] `hsds_ext_draft_resources`
        - `id, created_by, created_at, status(enum: draft|approved|rejected), payload(jsonb)`
        - Stores composite Resource payloads (Org/Location/Service) until approved, then written into HSDS.
  - [ ] `hsds_ext_change_requests`
        - `id, target_entity_type, target_entity_id, patch(jsonb RFC6902), status(enum: pending|approved|rejected), submitted_by, submitted_at, reviewed_by, reviewed_at`
        - Captures **review-required** edits; approval applies patch to HSDS.
  - [ ] `hsds_ext_bulk_operations`
        - `id, initiated_by, initiated_at, scope(enum: shelf|siblings), targets(jsonb), patch(jsonb), preview(jsonb), status(enum: staged|committed|undone), undo_token, committed_at, undone_at`
        - Stages shelf/sibling **bulk apply** with preview + undo.
  - [ ] `hsds_ext_shelves`
        - `id, owner_id, name, created_at, is_shared:boolean`
        - Collection of Resource references; cross-org allowed.
  - [ ] `hsds_ext_shelf_members`
        - `shelf_id, entity_type, entity_id, added_by, added_at`

- **Composite “Resource” API (façade):**
  - [ ] `GET /api/resource/{id}` → stitches HSDS entities + overlays; redacts via `hsds_ext_sensitive_overlays`
  - [ ] `PATCH /api/resource/{id}` (auto-publish fields) → writes to HSDS + updates `verification_events` and `field_versions`
  - [ ] `POST /api/resource` (wizard final step) → creates `hsds_ext_draft_resources` entry
  - [ ] `POST /api/review_queue/{change_request_id}/approve` → applies stored patch to HSDS; logs events/versions
  - [ ] All PATCH/POST require `If-Match` using field-level ETags from `hsds_ext_field_versions`

- **Review queue & drafts:**
  - [ ] Wizard submits **draft composite payload** to `hsds_ext_draft_resources`
  - [ ] Editor approval writes HSDS entities (Org/Location/Service) using canonical serializers
  - [ ] Review-required edits from live records land in `hsds_ext_change_requests` with JSON Patch

- **Shelf & bulk apply:**
  - [ ] `POST /api/shelf/{id}/stage_patch` → compute per-target diffs
  - [ ] `GET /api/bulk_ops/{id}/preview` → human-readable preview for UI
  - [ ] `POST /api/bulk_ops/{id}/commit` → apply across targets; create undo token
  - [ ] `POST /api/bulk_ops/{id}/undo` → revert via inverse patch

- **Dedupe & search:**
  - [ ] Duplicate hints via service indexing on name/phone/address; split-view merge uses JSON Patch
  - [ ] Quick-open uses DB text search (e.g., trigram/FTS); no performance targets required

- **Keyboard overlay:**
  - [ ] Central registry (json/yaml) drives both bindings and the `?` overlay UI
  - [ ] Scope-aware (global vs form section) and discoverable

- **Diffs & history:**
  - [ ] JSON Patch shown before save; per-field history joins HSDS last value + latest verification event + version counter

- **Taxonomy:**
  - [ ] Use HSDS taxonomy; store **namespaced extensions** as needed (e.g., `local:subtype`) and map back to HSDS on publish

## Other Notes
- **No offline mode.** Browser-based only
- **No attachments, macros, QR, or map/location helper UI** in v1
- Export handled by the other app (deferred)
- API-first: HTMX views call DRF serializers; validation is centralized via API
- **Defunct toggle requires review** (prevent accidental removals)

## Open Questions
- None blocking. (Future: notification strategy, editor workload views, and export sync hooks.)
</project_request>

<project_rules>
- **Django Coomponents**: We have `django-components` and should make the most use out of it. Components go in `src/[app]/components/[meta component or purpose]/[component name].{py,html}`. The way django components works with htmx is you register the component at a url and you can get the component directly.
  - **Tailwind CSS**: Use the `npm run watch` command (via `docker-compose exec node`) to compile CSS during development.
  - **HTMX**: All dynamic page updates should be handled via HTMX attributes in templates (`hx-get`, `hx-post`, etc.).
  - **Alpine.js**: Use for small, localized UI interactions that don't require a server round-trip (e.g., toggling a dropdown, managing modal visibility). Use the `x-data`, `x-show`, and `@click` directives. See `docs/frameworks/alpine-js.md`.
  - **Daisy UI**: Our primary component library. Use pre-built components whenever possible. See `docs/frameworks/daisyui.md`.
</project_rules>

<existing_code>
see docs/frameworks/*.md
</existing_code>

---
