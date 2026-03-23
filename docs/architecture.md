# Technical Architecture and Data Integration Plan

*Flask + SQLite architecture for a guided classroom inquiry app with pre-baked pathway data from [kc-industries](https://github.com/admiralorbiter/kc-industries).*

> **Implementation stance**
> Server-rendered Flask app with Jinja templates. Lightweight progressive enhancement (HTMX or Alpine-style patterns) only where it improves the classroom flow.
> This is a guided workflow application, not a client-heavy analytics tool.

## 1. Stack

| Layer | Tool | Why |
|-------|------|-----|
| Backend | Flask | Fast to build, familiar Python ecosystem. |
| Templating | Jinja2 | Server-rendered screens and print-friendly outputs. |
| Database (responses) | SQLite | Read-write. Student responses only. |
| Database (pathway data) | SQLite | Read-only. Programs, institutions, occupations, employers. Exported from kc-industries. |
| ORM | Flask-SQLAlchemy | Student response schema. |
| Pathway data (editorial) | YAML | Pre-baked summaries, tags, glossary — hand-edited by PREP-KC. |
| Pathway data (granular) | SQLite | 889 programs, 63 institutions, 634 occupations, 5,610 employers. |
| Front end | HTML + CSS + small JS | Understandable, aligned with classroom flow. |
| Drag-and-drop | SortableJS (CDN) | Criteria ranking on Screen 1. Zero-dependency, 3KB. |
| Data visualization | Chart.js (CDN) | Interactive charts on Screens 1 and 2. Deferred rendering for collapsed sections. |

## 2. Repository structure

```text
student_futures_lab/
├── README.md
├── docs/
│   ├── DECISIONS.md
│   ├── architecture.md          ← you are here
│   ├── backlog.md
│   ├── roadmap.md
│   └── reference/
│       ├── prd.md
│       └── app_spec.md
├── class_materials/
│   ├── student_core_inquiry_packet.md
│   ├── student_glossary.md
│   ├── student_evidence_catcher.md
│   ├── student_presentation_planner.md
│   ├── teacher_facilitation_guide.md
│   └── teacher_insight_capture.md
├── app.py                          # Entry point: python app.py
├── app/
│   ├── __init__.py                 # App factory
│   ├── config.py
│   ├── extensions.py               # SQLAlchemy init
│   ├── models/
│   │   └── student.py              # students, responses
│   ├── services/
│   │   └── pathway_service.py      # Hybrid: YAML + read-only SQLite
│   ├── blueprints/
│   │   └── main/                   # Screen routes
│   ├── templates/
│   │   ├── base.html
│   │   ├── landing.html
│   │   └── screens/screen_1–5.html
│   └── static/
│       ├── css/main.css
│       └── favicon.ico
├── data/
│   ├── mappings/                   # YAML editorial content (PREP-KC edits)
│   │   ├── pathway_families.yaml
│   │   ├── pathway_summaries.yaml
│   │   ├── support_tags.yaml
│   │   ├── county_notes.yaml
│   │   ├── launch_points.yaml
│   │   ├── employer_context.yaml
│   │   ├── glossary.yaml
│   │   └── plain_language_labels.yaml
│   ├── pathway_data.db             # Read-only SQLite (exported from kc-industries)
│   └── student_responses.db        # Read-write SQLite (created at runtime)
├── scripts/
│   ├── export_pathway_data.py      # Regenerate pathway_data.db from kc-industries
│   └── analyze_pathways.py         # Data analysis utility
└── tests/
```

## 3. Data architecture

Two-layer design (see Decision D9 in DECISIONS.md):

### Layer 1: YAML editorial content (PREP-KC editable)

| File | Contains | Source |
|------|----------|--------|
| `pathway_families.yaml` | 7 pathway families + CIP mapping + 9 additional fields | CIP families + PREP-KC grouping |
| `pathway_summaries.yaml` | Summaries, wage/demand/scale signals, caution notes | Data-derived + authored |
| `support_tags.yaml` | 7 barrier + 7 support tag definitions | PREP-KC authored |
| `county_notes.yaml` | Hickman Mills access context per pathway | Authored, informed by LEHD |
| `launch_points.yaml` | Institution archetypes, bridge roles, watch-outs | IPEDS/Scorecard + authored |
| `employer_context.yaml` | Top 5 employers per pathway | Curated from geocoded employers |
| `glossary.yaml` | 12 terms with Socratic prompts | Student Glossary |
| `plain_language_labels.yaml` | Technical field → plain label mapping | App Spec |

### Layer 2: Read-only SQLite (`pathway_data.db`)

Granular program, institution, and occupation data exported from kc-industries. Regenerated via `python scripts/export_pathway_data.py`.

| Table | Rows | Contains |
|-------|------|----------|
| `programs` | 889 | Program name, CIP, credential, earnings at 1yr/2yr/4yr, completions |
| `institutions` | 63 | Name, type, city, lat/lon, ownership, Scorecard link |
| `occupations` | 634 | SOC title, median wage, employment, growth, education required |
| `program_occupations` | 3,669 | Which programs link to which occupations |
| `employers` | 5,610 | Name, NAICS, headcount, city, lat/lon, county FIPS |
| `sector_profiles` | 20 | NAICS sector overview, risks, opportunities |
| `institution_sectors` | 714 | Which sectors each institution serves |

### Layer 3: Read-write SQLite (`student_responses.db`)

Only used when students enter an optional save code.

| Table | Purpose |
|-------|---------|
| `students` | Student code, cohort label, created timestamp |
| `responses` | Screen-by-screen saved selections, note text, timestamps |

### Relationship to kc-industries

```
kc-industries (source repo)            student_futures_lab (this repo)
┌──────────────────────────┐           ┌──────────────────────────────────┐
│ instance/app.sqlite      │           │ data/mappings/*.yaml             │
│  • program (889)         │  export   │  (editorial — PREP-KC edits)     │
│  • provider (63)         │ ────────→ │                                  │
│  • occupation (983)      │  script   │ data/pathway_data.db             │
│  • scorecard_earning     │           │  (read-only — granular data)     │
│  • scorecard_institution │           │                                  │
│  • organization (780)    │           │ data/student_responses.db        │
│  • program_occupation    │           │  (read-write — student answers)  │
│  • provider_sector       │           │                                  │
└──────────────────────────┘           └──────────────────────────────────┘
```

`scripts/export_pathway_data.py` queries the kc-industries database and builds `pathway_data.db`. YAML files were initially seeded from data analysis, then hand-edited by PREP-KC.

## 4. Route and screen map

| Route | Screen | Notes |
|-------|--------|-------|
| `/` | Landing | Simple welcome, optional code entry |
| `/screen/1` | Pathway Explorer | Initial ranking and criteria capture |
| `/screen/2` | Hickman Mills Lens | Barrier/support tagging, employer context, revised ranking |
| `/screen/3` | Launch Points | Filtered institution choices plus bridge roles |
| `/screen/4` | My Pathway Reality Check | Individual reflection |
| `/screen/5` | Recommendation Builder | Final synthesis output |

**Not in v1:** `/facilitator`, `/export/*`

## 5. Identity model

- No login required. Anyone can explore all 5 screens.
- Optional: enter a short code (4–6 chars) to save responses.
- Code is stored in a browser cookie for session continuity.
- Responses saved to SQLite keyed by code + screen.
- No PII collected. No facilitator login in v1.

## 6. Schema layers for YAML data

| Layer | What belongs there |
|-------|-------------------|
| Source (in kc-industries) | Raw downloaded CSVs, API responses, snapshots |
| Staging (in kc-industries) | Cleaned tables with standardized columns |
| Domain / mapping (this repo) | Pathway families, bridge roles, county notes, support tags, launch-point reasons |
| Presentation (this repo) | Student-facing summaries loaded from YAML at app start |

## 7. Testing priorities

- Inquiry flow works end to end from landing through all 5 screens.
- Progress persists correctly across screens (for code-based users).
- YAML files load without error.
- Screens render with plain-language labels matching the class materials.
- App boots cleanly with a fresh database.

## 8. Security, privacy, and classroom practicality

- No personal data collected. Codes are self-chosen or teacher-assigned, not PII.
- Student reflection responses are separable from identifying details.
- Simple autosave or explicit save checkpoints on each screen.
- Design for partial progress: students can leave and return without losing work.
- Back up the SQLite file after each class day.
