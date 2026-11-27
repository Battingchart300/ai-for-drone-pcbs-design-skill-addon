"""Shared helpers for the FPV addon pytest suite."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BASE_SKILL = ROOT.parent / "ai-pcb-design-skill"
EXAMPLE_5IN = ROOT / "examples" / "spec_5inch_freestyle.json"
EXAMPLE_HEX = ROOT / "examples" / "spec_hexacopter_inspection.json"


def load_example(path=EXAMPLE_5IN):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_spec(tmp_path, spec, name="spec.json"):
    p = tmp_path / name
    p.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return str(p)


def set_path(spec, dotted, value):
    """Set a dotted path (list indices as digits) in a nested spec."""
    parts = dotted.split(".")
    node = spec
    for part in parts[:-1]:
        node = node[int(part)] if part.isdigit() else node[part]
    last = parts[-1]
    if last.isdigit():
        node[int(last)] = value
    else:
        node[last] = value


def run_script(script, spec_path=None, base_skill=str(BASE_SKILL),
               extra_args=None):
    """Run a validator script; returns CompletedProcess."""
    cmd = [sys.executable, str(ROOT / "scripts" / script)]
    if spec_path is not None:
        cmd += ["--spec", str(spec_path)]
    if base_skill is not None:
        cmd += ["--base-skill", base_skill]
    if extra_args:
        cmd += extra_args
    return subprocess.run(cmd, capture_output=True, text=True)


def run_check(script, spec_path, base_skill=str(BASE_SKILL)):
    return run_script(script, spec_path, base_skill)


@pytest.fixture
def mutated(tmp_path):
    """Return a helper: mutated(overrides) -> path of a spec file
    built from the 5-inch example with dotted-path overrides."""
    def _mutate(overrides, base=EXAMPLE_5IN):
        spec = load_example(base)
        for dotted, value in overrides.items():
            set_path(spec, dotted, value)
        return write_spec(tmp_path, spec)
    return _mutate
