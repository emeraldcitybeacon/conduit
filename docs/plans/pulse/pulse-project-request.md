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
