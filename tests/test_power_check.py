"""power_check: battery, ESC, motors, PDB, domains, BMS."""
from conftest import EXAMPLE_5IN, EXAMPLE_HEX, run_check


def test_example_5inch_passes():
    r = run_check("power_check.py", EXAMPLE_5IN)
    assert r.returncode == 0, r.stdout


def test_example_hex_passes():
    r = run_check("power_check.py", EXAMPLE_HEX)
    assert r.returncode == 0, r.stdout


def test_esc_voltage_too_low(mutated):
    p = mutated({"esc.voltage_max_v": 16.8})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "below the battery max voltage" in r.stdout


def test_motor_total_over_battery(mutated):
    p = mutated({"motors.0.max_current_a": 100})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "exceeds the battery max current" in r.stdout


def test_motor_over_esc_channel(mutated):
    p = mutated({"motors.0.max_current_a": 50})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "exceeds the ESC continuous current" in r.stdout


def test_pdb_too_small(mutated):
    p = mutated({"pdb.max_current_a": 100})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "exceeds the PDB max current" in r.stdout


def test_vbat_domain_mismatch(mutated):
    p = mutated({"power_domains.0.voltage_v": 11.1})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "does not match the battery nominal voltage" in r.stdout


def test_domain_over_budget(mutated):
    p = mutated({"power_domains.1.consumers.0.current_a": 5.0})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "over the 3 A budget" in r.stdout


def test_bool_current_is_not_a_number(mutated):
    # Python treats True as 1 — the validator must reject it.
    p = mutated({"power_domains.0.consumers.0.current_a": True})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "must be a non-negative number" in r.stdout


def test_nan_current_rejected(mutated, tmp_path):
    import json
    from conftest import load_example, write_spec
    spec = load_example()
    spec["motors"][0]["max_current_a"] = float("nan")
    # json dumps NaN as NaN (invalid strict JSON) — write raw instead
    raw = json.dumps(spec).replace('"max_current_a": NaN',
                                  '"max_current_a": 1e999')
    path = tmp_path / "spec.json"
    path.write_text(raw)
    r = run_check("power_check.py", str(path))
    assert r.returncode == 1


def test_bms_cells_mismatch(mutated):
    p = mutated({"bms.present": True, "bms.cells": 4,
                 "bms.cutoff_v_per_cell": 3.2,
                 "bms.balance_current_ma": 500})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "does not match battery.cells" in r.stdout


def test_bms_cutoff_out_of_range(mutated):
    p = mutated({"bms.present": True, "bms.cells": 6,
                 "bms.cutoff_v_per_cell": 2.0,
                 "bms.balance_current_ma": 500})
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "cutoff_v_per_cell" in r.stdout


def test_missing_battery_fails(mutated, tmp_path):
    from conftest import load_example, write_spec
    spec = load_example()
    del spec["battery"]
    p = write_spec(tmp_path, spec)
    r = run_check("power_check.py", p)
    assert r.returncode == 1
    assert "battery section missing" in r.stdout


def test_array_root_is_setup_error(tmp_path):
    p = tmp_path / "spec.json"
    p.write_text("[1, 2, 3]")
    r = run_check("power_check.py", str(p))
    assert r.returncode == 2
    assert "must be a JSON object" in r.stdout
