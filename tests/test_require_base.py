"""require_base: the hard dependency must hold, or exit 2."""
from pathlib import Path

from conftest import BASE_SKILL, ROOT, run_script


def test_base_found_sibling(tmp_path):
    r = run_script("require_base.py", base_skill=str(BASE_SKILL))
    assert r.returncode == 0
    assert "Base skill OK" in r.stdout


def test_base_missing_dir_exits_2(tmp_path):
    r = run_script("require_base.py", base_skill=str(tmp_path / "nope"))
    assert r.returncode == 2
    assert "BASE SKILL MISSING" in r.stdout


def test_base_misnamed_exits_2(tmp_path):
    d = tmp_path / "fake-base"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\nname: ai-pcb-design-skill-addon\n---\n\n**Version:** 1.2.6\n")
    r = run_script("require_base.py", base_skill=str(d))
    assert r.returncode == 2


def test_base_too_old_exits_2(tmp_path):
    d = tmp_path / "old-base"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\nname: ai-pcb-design-skill\n---\n\n**Version:** 1.0.0\n")
    r = run_script("require_base.py", base_skill=str(d))
    assert r.returncode == 2
    assert "TOO OLD" in r.stdout


def test_base_exact_minimum_passes(tmp_path):
    d = tmp_path / "min-base"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\nname: ai-pcb-design-skill\n---\n\n**Version:** 1.2.1\n")
    r = run_script("require_base.py", base_skill=str(d))
    assert r.returncode == 0
