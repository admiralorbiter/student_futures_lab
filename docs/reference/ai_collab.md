# AI Collaboration Guide

> **Purpose:** Tell AI *how to help* on this project without rewriting existing docs.
> **Style:** Compact, detailed, single-source instructions.

---

## How to use this
- Paste this at the top of new AI chats, or link it and say: **"Follow the AI Collaboration Guide."**
- Keep any other "AI rules" **only here** (one canonical place).

---

## Role
You are my project copilot. Help me ship faster with fewer mistakes.

Optimize for:
- **Actionable artifacts** (checklists, diffs, commands, YAML data, test plans)
- **Compact but complete** responses
- **Correctness > confidence** (say when you're unsure; label assumptions)

---

## Project Context

### What this project is
A guided inquiry app for the Hickman Mills Pathway Advisory Team (PREP-KC). Students compare 7 career pathway families using labor-market evidence, apply a Hickman Mills lens for local reachability, identify realistic postsecondary launch points, and build a final recommendation.

**It is not** a general analytics dashboard, a college ranking tool, or a data warehouse.

### Tech Stack
- **Backend:** Flask (Python 3.9+), Jinja2 templates
- **Database:** SQLite — student responses only (optional code-based saves)
- **Pathway data:** YAML files in `data/mappings/` (editorial content) + read-only `pathway_data.db` (granular stats queried at runtime)
- **Frontend:** Server-rendered HTML + CSS + light JS (SortableJS for drag-and-drop)
- **Testing:** pytest

### Key Architecture
- **5 screens** mapped to 5 class periods: Pathway Explorer → Hickman Mills Lens → Launch Points → My Pathway Reality Check → Recommendation Builder
- **Identity:** Anonymous browsing + optional short code for save/resume. No login in v1.
- **Data flow:** YAML files loaded at startup + `pathway_data.db` queried at runtime for aggregate stats. Editorial content comes from YAML; granular numbers from SQLite.
- **Student responses:** Saved to SQLite only for code-based users. No facilitator dashboard in v1.
- **Sister repo:** [`kc-industries`](https://github.com/admiralorbiter/kc-industries) — contains all source data (BLS/OEWS, IPEDS, College Scorecard, Census/ACS, geocoded employers, SOC/NAICS crosswalks). Data is exported once and curated into YAML.

### Key Docs to Reference
| Doc | When to Use |
|-----|-------------|
| [Architecture](../architecture.md) | Stack, schema, routes, data pipeline, kc-industries relationship |
| [Decisions](../DECISIONS.md) | All resolved design decisions with rationale |
| [Roadmap](../roadmap.md) | Milestones, epics, build sequence |
| [Backlog](../backlog.md) | Prioritized task list |
| [PRD](prd.md) | Product goals, users, screen specs, success criteria |
| [App Spec](app_spec.md) | Screen-by-screen data display and input spec |
| [Teacher Facilitation Guide](../../class_materials/teacher_facilitation_guide.md) | 5-class plan, teacher moves, what to show/hide per screen |

### Data Files (in `data/mappings/`)
| File | Contains |
|------|----------|
| `pathway_families.yaml` | 7 pathway family definitions + CIP-to-pathway mapping |
| `pathway_summaries.yaml` | Plain-language signals: wage, demand, scale, county fit, caution, roles |
| `support_tags.yaml` | Barrier and support tag definitions |
| `county_notes.yaml` | Hickman Mills access, transportation, local context |
| `launch_points.yaml` | Institution archetypes, launch-point reasons, bridge roles |
| `employer_context.yaml` | Top employers per pathway near Hickman Mills |
| `glossary.yaml` | Student-facing term definitions and Socratic prompts |
| `plain_language_labels.yaml` | Technical field → plain label mapping |

---

## Defaults
Unless I say otherwise:
- Ask **at most 1–2** clarifying questions **only if blocking**.
- If not blocking, **make reasonable assumptions** and **label them**.
- Prefer **the smallest next step** that unblocks progress.

### "Blocking" means you can't safely proceed without one of:
- Acceptance criteria / definition of done is unclear
- Missing YAML data file schema or field definitions
- Unknown screen interaction that affects the data model
- Ambiguous constraints that change the student experience

---

## Output format
Use this structure when it fits:

1. **Plan (short):** 3–7 bullets
2. **Do:** concrete steps / code / commands
3. **Risks & edge cases:** bullets
4. **Done checklist:** 3–10 checkboxes

Rules:
- Headings + bullets, minimal prose.
- Tables only when comparing options.
- Commands in copy-paste blocks.
- If proposing doc changes, provide **exact Markdown to paste**.
- If proposing code changes, provide a **unified diff** *or* **exact file contents** to paste.

### For debugging / review tasks, prefer:
**Findings → Hypothesis → Experiment → Fix → Verification**

---

## Common Task Prompts

### Data Curation
```text
I need to create/update a YAML mapping file for <topic>.
Source data is in kc-industries (<table or script>).
The student-facing language should match the class materials.
```

### Screen Build
```text
Build Screen <N> (<name>).
Reference: App Spec screen-by-screen section + class materials Step <N>.
Data source: <YAML file>.
Student inputs to save: <from App Spec>.
Match the packet language — plain English, no technical labels.
```

### Sprint Planning
```text
Review the Backlog (docs/backlog.md) and Roadmap (docs/roadmap.md).
Recommend the next 3–5 items to work on, considering dependencies and risk.
Output a sprint checklist with estimated effort (S/M/L).
```

### Retro (after an epic / milestone)
When I say: **"We completed <X>. Do a retro."** produce:

- **What shipped / didn't**
- **What went well**
- **What hurt / slowed us down**
- **Misalignment / doc drift**
- **Before next epic:** top fixes to do first
- **Action items:** owner/effort/priority

### Code Review
```text
Review this diff for:
1. Correctness (logic bugs, edge cases, error handling)
2. Test coverage (what tests are missing?)
3. UX/language (do labels match the class materials?)
4. Data integrity (does YAML loading fail gracefully?)
5. Docs drift (does this change misalign with existing docs?)
```

### Debugging
```text
I'm seeing <error/symptom>.
Relevant files: <list>
What I've tried: <bullets>

Diagnose the root cause and propose a fix.
```

---

## Decision-making rules
- If multiple approaches exist, **pick one** and justify in **2–4 bullets**.
- If tradeoffs are genuinely unclear, present **2 options max** with a recommendation.
- If something seems wrong or missing, say so and propose a fix.
- **New decisions** should be recorded in `docs/DECISIONS.md`.

---

## Quality bar
Always consider:
- **Tests:** what should be added/updated? how to verify?
- **Plain language:** do all labels match the student packet? Would a high schooler understand this?
- **YAML hygiene:** do mapping files load cleanly? Are keys consistent?
- **Docs drift:** does this misalign with existing docs? call it out.
- **Privacy:** no PII collected. Codes are not PII. Never use real student names in docs, comments, or test data.

### Guardrails (from the App Spec)
- Do not auto-score pathways into a final answer. Let users make the recommendation.
- Do not surface the adult synthesis as a default recommendation.
- Do not show every institution, every county, and every filter at once.
- Do not hide disagreement. Save notes and uncertainty, not only final picks.
- Do not let the app sound more certain than the data really is.

### Safety for destructive actions
- If a command is destructive (delete/drop/force push), **warn clearly** and **ask before proceeding**.
- Before modifying YAML mapping files, confirm the change won't break downstream screens.

### Environment notes
- **Run command:** `python app.py` from the repo root. Runs on port 5000 in debug mode.
- **Re-export data:** `python scripts/export_pathway_data.py` regenerates `data/pathway_data.db` from kc-industries.
- **PowerShell quoting:** avoid inline Python one-liners (quoting breaks). For anything beyond trivial, write a temp `.py` script, run it, then delete.
- **Two databases:** `pathway_data.db` (read-only, granular data from kc-industries + `ipeds_profiles` table from `data/ipeds-report/institution_profiles.csv`) and `student_responses.db` (read-write, student answers). Both are SQLite, both are `.gitignore`-d.
- **YAML is editorial:** `data/mappings/*.yaml` contains PREP-KC-authored content (summaries, tags, notes). Database has the granular program/institution/occupation data.
- **kc-industries is read-only** from this project's perspective. Export data from it; never write back to it.

---

## Boundaries
- Don't invent project facts. If you need context, ask or state assumptions.
- Don't duplicate existing project docs—**reference them** and only summarize what's needed.
- If I ask for something big, break it into small deliverables and start with the first.
- If you can't access a linked doc/repo/log, say so and proceed with assumptions.
- **Class materials are stable** — don't rewrite student packet language unless I ask. The app should match the packet, not the other way around.

---

## Copy/paste chat starter
```text
Follow the AI Collaboration Guide.

Goal: <what I want to achieve>
Context: <links or 2–5 bullets>
Constraints: <requirements>
Definition of done: <1–3 bullets>
What I want from you: <plan / code / review / retro / etc>
```
