"""run_all + examples: end-to-end behaviour of the addon."""
import json
import subprocess
import sys
from pathlib import Path

from conftest import (BASE_SKILL, EXAMPLE_5IN, EXAMPLE_HEX, ROOT,
                      run_script)


def run_all(spec, base_skill=str(BASE_SKILL)):
    return run_script("run_all.py", spec, base_skill)


def test_run_all_5inch_passes():
    r = run_all(EXAMPLE_5IN)
    assert r.returncode == 0, r.stdout
    assert "run_all=PASS" in r.stdout
    assert "Made by PTS6845" in r.stdout


def test_run_all_hex_passes():
    r = run_all(EXAMPLE_HEX)
    assert r.returncode == 0, r.stdout
    assert "run_all=PASS" in r.stdout


def test_run_all_invented_part_fails(mutated):
    p = mutated({"flight_controller.mcu": "STM32X999"})
    r = run_all(p)
    assert r.returncode == 1
    assert "run_all=FAIL" in r.stdout


def test_run_all_missing_base_exits_2():
    r = run_all(EXAMPLE_5IN, base_skill="/nonexistent/base-skill")
    assert r.returncode == 2
    assert "base skill missing" in r.stdout


def test_run_all_missing_spec_exits_2(tmp_path):
    r = run_all(str(tmp_path / "nope.json"))
    assert r.returncode == 2


def test_examples_have_required_sections():
    for path in (EXAMPLE_5IN, EXAMPLE_HEX):
        spec = json.loads(Path(path).read_text(encoding="utf-8"))
        for section in ("drone", "battery", "flight_controller", "esc",
                        "motors", "power_domains", "thermal"):
            assert section in spec, f"{path}: missing {section}"


def test_manifest_and_compatibility_versions():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    compat = json.loads((ROOT / "compatibility.json").read_text())
    assert manifest["version"] == "0.0.1"
    assert manifest["requires"]["ai-pcb-design-skill"] == ">=1.2.1"
    assert compat["hard_dependency"] is True
    assert compat["missing_base_exit_code"] == 2
    assert compat["base_skill"]["min_version"] == "1.2.1"


def test_schema_is_valid_json():
    schema = json.loads(
        (ROOT / "schemas" / "drone-spec.schema.json").read_text())
    assert schema["type"] == "object"
    assert "drone" in schema["properties"]


def test_credit_in_skill_and_readme():
    credit = "Made by PTS6845 — https://battingchart300.github.io"
    assert credit in (ROOT / "SKILL.md").read_text()
    assert credit in (ROOT / "README.md").read_text()
    assert credit in (ROOT / "scripts" / "run_all.py").read_text()


def test_sim_status_runs():
    r = subprocess.run([sys.executable,
                        str(ROOT / "simulations" / "sim_status.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "BLOCKED" in r.stdout or "OK" in r.stdout
    # No fake PASS: the tool status must never claim a simulation ran.
    assert "simulation ran" not in r.stdout.lower().replace(
        "no simulation run", "")
