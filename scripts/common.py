#!/usr/bin/env python3
"""common.py — shared helpers for the FPV drone addon validators.

Standard library only.
Exit codes used by every check: 0 = pass, 1 = fail, 2 = setup missing.
A bool is NEVER a number here (Python treats True as 1 — that bug
is exactly what the Monday v1.2.7/v0.3.6 fixes address in the base
skill and the PC addon, so this addon rejects bools from day one).
"""
import json
import math
import sys
from pathlib import Path

VERSION = "0.0.1"
CREDIT = "Made by PTS6845 — https://battingchart300.github.io"


def is_int(v):
    """True only for real ints — bool is excluded on purpose."""
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    """True only for finite real numbers — bool, NaN and inf excluded."""
    return (isinstance(v, (int, float)) and not isinstance(v, bool)
            and math.isfinite(v))


def is_nonempty_str(v):
    return isinstance(v, str) and v.strip() != ""


def is_unverified(v):
    return isinstance(v, str) and v.strip().upper() == "UNVERIFIED"


def load_spec(path):
    """Load a drone spec JSON. Returns (data, exit_code).

    A non-object root (array, scalar) is a setup error (exit 2),
    never a traceback and never a silent pass.
    """
    p = Path(path)
    if not p.is_file():
        print(f"SETUP ERROR: spec file not found: {path}")
        return None, 2
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"SETUP ERROR: spec is not valid JSON: {e}")
        return None, 2
    if not isinstance(data, dict):
        print("SETUP ERROR: spec root must be a JSON object, "
              "not an array or scalar.")
        return None, 2
    return data, 0


def load_config():
    """Load scripts/config.json next to this file."""
    here = Path(__file__).resolve().parent
    cfg_path = here / "config.json"
    if not cfg_path.is_file():
        print(f"SETUP ERROR: missing config: {cfg_path}")
        return None
    try:
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"SETUP ERROR: config is not valid JSON: {e}")
        return None


class Report:
    """Collect errors/warnings, print them, return the exit code."""

    def __init__(self, name):
        self.name = name
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)
        print(f"  ERROR: {msg}")

    def warning(self, msg):
        self.warnings.append(msg)
        print(f"  WARNING: {msg}")

    def finish(self):
        n_e, n_w = len(self.errors), len(self.warnings)
        verdict = "PASS" if n_e == 0 else "FAIL"
        print(f"Audit log: {self.name}={verdict} "
              f"({n_e} errors, {n_w} warnings), exit={0 if n_e == 0 else 1}")
        return 0 if n_e == 0 else 1


def check_base_or_exit(argv_base_skill):
    """Hard dependency: no base skill -> exit 2, run nothing.

    Returns the base skill path (unused by most checks, but proves
    the dependency was verified). Exits the process on failure.
    """
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    import require_base
    path, version = require_base.find_base_skill(argv_base_skill)
    if path is None:
        print("BASE SKILL MISSING — STOP")
        print("This addon does not work without ai-pcb-design-skill v1.2.1+.")
        print("Load the base skill first, or pass --base-skill <path>,")
        print("or set AI_PCB_SKILL_PATH. No addon check ran.")
        sys.exit(2)
    if version is None or version < require_base.REQUIRED_VERSION:
        have = ".".join(map(str, version)) if version else "unknown"
        need = ".".join(map(str, require_base.REQUIRED_VERSION))
        print(f"BASE SKILL TOO OLD — STOP: found v{have}, need v{need}+")
        sys.exit(2)
    return path
