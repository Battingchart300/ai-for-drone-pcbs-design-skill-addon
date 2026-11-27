"""Regression fixtures: each file must FAIL its validator."""
from pathlib import Path

from conftest import ROOT, run_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"

# (fixture file, validator script that must FAIL on it)
CASES = [
    ("invented_mcu.json", "compatibility_check.py"),
    ("esc_voltage_low.json", "power_check.py"),
    ("px4_f405.json", "firmware_check.py"),
    ("vtx_vrx_mismatch.json", "compatibility_check.py"),
    ("thermal_overload.json", "thermal_check.py"),
    ("bool_current.json", "power_check.py"),
    ("kv_out_of_range.json", "compatibility_check.py"),
    ("unverified_imu.json", "compatibility_check.py"),
]


def test_fixtures_exist():
    for name, _ in CASES:
        assert (FIXTURES / name).is_file(), f"missing fixture {name}"


def test_fixtures_fail_their_validator():
    for name, script in CASES:
        r = run_check(script, str(FIXTURES / name))
        assert r.returncode == 1, (
            f"{name} should FAIL {script} but exited {r.returncode}:\n"
            f"{r.stdout}")
        assert "Traceback" not in r.stdout + r.stderr, (
            f"{name}: validator crashed instead of failing cleanly")
