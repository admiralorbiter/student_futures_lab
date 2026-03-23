# Rolling Backlog and Task Tracker

*A living task list organized for fast iteration. Reprioritize after each build session or data discovery.*

> **How to use this document**
> Treat this as a working backlog, not a frozen plan. Keep tasks small enough to finish, test, or clearly park within one focused work block.

## 1. Conventions

| Field | Meaning |
|-------|---------|
| Priority | Now / Soon / Later |
| Type | Build / Data / Content / QA / Decision |
| Status | Not started / In progress / Blocked / Done |

## 2. Immediate setup

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Now | Build | Done | Initialize Flask repo, config, templates, and static folders. |
| Now | Build | Done | Set up SQLite database and response model (students + responses tables). |
| Now | Build | Done | Create screen stub templates for all 5 screens with navigation. |
| Now | Data | Done | Author `pathway_families.yaml` — map CIP program areas to 7 pathway families + additional fields. |
| Now | Content | Done | Translate student packet labels into UI copy (`plain_language_labels.yaml`). |
| Now | Content | Done | Author `pathway_summaries.yaml` with plain-language signals from data. |
| Now | Content | Done | Author `support_tags.yaml`, `county_notes.yaml`, `employer_context.yaml`, `launch_points.yaml`, `glossary.yaml`. |
| Now | QA | Done | All YAML files load and are accessible via `PathwayService`. |

## 3. Screen-by-screen

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Now | Build | Done | Create Screen 1 layout and cards for seven pathways + additional fields (loads from YAML). |
| Now | Build | Done | Add form handling for criteria ranking, pathway buckets, and confidence. |
| Now | QA | Done | Verify Screen 1 labels match classroom packet language. |
| Now | Build | Done | Create Screen 2 comparison layout for top pathways only. |
| Now | Build | Done | Persist revised ranking and what-changed notes (for code-based users). |
| Now | Build | Done | Create Screen 3 institution filter by pathway. |
| Now | Build | Done | Create Screen 4 reflection form with save and edit. Cross-screen evidence sidebar. |
| Now | Build | Done | Create Screen 5 recommendation builder with prefilled evidence and print button. |

## 4. Enrichment (shipped with Epics)

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Now | Build | Done | Import IPEDS institutional profiles (217 institutions × 79 columns) into `pathway_data.db`. |
| Now | Build | Done | Enrich Screen 3 launch point cards with IPEDS stats (enrollment, grad rate, Pell %). |
| Now | Build | Done | Build institution detail page (`/institution/<id>`) with IPEDS scorecard. |
| Now | Build | Done | Create print-friendly view for Screen 5 recommendation (`@media print`). |
| Now | Build | Done | Add completion page after Screen 5 submit. |
| Now | Build | Done | Import BLS QCEW employment + projections. Surface on Screens 1–2 cards, 4–5 sidebars, and Screen 5 print view. |

## 5. Polish and QA

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Now | Build | Done | Extract `_screen_nav.html` partial to reduce navigation duplication. |
| Now | QA | Done | Test optional code save/resume across all 5 screens. |
| Soon | QA | Not started | Run full classroom rehearsal with mock data. |
| Soon | QA | Not started | Test print/PDF layout from real entries. |
| Soon | Build | Not started | Add pytest route smoke tests. |

## 6. Post-v1

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Later | Build | Not started | Create facilitator dashboard with progress by screen. |
| Later | Build | Not started | Create CSV export for student responses. |
| Later | Build | Not started | Add student/facilitator login system. |
| Later | Build | Not started | Add interactive employer/location map layer. |
| Later | Build | Not started | Add JSON export for downstream analysis. |

## 7. Suggested work rhythm

1. Build the smallest slice that can be clicked through.
2. Seed it with mock YAML data if the real curation is not ready.
3. Swap in real data only after the screen interaction feels right.
4. After each screen works, print the output and compare to the class packet.
5. At the end of each build session, update this backlog.
