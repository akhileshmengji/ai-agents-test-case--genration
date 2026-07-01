# AI QA Test Case Generation

This file is written for Claude Code, but the pattern is portable to any AI
coding agent that reads a persistent instructions file (e.g. `.cursorrules`,
`.windsurfrules`, an Aider config, or a custom system prompt). Copy the
"Instruction" section into whichever file your agent honors.

## Product Knowledge
Always read `reference/PRODUCT_KNOWLEDGE.md` before analysing any user story.
(See `examples/acme-lms/PRODUCT_KNOWLEDGE.md` for a fully filled-in example.)

## Story Files
User story JSON files live in `stories/`. Use `stories/_TEMPLATE.json` as the
schema reference. (See `examples/acme-lms/stories/course-enrollment-invite.json`
for a fully filled-in example.)

## Configuration
Copy `config.example.json` to `config.json` and adjust `output_dir`,
`missing_requirements_dir`, and (optionally) `automation_pipeline_dir` to
match your machine/team setup. `config.json` is gitignored — each
contributor/agent keeps their own.

---

## Instruction: Full QA Artifacts on Every New User Story

**Trigger:** Whenever a new user story JSON file is added to `stories/`, do
the following automatically — no need to ask:

1. **Read the story file** (the new `.json` in `stories/`).
2. **Read `reference/PRODUCT_KNOWLEDGE.md`** for platform context.
3. **Identify every missing requirement** — anything that is:
   - Not specified / left undefined
   - Ambiguous or contradictory
   - Untestable as written
   - A gap already noted in the `gaps` array of the JSON
   — plus any additional gaps spotted by cross-referencing the product
   knowledge.
4. **Run the missing-requirements script:**
   ```
   python scripts/generate_missing_req.py stories/<new-file>.json
   ```
   Saves to: `<missing_requirements_dir>` (default `./output/missing-requirements/`)

5. **Run the Excel script:**
   ```
   python scripts/generate_excel.py stories/<new-file>.json
   ```
   Saves to: `<output_dir>/<story_id>_test_cases.xlsx` (default `./output/test-cases/`)

6. **Update `reference/PRODUCT_KNOWLEDGE.md`** if the story reveals new
   product knowledge not already captured there:
   - New rules, constraints, or business logic for any module
   - New user capabilities or role restrictions
   - New platform behaviours (e.g. session rules, timer behaviour, invite logic)
   - Only add facts that are confirmed by the story's acceptance criteria or
     business rules — do not infer or speculate
   - Append new facts under the most relevant existing section, or create a
     new numbered section if none fits
   - Do **not** remove or overwrite existing content unless the story
     explicitly contradicts it

7. **Report back** with a short summary:
   - Total test cases and type distribution (Functional, Negative,
     Edge-Boundary, etc.)
   - Total gaps and severities (High / Medium / Low)
   - Names of both output files
   - Any additions made to `PRODUCT_KNOWLEDGE.md` (or "No updates needed" if
     unchanged)

**A note on the JSON itself:** if `automation_pipeline_dir` is configured,
the story JSON is copied there after every run for a downstream AI/LLM-driven
E2E automation pipeline to consume directly. When that's the case, keep
`steps`, `test_data`, and `expected_result` literal and concrete (specific
values, exact UI actions, precise expected outcomes) rather than vague prose
— a downstream LLM may act on these fields directly, not just a human
reviewer.

---

## JSON Schema — Key Fields

| Field | Location | Description |
|-------|----------|-------------|
| `meta.story_id` | meta | Unique ID, used in output filenames |
| `meta.module` | meta | Top-level module (e.g. Checkout, Auth, Invite) |
| `meta.feature` | meta | Feature name (e.g. Guest Checkout Flow) |
| `meta.quality_score` | meta | Requirement quality 0–100 (set when known) |
| `test_cases[].module` | test case | Module (inherits from meta if omitted) |
| `test_cases[].sub_module` | test case | Sub-module (optional) |
| `test_cases[].feature` | test case | Feature (inherits from meta if omitted) |
| `test_cases[].platform` | test case | Web \| Android \| iOS \| All |
| `test_cases[].user_role` | test case | Role name defined in your product knowledge doc |
| `test_cases[].test_scenario` | test case | One-liner scenario description |
| `test_cases[].severity` | test case | Critical \| High \| Medium \| Low |
| `test_cases[].requirement_mapping` | test case | Comma-separated AC/BR IDs (e.g. "AC-1, BR-2") |
| `test_cases[].automation_candidate` | test case | Yes \| No \| Conditional |
| `test_cases[].tags` | test case | Optional array: ["Smoke", "Regression", "Security"] |
| `qa_review` | root | Optional: smoke_tests, regression_tests, security_checks, etc. |

---

## Scripts
| Script | Purpose |
|--------|---------|
| `scripts/generate_excel.py` | Reads a story JSON → writes 4-sheet `.xlsx` (Manual Test Cases · Traceability Matrix · Requirement Gaps · QA Review) |
| `scripts/generate_missing_req.py` | Reads a story JSON → writes a missing-requirements `.md` with quality score, summary table, and detailed gaps |
| `scripts/qa_config.py` | Shared config loader used by both scripts (reads `config.json`, falls back to relative defaults) |

## Output Locations
| Artifact | Location |
|----------|----------|
| Excel test-case files | `<output_dir>` (default `./output/test-cases/`) |
| Missing requirements MD | `<missing_requirements_dir>` (default `./output/missing-requirements/`) |
| Story JSON (optional automation copy) | `<automation_pipeline_dir>` if configured; disabled by default |

## Excel Workbook Structure
| Sheet | Contents |
|-------|----------|
| Manual Test Cases | 21-column sheet: S.No, Module, Sub Module, Feature, User Story ID, Platform, User Role, Priority, Severity, Preconditions, Test Case ID, Test Scenario, Test Case Description, Test Data, Test Steps, Expected Result, Actual Result, Status, Comments, Requirement Mapping, Automation Candidate |
| Traceability Matrix | AC/BR ID → Mapped Test Cases → Coverage Status (auto-generated) |
| Requirement Gaps | Gap analysis with severity colour coding |
| QA Review | Smoke · Regression · Security · Accessibility · Performance · Exploratory summary |
