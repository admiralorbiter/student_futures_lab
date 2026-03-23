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
| Soon | Build | Done | Create Screen 2 comparison layout for top pathways only. |
| Soon | Build | Done | Persist revised ranking and what-changed notes (for code-based users). |
| Soon | Build | Done | Create Screen 3 institution filter by pathway. |
| Soon | Build | Not started | Create Screen 4 reflection form with save and edit. |
| Soon | Build | Not started | Create Screen 5 recommendation builder with prefilled evidence. |

## 4. Polish and QA

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Soon | Build | Not started | Create print-friendly view for Screen 5 recommendation. |
| Soon | QA | Not started | Test optional code save/resume across all 5 screens. |
| Later | QA | Not started | Run full classroom rehearsal with mock data. |
| Later | QA | Not started | Test print/PDF layout from real entries. |

## 5. Post-v1

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Later | Build | Not started | Create facilitator dashboard with progress by screen. |
| Later | Build | Not started | Create CSV export for student responses. |
| Later | Build | Not started | Add student/facilitator login system. |
| Later | Build | Not started | Add interactive employer/location map layer. |
| Later | Build | Not started | Add JSON export for downstream analysis. |

## 6. Suggested work rhythm

1. Build the smallest slice that can be clicked through.
2. Seed it with mock YAML data if the real curation is not ready.
3. Swap in real data only after the screen interaction feels right.
4. After each screen works, print the output and compare to the class packet.
5. At the end of each build session, update this backlog.
