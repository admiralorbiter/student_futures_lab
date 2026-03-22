# Design Decisions

Canonical record of all resolved and open design decisions. This replaces the scattered "Open Decisions" sections previously in the PRD, backlog, and architecture docs.

---

## Resolved

### D1. Student Identity Model

**Decision:** Optional code — anonymous exploration with optional save code.

Anyone can explore the app without logging in. If a classroom student wants to save progress, they enter a short code (teacher-created or self-chosen). The explore mode shows all data screens; only personal reflections and recommendations require a code. Codes are not PII.

**Rationale:** Keeps the tool open to the public while supporting the classroom use case. Zero friction for casual users; persistence for students who need it.

---

### D2. Facilitator Features in v1

**Decision:** Skip facilitator UI; keep response-saving schema.

No facilitator dashboard, no CSV export UI, no facilitator login in v1. The paper packet and PREP-KC Insight Capture Sheet handle classroom collection. Student responses are saved silently to SQLite (for code-based users) so the data exists when a facilitator dashboard is added later. The facilitator can query the SQLite file directly if needed.

**Rationale:** Dramatically reduces v1 scope. The class materials already handle the collection workflow.

---

### D3. Employer / Location Layer

**Decision:** Static text list in v1; interactive layer in v2.

For v1, show a pre-extracted plain-language list of major employers per pathway family near Hickman Mills on Screen 2 (Hickman Mills Lens). Data comes from existing geocoded employers in the `kc-industries` repo (300+ employers with lat/lon, FIPS, NAICS). No map component needed.

**Rationale:** Easy win from existing data. Adds local context without building a map.

---

### D4. Data Architecture

**Decision:** Pre-baked YAML/JSON for pathway data + SQLite for student responses.

- **Pathway, institution, and employer data:** Exported once from `kc-industries`, hand-edited with PREP-KC language, stored as YAML/JSON in `data/mappings/`.
- **Student responses:** SQLite database (only used if student enters a code).
- **No runtime dependency** on `kc-industries`.

**Rationale:** Simplest possible architecture. PREP-KC staff can edit YAML files directly. No data pipeline needed for v1.

---

### D5. Source Refresh Cadence

**Decision:** One-time classroom snapshot.

Data from `kc-industries` is current enough (BLS 2023, IPEDS 2022–23, Scorecard 2022–23 cohorts). Export once, curate with PREP-KC content, freeze. Re-export if the class runs again next year.

**Rationale:** Don't build a refresh pipeline for a single classroom run.

---

### D6. Editable Fields

**Decision:** YAML files in `data/mappings/`.

Pathway summaries, caution notes, county notes, support tag definitions, bridge role descriptions, and launch-point reasons are stored as YAML. The app loads them at startup. PREP-KC staff can edit in any text editor or directly in GitHub.

**Rationale:** Version-controlled, simple, no admin UI needed.

---

### D7. Single Classroom vs. Reusable

**Decision:** No multi-tenant abstraction. Add a `cohort` field to responses.

The app is already reusable by design since anyone can explore anonymously. For tracking separate classroom runs, add a `cohort` or `session_label` field to the responses table. One column, no extra UI.

**Rationale:** Don't over-engineer for a hypothetical future. One field preserves the option.

---

### D8. Unmapped CIP Program Visibility

**Decision:** Show unmapped CIP areas as browsable "Additional Fields of Study."

Programs in CIP areas not mapped to the 7 pathway families (Psychology, Visual Arts, Culinary, Communication, Liberal Arts, Recreation, Social Sciences, Theology, Agriculture — ~112 programs total) are surfaced to students as an "Additional Fields" section. Each field has a student-facing description, program count, and `related_pathways` links back to the 7 families. A `visible` flag lets PREP-KC hide individual fields (e.g., Theology is hidden by default).

**Rationale:** Students should see the full landscape of what's available, not just the 7 focus pathways. Hiding 112 programs (25% of the dataset) would give an incomplete picture. The `related_pathways` links help students understand how these areas connect back to the main pathways.

---

### D9. Hybrid Data Architecture

**Decision:** YAML for curated editorial content + read-only SQLite for granular drill-down data.

The original D4 decision used YAML-only for all pathway data. With 889 programs, 634 occupations, and 5,610 employers now imported, the architecture was upgraded:
- **YAML** (`data/mappings/`): Pathway summaries, support tags, county notes, glossary — content PREP-KC edits by hand.
- **Read-only SQLite** (`data/pathway_data.db`): Granular program-level earnings, institution details, occupation wages/projections, employer headcounts — exported from kc-industries via `scripts/export_pathway_data.py`.
- **Read-write SQLite** (`data/student_responses.db`): Student responses (unchanged from D4).

`PathwayService` queries both: YAML indexes at startup, database on demand. Database connections use `mode=ro` for safety.

**Rationale:** Students should be able to dig as deep as they want — from "Healthcare is strong" → specific programs → linked occupations → local employers. YAML doesn't scale for thousands of rows. The export script makes refresh repeatable.

---

## Open

*No open decisions remain at this time. New decisions should be added here as they arise during development.*
