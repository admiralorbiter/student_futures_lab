# Delivery Roadmap and Epics

*A practical build plan for a first classroom-ready release, followed by iteration.*

> **Planning principle**
> Build the app in the same order that students encounter the inquiry. Every increment should be testable with real classroom artifacts.
> A small, trustworthy v1 is better than a broad but unfinished dashboard.

## 1. Milestones

| Milestone | Target outcome |
|-----------|---------------|
| M0 — Foundations | Repo, app skeleton, YAML data files, styling foundation. |
| M1 — Opportunity flow | Screen 1 working with pathway explorer and saved rankings. |
| M2 — Hickman Mills feasibility | Screen 2 working with barrier/support tags and employer context. |
| M3 — Launch points | Screen 3 working with pathway-filtered institution views. |
| M4 — Reflection and synthesis | Screens 4 and 5 with final recommendation builder. |
| M5 — Classroom hardening | Seeded data, test pass, print view polish, backup plan. |

## 2. Epic list

### Epic A — Product foundation and experience shell ✅

- ~~Create Flask app shell, base template, typography, navigation, and screen progression.~~
- ~~Set up SQLite schema for student responses (optional save-code model).~~
- ~~Implement anonymous browsing + optional code save.~~

### Epic B1 — Data curation and seed files ✅

- ~~Run `export_from_kc_industries.py` to extract pathway and institution data.~~
- ~~Create the CIP → pathway family mapping (`pathway_families.yaml`).~~
- ~~Author PREP-KC editorial content: pathway summaries, caution notes, county notes, support tag definitions.~~
- ~~Create `employer_context.yaml` from geocoded employer data.~~
- ~~Create `glossary.yaml` from the Student Glossary document.~~
- ~~Added `additional_fields` (9 unmapped CIP areas) as browsable student data.~~

### Epic B2 — Full data pipelines (post-v1)

- ~~Build repeatable ingest scripts if the tool will be refreshed annually.~~ `export_pathway_data.py` ships with v1.
- Automate export as a CI/build step (if refreshed annually).
- Add source provenance tracking (which kc-industries commit produced which export).

### Epic C — Screen 1: Pathway Explorer

- Render seven pathways with plain-language signals and evidence notes.
- Capture top criteria, pathway buckets, confidence, and initial top two.
- Load pathway data from `pathway_summaries.yaml`.

### Epic D — Screen 2: Hickman Mills Lens

- Reveal county/access/support context only after initial ranking.
- Show static employer context from `employer_context.yaml`.
- Capture barrier tags, support tags, revised ranking, and what changed.

### Epic E — Screen 3: Launch Points and Bridge Roles

- Filter institution and first-step options by selected pathways.
- Load institution data from `launch_points.yaml`.
- Capture realistic launch points, bridge roles, and unresolved questions.

### Epic F — Screen 4: My Pathway Reality Check

- Create personal reflection flow with save and edit.
- Connect reflection prompts back to pathway and launch-point choices.

### Epic G — Screen 5: Recommendation Builder

- Assemble saved evidence into a final recommendation flow.
- Support clean print view for the final presentation planner.

### Epic H — Facilitator tools and analytics (post-v1)

- Student and facilitator logins.
- Teacher summary page showing progress and class patterns.
- CSV/JSON export for PREP-KC analysis.

### Epic I — QA, classroom rehearsal, and iteration

- Test the app end to end with mock student data.
- Tune wording, reduce confusion, and polish print views.

## 3. Suggested build sequence

1. Lock the YAML data files and pathway labels before building interactions.
2. Stand up the app skeleton and one seed dataset early so screen work has something real to render.
3. Complete Screens 1 and 2 before spending significant time on institutions or exports.
4. Build Screen 3 only after the pathway-to-launch-point mapping is credible.
5. Build reflection and recommendation last, but define the response fields now so earlier screens capture the right data.
6. Do at least one full dry run using the classroom packet before calling v1 done.

## 4. Definition of done by epic

| Epic | Done means… |
|------|------------|
| A | ~~Local app boots, base layout works, and users can explore or enter a code.~~ **Done.** |
| B1 | ~~YAML files exist, load without error, and pathway summaries are readable.~~ **Done.** |
| C | Users can complete Screen 1 and data persists (for code-based users). |
| D | Users can re-rank pathways with barrier/support tagging and saved reasoning. |
| E | Users can select launch points and bridge roles filtered by pathway. |
| F | Users can complete and edit personal reflections. |
| G | The recommendation builder produces a clean print view. |
| H | (Post-v1) Facilitator can review progress and export. |
| I | At least one rehearsal run finds no blocking usability or data issues. |

## 5. Risk register

| Risk | Why it matters | Mitigation |
|------|---------------|------------|
| Data sprawl | Too many fields or sources slow the build. | Start with a small YAML presentation layer and enrich later. |
| Pathway mapping churn | Definitions may change as PREP-KC learns more. | Keep all mapping content in editable YAML. |
| Institution overload | Too many schools confuse students. | Filter aggressively; show archetypes first. |
| Weak classroom flow | A technically working app may still feel confusing. | Prototype screen copy from the packet language. |
| Export mismatch | Final slides may require rework if outputs are too raw. | Design the print view in parallel with Screens 4 and 5. |

## 6. Post-v1 enhancements

- Interactive employer and geography layer (map component).
- Side-by-side pathway comparison.
- Facilitator dashboard charts summarizing rankings and tags.
- Student/facilitator login system.
- Reusable class templates for future cohorts or districts.

## 7. Classroom rehearsal checklist

- Use one mock user who changes their mind between Screens 1 and 2.
- Use one mock user whose personal plan does not match the group recommendation.
- Print the final recommendation and compare it against the presentation planner.
- Verify that saved fields (for code-based users) persist correctly.
