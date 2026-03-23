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

### D10. Drag-and-Drop Criteria Ranking

**Decision:** Use SortableJS drag-and-drop instead of dropdown selects for Step 1 criteria ranking.

Students drag items up/down to rank 7 criteria by personal importance. Rank is determined by position — no duplicate or missing values possible. Order is stored as a comma-separated list of IDs in a hidden input.

**Rationale:** Dropdowns allowed overlapping ranks (e.g., two items both ranked #1). Drag-and-drop is more intuitive for students and eliminates data validation issues. SortableJS is 3KB, zero-dependency, MIT licensed.

---

### D11. Explore → Assess Two-Phase Layout

**Decision:** Split Step 2 into "Explore" (read-only pathway cards) then "Assess" (compact assessment table).

The original design intermixed data exploration with student input on each card. The redesign separates them: students read through all 7 pathway data cards first, then place each pathway in a bucket using a single assessment table below the cards. The table includes jump-back links to reference data.

A "Quick Stats" bar on each card surfaces aggregate database numbers (program count, institution count, occupation count, wage range, growth %) alongside the editorial YAML signals.

**Rationale:** The student packet's intent is "look at all the evidence first, then compare." Mixing explore and judge per card encouraged premature judgment. The table layout matches the paper packet's assessment worksheet.

---

### D12. Screen 2 Auto-Select with Override

**Decision:** Screen 2 auto-selects the pathways the student marked "Strongest" on Screen 1, but students can swap pathways in or out.

`_get_screen1_top_pathways()` reads Screen 1 bucket responses and returns the "strongest" IDs. If fewer than 3, it fills in from "mixed." Students see their auto-selection pre-loaded but can change it via toggle controls.

**Rationale:** The student packet says "Only use the top 3 pathways from Step 2." Auto-selecting respects that flow while allowing students who changed their minds to override without going back to Screen 1.

---

### D13. Group-Level Barrier/Support Tagging

**Decision:** Move barrier/support tag chips from per-pathway (repeated 7×) to a single group-level section.

**Rationale:** The 7 barriers and 7 supports (transportation, cost, schedule, etc.) describe Hickman Mills realities, not pathway-specific data. Students were clicking the same tags for every pathway. Consolidating into one "Biggest barriers for HM students" + "Supports that would help most" picker (pick top 3) creates a meaningful synthesis exercise instead of repetitive clicking.

**Impact:** Per-pathway assessment now has only free-text fields ("What still looks strong?" / "What could get in the way?"). Student packet Step 3 updated to align.

---

### D14. Per-Pathway Charts on Screen 3 (Not Per-Institution)

**Decision:** Screen 3 charts aggregate data across all institutions within a pathway, rather than showing separate charts per institution.

**Rationale:** The student question is "How accessible is this pathway?" not "How big is MCC?" Aggregating by pathway keeps the chart count manageable (one chart set per pathway) and focuses on credential-level accessibility. Per-institution charts would create 2–3× more charts with less pedagogical value.

**Impact:** `get_launch_point_chart_data()` queries programs by credential type and by institution per pathway family.

---

### D15. Institution Detail Page — IPEDS as Primary Data Source

**Decision:** Build a dedicated institution detail page (`/institution/<id>`) accessible from Screen 3 launch point cards, using IPEDS `institution_profiles.csv` (217 institutions × 79 columns) as the primary data source. Generic KC-area sector profiles and nearby employers are excluded.

**Rationale:** Three iterations were needed to find the right approach:
1. **v1 (occupation crosswalk only)** — Programs + linked occupations via SOC codes. Rich career data but only 3 programs for JCCC — felt thin.
2. **v2 (sector cards + employers)** — Added 19 NAICS sector profiles and nearby employers. But these are KC-wide data, not institution-specific. User correctly flagged: "industry cards aren't unique to the institution."
3. **v3 (IPEDS data)** — Imported curated IPEDS profiles. Enrollment, demographics, graduation rates, financial aid, completions — all institution-specific. Exactly what was wanted.

**Impact:** New `ipeds_profiles` table in `pathway_data.db`, matched via `institutions.scorecard_unitid`. Template shows: scorecard banner, demographics donut, completions bar, financial aid bar, enrollment/outcomes stat cards, plus existing career outcomes + program cards.

---

## Open

*No open decisions remain at this time. New decisions should be added here as they arise during development.*

