"""
generate_missing_req.py  -  Missing Requirements MD writer

Reads a story JSON, extracts every gap (missing / ambiguous / contradictory /
untestable requirement), and writes a formatted Markdown report to
<missing_requirements_dir> (see config.json / config.example.json).

Usage:
    python generate_missing_req.py stories/<file>.json
"""

import json
import os
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_config import load_config

SEVERITY_EMOJI = {"High": "[High]", "Medium": "[Med]", "Low": "[Low]"}

GAP_TYPE_LABELS = {
    "Missing": "Missing",
    "Missing acceptance criteria": "Missing AC",
    "Ambiguous": "Ambiguous",
    "Contradictory": "Contradictory",
    "Untestable": "Untestable",
}


def _severity_order(g):
    return {"High": 0, "Medium": 1, "Low": 2}.get(g.get("severity", "Low"), 9)


def build_md(data: dict) -> str:
    meta = data.get("meta", {})
    story_id = meta.get("story_id", "UNKNOWN")
    title = meta.get("title", "")
    source = meta.get("source", "")
    gaps = sorted(data.get("gaps", []), key=_severity_order)

    high   = [g for g in gaps if g.get("severity") == "High"]
    medium = [g for g in gaps if g.get("severity") == "Medium"]
    low    = [g for g in gaps if g.get("severity") == "Low"]

    quality_score = meta.get("quality_score")
    module        = meta.get("module", "")
    feature       = meta.get("feature", "")

    lines = []

    # -- Header ---------------------------------------------------------
    lines += [
        f"# Missing Requirements - {story_id}",
        "",
        f"**Story:** {title}",
    ]
    if module:
        lines.append(f"**Module:** {module}")
    if feature:
        lines.append(f"**Feature:** {feature}")
    lines += [
        f"**Source:** {source}",
        f"**Generated:** {date.today().isoformat()}",
    ]
    if quality_score is not None and quality_score != 0:
        bar_filled = int(quality_score / 10)
        bar = "#" * bar_filled + "." * (10 - bar_filled)
        lines.append(f"**Requirement Quality Score:** {quality_score}/100  `{bar}`")
    lines += [
        f"**Total gaps:** {len(gaps)}  "
        f"({len(high)} High - {len(medium)} Medium - {len(low)} Low)",
        "",
        "---",
        "",
    ]

    if not gaps:
        lines.append("> No requirement gaps detected.")
        return "\n".join(lines)

    # -- Summary table ----------------------------------------------------
    lines += [
        "## Summary",
        "",
        "| # | Req Ref | Gap Type | Severity | Issue (short) |",
        "|---|---------|----------|----------|---------------|",
    ]
    for i, g in enumerate(gaps, 1):
        sev = g.get("severity", "")
        emoji = SEVERITY_EMOJI.get(sev, "")
        gap_type = GAP_TYPE_LABELS.get(g.get("gap_type", ""), g.get("gap_type", ""))
        issue_short = g.get("issue", "")[:80].rstrip()
        if len(g.get("issue", "")) > 80:
            issue_short += "..."
        lines.append(
            f"| {i} | {g.get('req_ref','')} | {gap_type} | {emoji} {sev} | {issue_short} |"
        )

    lines += ["", "---", ""]

    # -- Detailed gaps ------------------------------------------------------
    lines += ["## Detailed Gaps", ""]

    for i, g in enumerate(gaps, 1):
        sev = g.get("severity", "")
        emoji = SEVERITY_EMOJI.get(sev, "")
        lines += [
            f"### GAP-{i} - {g.get('req_ref', '')} - {emoji} {sev}",
            "",
            f"**Gap type:** {g.get('gap_type', '')}",
            "",
            f"**Requirement as written:**",
            f"> {g.get('requirement_text', 'NOT SPECIFIED')}",
            "",
            f"**Issue:**  ",
            g.get("issue", ""),
            "",
            f"**Suggested fix:**  ",
            g.get("suggested_fix", ""),
            "",
            "---",
            "",
        ]

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_missing_req.py stories/<file>.json")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if not in_path.exists():
        print(f"ERROR: file not found - {in_path}")
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md_content = build_md(data)

    story_id = data.get("meta", {}).get("story_id", in_path.stem)
    out_filename = f"{story_id}_missing_requirements.md"

    config = load_config()
    output_dir = Path(config["missing_requirements_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / out_filename

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    gaps = data.get("gaps", [])
    high   = sum(1 for g in gaps if g.get("severity") == "High")
    medium = sum(1 for g in gaps if g.get("severity") == "Medium")
    low    = sum(1 for g in gaps if g.get("severity") == "Low")

    print(f"OK  ->  {out_path}")
    print(f"     {len(gaps)} gaps  ({high} High - {medium} Medium - {low} Low)")


if __name__ == "__main__":
    main()
