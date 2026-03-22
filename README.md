# Student Futures Lab

A guided inquiry app for the Hickman Mills Pathway Advisory Team project, built for [PREP-KC](https://www.prepkc.org/).

Students use this tool to compare career pathway families using labor-market evidence, apply a Hickman Mills lens for local reachability, identify realistic postsecondary launch points, and build a final recommendation for PREP-KC.

**Anyone can explore the data anonymously.** Classroom students can optionally save progress with a short code.

## Tech Stack

| Layer | Tool |
|-------|------|
| Backend | Flask + Python |
| Database | SQLite (student responses only) |
| Templating | Jinja2 |
| Pathway data | Pre-baked YAML/JSON (from [kc-industries](https://github.com/admiralorbiter/kc-industries)) |
| Front end | HTML + CSS + light JS |

## Getting Started

```bash
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Data Sources

Pathway and institution data is derived from the [kc-industries](https://github.com/admiralorbiter/kc-industries) repo, which integrates:

- **BLS / OEWS** — occupation wages, employment, location quotients
- **BLS Projections** — 10-year national growth and openings
- **IPEDS** — institutional programs and completions
- **College Scorecard** — program-level earnings after graduation
- **Census / ACS** — local context and commute patterns
- **PREP-KC authored content** — pathway summaries, support tags, county notes (YAML)

## Documentation

### Living dev docs (change during development)
- [Architecture](docs/architecture.md) — stack, schema, routes, data pipeline
- [Roadmap](docs/roadmap.md) — milestones, epics, build sequence
- [Backlog](docs/backlog.md) — prioritized task list
- [Decisions](docs/DECISIONS.md) — resolved and open design decisions

### Stable reference docs
- [Product Requirements](docs/reference/prd.md) — goals, users, screens, success criteria
- [App Specification](docs/reference/app_spec.md) — screen-by-screen data and input spec

### Class materials
- [Student Core Inquiry Packet](class_materials/student_core_inquiry_packet.md)
- [Student Glossary](class_materials/student_glossary.md)
- [Student Evidence Catcher](class_materials/student_evidence_catcher.md)
- [Student Presentation Planner](class_materials/student_presentation_planner.md)
- [Teacher Facilitation Guide](class_materials/teacher_facilitation_guide.md)
- [Teacher Insight Capture Sheet](class_materials/teacher_insight_capture.md)
