# AI QA Test Case Generation

A customizable QA AI assistant that helps teams improve requirement quality,
increase test coverage, and standardize manual testing workflows.

Turn a user story into a full QA package — automatically, every time — using
an AI coding agent (Claude Code, Cursor, Windsurf, or similar) plus two small
Python scripts.

Drop a user story JSON into `stories/`, and the agent:
1. Reads your product knowledge doc for context.
2. Writes a **missing-requirements report** — every gap, ambiguity, or
   contradiction in the story, ranked by severity.
3. Generates a **4-sheet Excel workbook** — manual test cases, a
   requirement traceability matrix, the gap analysis, and a QA review
   summary (smoke / regression / security / accessibility / performance).
4. Updates your product knowledge doc with any new facts the story revealed
   (so gap analysis on the *next* story gets sharper, not just this one).

No AI agent required to run the scripts themselves — `generate_excel.py`
and `generate_missing_req.py` work standalone on any story JSON that follows
the schema. The agent is what makes the workflow automatic and adds the
actual gap-analysis judgment.

## Why

Writing thorough test cases and spotting every unstated assumption in a
user story is repetitive, easy to shortcut under deadline pressure, and
inconsistent across people. This toolkit makes "read the story → find every
gap → write every test case → keep the product spec current" a five-minute,
zero-willpower loop instead of an afternoon.

## Quick Start

```bash
git clone https://github.com/akhileshmengji/ai-agents-test-case--genration.git
cd ai-agents-test-case--genration
pip install -r requirements.txt
cp config.example.json config.json   # optional — defaults work out of the box
```

Try it against the included worked example:

```bash
python scripts/generate_missing_req.py examples/acme-lms/stories/course-enrollment-invite.json
python scripts/generate_excel.py examples/acme-lms/stories/course-enrollment-invite.json
```

Check `./output/` for the generated `.md` and `.xlsx` files.

## Adopting this for your own product

1. **Fill in `reference/PRODUCT_KNOWLEDGE.md`** with your product's roles,
   modules, business rules, and non-functional baselines. Use
   `examples/acme-lms/PRODUCT_KNOWLEDGE.md` as a model for level of detail —
   short, factual, testable statements, not marketing copy.
2. **Write story JSON files** in `stories/`, following `stories/_TEMPLATE.json`.
   You can hand-write these, or have your AI agent draft the schema from a
   Jira ticket / PRD / Figma spec — the schema is the contract, not the
   authoring method.
3. **Wire up your AI agent** to run the workflow automatically. If you use
   Claude Code, `CLAUDE.md` in this repo already contains the trigger
   instructions — it activates as soon as you add a new file to `stories/`.
   For other agents, copy the "Instruction" section of `CLAUDE.md` into
   whatever persistent context file your tool reads.
4. **Customize `config.json`** (copied from `config.example.json`) if you
   want output elsewhere, or want the story JSON copied to a downstream
   automation pipeline directory after each run (see `automation_pipeline_dir`
   below).

## Configuration

`config.json` (gitignored — copy from `config.example.json`) controls where
output goes:

| Key | Default | Purpose |
|-----|---------|---------|
| `output_dir` | `./output/test-cases` | Where `.xlsx` workbooks are saved |
| `missing_requirements_dir` | `./output/missing-requirements` | Where gap-analysis `.md` reports are saved |
| `automation_pipeline_dir` | `""` (disabled) | If set, the source story JSON is copied here after each run — for teams with a separate AI/LLM-driven E2E automation pipeline that consumes these files directly |

All relative paths resolve against the repo root, so the scripts behave the
same regardless of your current working directory. Override the config file
location entirely with the `QA_CONFIG_PATH` environment variable.

## Repository Structure

```
.
├── CLAUDE.md                  # Agent instructions (works for Claude Code out of the box)
├── config.example.json        # Copy to config.json and customize
├── scripts/
│   ├── generate_excel.py      # Story JSON -> 4-sheet .xlsx workbook
│   ├── generate_missing_req.py# Story JSON -> missing-requirements .md
│   └── qa_config.py           # Shared config loader
├── stories/
│   └── _TEMPLATE.json         # Schema reference for your own stories
├── reference/
│   └── PRODUCT_KNOWLEDGE.md   # Fill this in for your own product
└── examples/
    └── acme-lms/               # A complete, fictional worked example
        ├── PRODUCT_KNOWLEDGE.md
        └── stories/course-enrollment-invite.json
```

## Story JSON Schema

See `stories/_TEMPLATE.json` for the annotated schema, and
`CLAUDE.md` for the key-field reference table. In short, each story has:

- `meta` — story ID, module, feature, quality score
- `test_cases[]` — one entry per test case (functional, negative,
  edge-boundary, security, accessibility, performance, E2E, etc.)
- `gaps[]` — requirement gaps found in the story, with severity
- `qa_review` — optional curated smoke/regression/security/a11y/perf lists

## License

MIT — see `LICENSE`.
