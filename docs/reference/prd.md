# PRD: Hickman Mills Guided Inquiry App

*Server-rendered classroom app to guide pathway inquiry, capture student reasoning, and produce useful PREP-KC planning data.*

> **Product intent**
> This product is not a general labor-market dashboard. It is a guided inquiry tool that helps students compare pathways, apply a Hickman Mills lens, connect those pathways to realistic launch points, and produce a defensible recommendation.
> The app should feel like a sequence of questions, not an open-ended data warehouse.
> **Anyone can explore anonymously.** Classroom students can optionally save progress with a short code.

## 1. Problem statement

PREP-KC needs a lightweight application that helps students reason across multiple data sources without overwhelming them. The class must move from raw pathway opportunity to local reachability and support needs, then connect that evidence to realistic postsecondary starts and personal reflection.

The current challenge is not access to data alone; it is the need to sequence that data in a way that leads to a useful student product and usable internal insight.

## 2. Product goals

### The product should:

- Guide users through the inquiry in phases that match the classroom packet and facilitation plan.
- Use plain language instead of internal field names or technical labor-market labels.
- Capture structured answers and short written reasoning at each stage (for code-based users).
- Stay simple enough to build quickly in Flask, SQLite, HTML, CSS, and light JavaScript.
- Be usable by anyone who wants to explore KC pathways, not just the classroom.

## 3. Non-goals

- Not a fully open analytics dashboard.
- Not a public-facing PREP-KC product in v1.
- Not a long-term data warehouse or master source-of-truth platform.
- Not an auto-scoring engine that decides the "best" pathway for students.
- **Not a facilitator tool in v1** — no teacher dashboard, no CSV export UI, no login system.

## 4. Primary users

| User | What they need |
|------|---------------|
| Students (classroom) | A guided flow, readable summaries, optional save with a short code. |
| General explorers | Anonymous access to pathway, lens, and launch-point data without saving. |
| Facilitator | Uses the paper packet and PREP-KC Insight Capture Sheet alongside the app in v1. |
| PREP-KC staff | Structured insight from YAML-based data curation and optional SQLite responses. |

## 5. Core user stories

1. As a user, I want to compare pathway families without being buried in dozens of filters, so I can form an initial judgment.
2. As a user, I want to re-rank pathways after seeing Hickman Mills-specific barriers and supports, so I can distinguish metro-level opportunity from local feasibility.
3. As a user, I want to see realistic launch points and bridge roles, so I can picture a believable starting step.
4. As a student, I want to record how the data confirms or challenges my own plan, so the project feels relevant to me.
5. As a student, I want to optionally save my progress with a short code, so I can return later without losing work.
6. As PREP-KC, I want editable YAML-based pathway definitions, so we can revise the classroom framing without touching code.

## 6. Experience principles

- **Phase reveal:** only show the data needed for the current question.
- **Interpretation before detail:** surface pathway summaries first, then offer drill-down.
- **Plain language everywhere:** labels should sound like a teacher prompt, not a database schema.
- **Save uncertainty:** users should be able to note that a pathway is promising but still feels hard to reach.
- **Build for synthesis:** every screen should contribute directly to the final recommendation.

## 7. Functional requirements by screen

### Screen 1 — Pathway Explorer

- Display the seven pathway families with a short summary, wage signal, demand signal, current scale, county fit, 2–4 example roles, and one caution note.
- Capture each user's top criteria, confidence score, initial top two pathways, and a bucket placement for all seven pathways: strongest on paper / mixed / lower priority for now.
- Allow short evidence notes for why a pathway was placed where it was.

### Screen 2 — Hickman Mills Lens

- Only after Screen 1, reveal transportation notes, local access notes, work-based learning flags, bridge roles, support ideas, and major employers for the user's top pathways.
- Capture revised ranking, selected barrier tags, selected support tags, and a short explanation of what changed.
- Support comparison across top pathways rather than reopening all seven equally.

### Screen 3 — Launch Points

- Display institution archetype, level, access note, strongest program families, launch-point reason, likely first-step type, and watch-out.
- Capture selected launch points, selected bridge roles or first steps, and a note on why those starts feel realistic.
- Keep the institution list filtered by chosen pathways to reduce noise.

### Screen 4 — My Pathway Reality Check

- Support an individual reflection tied to one user's real or tentative plan.
- Capture original plan, closest pathway, what the data confirmed, what it complicated, likely first step, support needed, and one open question.
- Allow users to revise without losing earlier entries.

### Screen 5 — Recommendation Builder

- Pre-fill the builder using saved notes from earlier screens.
- Capture final top two pathways, one caution pathway, three supports, two to three launch points, a message PREP-KC should use with students, and one remaining uncertainty.
- Offer a clean print view for the final presentation planner.

## 8. Data requirements

| Source family | Use in the app | Notes |
|--------------|----------------|-------|
| BLS / OEWS / projections | Pathway wage, scale, and demand signals | Pre-baked into `pathway_summaries.yaml`. |
| IPEDS | Institution-level program and award context | Pre-baked into `launch_points.yaml`. |
| College Scorecard | Access, earnings, and outcome context | Used as access/outcome overlay in launch points. |
| Census / ACS / commuting | Local context and feasibility notes | Used selectively in `county_notes.yaml`. |
| PREP-KC authored content | Pathway definitions, bridge roles, county notes, support logic | Editable YAML in `data/mappings/`. |
| kc-industries geocoded employers | Employer context near Hickman Mills | Pre-baked into `employer_context.yaml`. |

## 9. Success criteria

- Users can move through all five screens without needing raw spreadsheet work.
- The final recommendation builder produces content that maps directly into the four-slide presentation planner.
- YAML pathway data loads correctly and displays in plain language.
- Code-based users can save and resume progress across sessions.
- The app is simple enough to iterate quickly as the data model evolves.

## 10. v1 acceptance checklist

- A user can move from landing through all five screens and return later (with a code) without losing work.
- Every screen uses plain-language labels that match the packet and teacher prompts.
- The recommendation builder can print cleanly and map directly into the final four-slide structure.
- YAML files can be edited and the app restarted to see changes without code changes.
- Anonymous users can explore all data without entering a code.

## 11. Build assumptions

- The first version is optimized for guided exploration and one small classroom.
- Pathway summaries and support notes are partly PREP-KC-authored (in YAML), not fully derived from source data at runtime.
- The first release priorities: clarity, data exploration, and optional save over advanced analytics or facilitator tools.
