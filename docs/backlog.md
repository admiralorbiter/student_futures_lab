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
| Now | Build | Not started | Initialize Flask repo, config, templates, and static folders. |
| Now | Build | Not started | Set up SQLite database and response model (students + responses tables). |
| Now | Data | Not started | Run `export_from_kc_industries.py` to seed initial YAML files. |
| Now | Content | Not started | Author `pathway_families.yaml` — map CIP program areas to 7 pathway families. |
| Now | Content | Not started | Translate student packet labels into UI copy. |
| Now | Content | Not started | Author `pathway_summaries.yaml` with plain-language signals from data. |
| Now | QA | Not started | Create mock YAML data so screens can be built before full data curation. |

## 3. Screen-by-screen

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Now | Build | Not started | Create Screen 1 layout and cards for seven pathways (loads from YAML). |
| Now | Build | Not started | Add form handling for criteria ranking, pathway buckets, and confidence. |
| Now | QA | Not started | Verify Screen 1 labels match classroom packet language. |
| Soon | Build | Not started | Create Screen 2 comparison layout for top pathways only. |
| Soon | Content | Not started | Finalize barrier and support tag definitions in `support_tags.yaml`. |
| Soon | Content | Not started | Author `county_notes.yaml` for Hickman Mills access context. |
| Soon | Content | Not started | Create `employer_context.yaml` from kc-industries geocoded employers. |
| Soon | Build | Not started | Persist revised ranking and what-changed notes (for code-based users). |
| Soon | Build | Not started | Create Screen 3 institution filter by pathway. |
| Soon | Data | Not started | Author `launch_points.yaml` — pathway-to-institution mapping with reasons. |
| Soon | Build | Not started | Create Screen 4 reflection form with save and edit. |
| Soon | Build | Not started | Create Screen 5 recommendation builder with prefilled evidence. |

## 4. Data curation

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Now | Data | Not started | Write `export_from_kc_industries.py` to query kc-industries DB and produce seed YAML. |
| Now | Content | Not started | Author pathway summaries, caution notes, and county notes in YAML. |
| Now | Content | Not started | Extract glossary terms from Student Glossary doc into `glossary.yaml`. |
| Soon | Content | Not started | Author launch-point reasons and bridge role descriptions. |
| Soon | Data | Not started | Extract plain-language label mapping from App Spec into `plain_language_labels.yaml`. |

## 5. Polish and QA

| Priority | Type | Status | Task |
|----------|------|--------|------|
| Soon | Build | Not started | Create print-friendly view for Screen 5 recommendation. |
| Soon | QA | Not started | Test optional code save/resume across all 5 screens. |
| Later | QA | Not started | Run full classroom rehearsal with mock data. |
| Later | QA | Not started | Test print/PDF layout from real entries. |

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
