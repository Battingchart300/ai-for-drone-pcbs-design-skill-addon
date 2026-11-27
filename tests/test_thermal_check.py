"""thermal_check: budget model, bool guards, cooling types."""
from conftest import EXAMPLE_5IN, EXAMPLE_HEX, run_check


def test_example_5inch_passes():
    r = run_check("thermal_check.py", EXAMPLE_5IN)
    assert r.returncode == 0, r.stdout


def test_example_hex_passes():
    r = run_check("thermal_check.py", EXAMPLE_HEX)
    assert r.returncode == 0, r.stdout


def test_overload_fails(mutated):
    # VTX: 25 + 20 W * 8 C/W * 0.5 = 105 C > 85 C max.
    p = mutated({"thermal.components.2.power_w": 20})
    r = run_check("thermal_check.py", p)
    assert r.returncode == 1
    assert "exceeds the max" in r.stdout


def test_bool_power_is_not_a_number(mutated):
    p = mutated({"thermal.components.0.power_w": True})
    r = run_check("thermal_check.py", p)
    assert r.returncode == 1
    assert "must be a non-negative number" in r.stdout


def test_unknown_cooling_fails(mutated):
    p = mutated({"thermal.components.0.cooling": "water"})
    r = run_check("thermal_check.py", p)
    assert r.returncode == 1
    assert "cooling must be one of" in r.stdout


def test_empty_components_fails(mutated):
    p = mutated({"thermal.components": []})
    r = run_check("thermal_check.py", p)
    assert r.returncode == 1
    assert "non-empty list" in r.stdout


def test_missing_thermal_section_fails(mutated, tmp_path):
    from conftest import load_example, write_spec
    spec = load_example()
    del spec["thermal"]
    p = write_spec(tmp_path, spec)
    r = run_check("thermal_check.py", p)
    assert r.returncode == 1
    assert "thermal section missing" in r.stdout
