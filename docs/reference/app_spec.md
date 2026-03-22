# Guided Inquiry App Specification

*Application build and data-capture notes for the Hickman Mills project.*

> The app should guide student thinking in phases and save useful student insight for PREP-KC.

## Design principles

- Build a guided explorer, not a giant dashboard.
- The interface should support interpretation, not replace it.
- Students should see pathway families first, then a Hickman Mills lens, then launch points, then their own reflection, then a recommendation builder.
- Default to plain language: "What looks strong?" is better than a field name that sounds technical.
- Keep the number of visible choices small. Users can dig deeper, but they should not face every variable at once.
- Make student input saveable (for code-based users) from the beginning.

## Minimum viable build order

| Ready before… | Must-have screen / feature | Why it matters |
|----------------|---------------------------|----------------|
| Class 1 | Optional code entry + Screen 1 Pathway Explorer + ranking capture | Users need to record criteria and make a first pathway read. |
| Class 2 | Screen 2 Hickman Mills Lens + barrier / support tagging | Local-access logic becomes real; much of the usable PREP-KC insight emerges here. |
| Class 3 | Screen 3 Launch Points and Bridge Roles | Users need a realistic way to connect promising pathways to believable starting places. |
| Class 4 | Screen 4 My Pathway Reality Check | Personal reflection should be structured, saveable, and easy to revisit. |
| Class 5 | Screen 5 Recommendation Builder + print view | Final synthesis space that can turn into slides and a usable record. |

## Screen-by-screen build map

### 1. Pathway Explorer

| | |
|---|---|
| **Student question** | What looks strongest on paper? |
| **Display data** | Pathway family, plain-language summary, current scale, wage signal, projected demand / openings signal, county fit, 2–4 example roles, caution note. |
| **Student inputs to save** | Top criteria, initial top 2, pathway bucket for each of the 7 pathways, confidence score, evidence notes. |
| **Data source** | `pathway_summaries.yaml` |

### 2. Hickman Mills Lens

| | |
|---|---|
| **Student question** | Would this still look strong for Hickman Mills students? |
| **Display data** | Transportation notes, county role, local access notes, bridge roles, internship/work-based learning flags, support ideas, major employers. |
| **Student inputs to save** | Top 3 selected pathways, barrier tags, support tags, revised ranking, short explanation of what changed. |
| **Data source** | `county_notes.yaml`, `support_tags.yaml`, `employer_context.yaml` |

### 3. Launch Points

| | |
|---|---|
| **Student question** | Where could someone realistically start? |
| **Display data** | Institution archetype, 2-year/4-year, Pell/access note, strongest program families, launch-point reason, bridge role or first-step note, watch-out. |
| **Student inputs to save** | Chosen launch points, chosen bridge roles, explanation of why these feel realistic, remaining questions. |
| **Data source** | `launch_points.yaml` |

### 4. My Pathway Reality Check

| | |
|---|---|
| **Student question** | What does this mean for me? |
| **Display data** | Selected pathway, likely first step, route length note, county/access note, support options. |
| **Student inputs to save** | Original plan, closest pathway, what the data confirmed, what it complicated, first realistic step, support needed, open question. |

### 5. Recommendation Builder

| | |
|---|---|
| **Student question** | What should PREP-KC do? |
| **Display data** | Saved notes from previous screens, pathway selections, support tags, launch-point selections, editable message fields. |
| **Student inputs to save** | Top 2 pathways, caution pathway, 3 supports, 2–3 launch points, final student message, uncertainty / next question. |

## Recommended data model

Use this as a practical schema sketch for the student response SQLite database and the YAML data files.

### SQLite tables (student responses)

| Table | Core fields | Purpose |
|-------|-------------|---------|
| `students` | code, cohort, created_at | Optional code-based identity |
| `responses` | student_code, screen_id, response_type, selected_value, note_text, timestamp | Screen-by-screen saved selections and written reasoning |

### YAML data files

| File | Core fields | Purpose |
|------|-------------|---------|
| `pathway_families.yaml` | id, name, cip_prefixes, display_order | Maps CIP codes to 7 pathway families |
| `pathway_summaries.yaml` | pathway_id, summary, current_scale, wage_signal, demand_signal, county_fit_summary, caution_note, example_roles | Main comparison object on Screens 1 and 2 |
| `support_tags.yaml` | id, tag_name, definition | Standardized barriers and supports |
| `county_notes.yaml` | pathway_id, transport_flag, internship_flag, local_access_note, hickman_mills_note | Local reachability and support logic |
| `launch_points.yaml` | pathway_id, institution_name, archetype, level, pell_band, reason, first_step_type, watch_out | Connects pathways to realistic starts |
| `employer_context.yaml` | pathway_id, employers[] (name, location, sector) | Major employers near Hickman Mills by pathway |
| `glossary.yaml` | term, definition, question_to_ask | Student-facing contextual help |

## Barrier and support tags worth standardizing

| Suggested tag | Plain-language definition |
|---------------|--------------------------|
| Transportation / commute | Getting to the pathway, training site, or workplace is the main challenge. |
| Cost / affordability | The pathway or start point may be too expensive without support. |
| Schedule / time | A student would struggle to fit the pathway around school, work, or family responsibilities. |
| Information / awareness | Students may not know the pathway exists or may not understand how to enter it. |
| Confidence / belonging | The pathway may feel hard to picture or socially distant from who the student sees themselves as. |
| Prerequisites / selectivity | Grades, tests, prerequisites, or competitive entry rules make the path harder to access. |
| Work-based learning access | Internships, clinical placements, apprenticeships, or employer openings may be limited. |
| Advising / navigation | Students need someone to help them map steps, applications, and transitions. |

## Plain-language labels to use in the interface

| Avoid showing… | Instead label it as… |
|----------------|---------------------|
| `linked_occupation_count` | How many kinds of jobs connect to this pathway |
| `wage_median` | Typical wage signal |
| `annual_openings_projection` | How strong demand looks over time |
| `institution_type_archetype` | What kind of start this school offers |
| `support_tag` | What support would help? |
| `local_access_note` | What could get in the way from Hickman Mills? |

## Export views to build (v1: print only)

- A clean print view that mirrors the student packet.
- A team summary view that can translate directly into the 4-slide presentation planner.

## Guardrails

- Do not auto-score pathways into a final answer. Let users make the recommendation.
- Do not surface the adult synthesis as a default recommendation.
- Do not show every institution, every county, and every filter at once.
- Do not hide disagreement. Save notes and uncertainty, not only final picks.
- Do not let the app sound more certain than the data really is.

## Nice-to-have later, not required for v1

- Interactive maps or employer layers once the inquiry flow is working.
- Compare view for two pathways side by side.
- Saved screenshots or slide exports.
- A teacher dashboard that summarizes class responses automatically.
- CSV/JSON export for PREP-KC analysis.
