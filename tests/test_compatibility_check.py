"""compatibility_check: known parts, protocols, KV, EU rules."""
from conftest import EXAMPLE_5IN, EXAMPLE_HEX, run_check


def test_example_5inch_passes():
    r = run_check("compatibility_check.py", EXAMPLE_5IN)
    assert r.returncode == 0, r.stdout


def test_example_hex_passes():
    r = run_check("compatibility_check.py", EXAMPLE_HEX)
    assert r.returncode == 0, r.stdout


def test_invented_mcu_fails(mutated):
    p = mutated({"flight_controller.mcu": "STM32X999"})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "not a known verified part" in r.stdout


def test_unverified_imu_fails(mutated):
    p = mutated({"flight_controller.imu": "UNVERIFIED"})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "UNVERIFIED" in r.stdout


def test_vtx_vrx_mismatch_fails(mutated):
    p = mutated({"vrx.protocol": "DJI O3"})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "does not match VTX protocol" in r.stdout


def test_kv_out_of_range_fails(mutated):
    p = mutated({"motors.0.kv": 4000})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "outside the typical range" in r.stdout


def test_connector_over_rating_fails(mutated):
    p = mutated({"connectors.0.max_current_a": 100})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "exceeds the XT60 rating" in r.stdout


def test_eu_altitude_over_limit_fails(mutated):
    p = mutated({"compliance.max_altitude_m": 150})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "exceeds the EU open-category limit" in r.stdout


def test_remote_id_missing_for_c3_fails(mutated):
    p = mutated({"compliance.class_mark": "C3",
                 "compliance.remote_id": False},
                base=EXAMPLE_HEX)
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "requires Direct Remote ID" in r.stdout


def test_unknown_telemetry_fails(mutated):
    p = mutated({"telemetry.protocol": "WiFi"})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "not a known verified part" in r.stdout


def test_dshot1200_on_blheli_s_fails(mutated):
    p = mutated({"esc.protocol": "DShot1200",
                 "esc.firmware": "BLHeli_S"})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "not supported by ESC firmware" in r.stdout


def test_unknown_gps_module_fails(mutated):
    p = mutated({"gps.module": "GPS-9000"})
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "not a known verified part" in r.stdout


def test_mtom_over_class_limit_fails(mutated):
    p = mutated({"compliance.class_mark": "C1"},
                base=EXAMPLE_HEX)
    r = run_check("compatibility_check.py", p)
    assert r.returncode == 1
    assert "exceeds the C1 class limit" in r.stdout
