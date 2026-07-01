"""
qa_config.py - Shared configuration loader for the QA test-case generation scripts.

Looks for a `config.json` in the repository root (one level up from `scripts/`).
Falls back to sensible relative defaults if no config file exists, so the
toolkit works out of the box with zero setup.

Override the config file location with the QA_CONFIG_PATH environment variable
(useful in CI or when multiple teams share the scripts with different configs).
"""
import json
import os

_DEFAULTS = {
    "output_dir": "./output/test-cases",
    "missing_requirements_dir": "./output/missing-requirements",
    # Optional: if set, the source story JSON is copied here after each run.
    # Useful for teams with a separate AI/LLM-driven E2E automation pipeline
    # that consumes these story files directly. Leave blank to disable.
    "automation_pipeline_dir": "",
}


def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    config_path = os.environ.get("QA_CONFIG_PATH") or os.path.join(_repo_root(), "config.json")

    config = dict(_DEFAULTS)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config.update(json.load(f))

    # Resolve relative paths against the repo root, not the caller's CWD,
    # so the scripts behave the same whether run from repo root or elsewhere.
    for key in ("output_dir", "missing_requirements_dir", "automation_pipeline_dir"):
        value = config.get(key) or ""
        if value and not os.path.isabs(value):
            config[key] = os.path.normpath(os.path.join(_repo_root(), value))

    return config
