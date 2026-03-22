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
| Database | SQLite | v1 stores student responses only. Simple local dev + exports. |
| ORM | SQLAlchemy or Flask-SQLAlchemy | Schema evolution and local queries. |
| Forms | WTForms or light custom validation | Structured input. |
| Front end | HTML + CSS + small JS | Understandable, aligned with classroom flow. |
| Enhancement | HTMX or Alpine-like patterns | Partial updates, save without reload. |
| Pathway data | YAML/JSON files | Pre-baked from kc-industries, hand-edited with PREP-KC content. |

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
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py           # students, responses
│   ├── services/
│   │   ├── inquiry_service.py
│   │   ├── pathway_service.py   # loads YAML pathway data
│   │   └── response_service.py
│   ├── blueprints/
│   │   ├── main/
│   │   └── api/
│   ├── templates/
│   │   ├── base.html
│   │   └── screens/
│   └── static/
│       ├── css/
│       └── js/
├── data/
│   ├── mappings/
│   │   ├── pathway_families.yaml
│   │   ├── pathway_summaries.yaml
│   │   ├── support_tags.yaml
│   │   ├── county_notes.yaml
│   │   ├── launch_points.yaml
│   │   ├── employer_context.yaml
│   │   ├── glossary.yaml
│   │   └── plain_language_labels.yaml
│   └── student_responses.db     # SQLite — created at runtime
├── scripts/
│   └── export_from_kc_industries.py
└── tests/
```

## 3. Data architecture

### Pathway data (read-only, YAML/JSON)

Pre-baked from `kc-industries`, enriched with PREP-KC editorial content. No runtime dependency on the kc-industries repo.

| File | Contains | Source |
|------|----------|--------|
| `pathway_families.yaml` | 7 pathway family definitions + CIP-to-pathway mapping | CIP families from kc-industries + PREP-KC grouping |
| `pathway_summaries.yaml` | Plain-language summary, wage signal, demand signal, scale, county fit, caution note, example roles | Derived from BLS/OEWS/projections + authored content |
| `support_tags.yaml` | Barrier and support tag definitions | PREP-KC authored |
| `county_notes.yaml` | Hickman Mills access, transportation, local context | PREP-KC authored, informed by LEHD/commute data |
| `launch_points.yaml` | Institution archetypes, launch-point reasons, bridge roles | Derived from IPEDS/Scorecard + authored content |
| `employer_context.yaml` | Top employers per pathway near Hickman Mills | Extracted from kc-industries geocoded employers |
| `glossary.yaml` | Student-facing term definitions and Socratic prompts | From Student Glossary |
| `plain_language_labels.yaml` | Technical field → plain label mapping | From App Spec |

### Student response data (SQLite)

Only used when students enter an optional save code. Schema:

| Table | Purpose |
|-------|---------|
| `students` | Student code, cohort label, created timestamp |
| `responses` | Screen-by-screen saved selections, note text, timestamps |

No `pathways`, `institutions`, or `team_outputs` tables in v1 — pathway data comes from YAML.

### Relationship to kc-industries

```
kc-industries (source repo)          student_futures_lab (this repo)
┌─────────────────────────┐          ┌──────────────────────────┐
│ kc_pathways.db          │          │ data/mappings/*.yaml     │
│  • occupation           │  export  │  • pathway_families      │
│  • scorecard_earning    │ ───────→ │  • pathway_summaries     │
│  • scorecard_institution│  once    │  • launch_points         │
│  • organization         │          │  • employer_context      │
│  • program_occupation   │          │                          │
│  • metric_value         │          │ data/student_responses.db│
│  • provider_sector      │          │  • students              │
│  • major_employers.json │          │  • responses             │
└─────────────────────────┘          └──────────────────────────┘
```

A one-time `export_from_kc_industries.py` script queries the kc-industries database and generates the YAML seed files. PREP-KC content is then hand-edited on top.

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
