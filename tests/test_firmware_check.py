"""firmware_check: firmware vs MCU, gyro loop, DShot, versions."""
from conftest import EXAMPLE_5IN, EXAMPLE_HEX, run_check


def test_example_5inch_passes():
    r = run_check("firmware_check.py", EXAMPLE_5IN)
    assert r.returncode == 0, r.stdout


def test_example_hex_passes():
    r = run_check("firmware_check.py", EXAMPLE_HEX)
    assert r.returncode == 0, r.stdout


def test_px4_on_f405_fails(mutated):
    p = mutated({"flight_controller.firmware": "PX4",
                 "flight_controller.mcu": "STM32F405"})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "does not support MCU STM32F405" in r.stdout


def test_dshot1200_on_f405_fails(mutated):
    p = mutated({"flight_controller.mcu": "STM32F405",
                 "esc.protocol": "DShot1200"})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "maximum of DShot600" in r.stdout


def test_gyro_loop_over_max_fails(mutated):
    p = mutated({"flight_controller.gyro_loop_hz": 32000})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "exceeds the STM32F722 maximum" in r.stdout


def test_bad_version_string_fails(mutated):
    p = mutated({"flight_controller.firmware_version": "latest"})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "must look like '4.5.0'" in r.stdout


def test_mavlink_on_betaflight_fails(mutated):
    p = mutated({"telemetry.protocol": "MAVLink"})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "not supported by firmware Betaflight" in r.stdout


def test_nmea_on_px4_fails(mutated):
    p = mutated({"flight_controller.firmware": "PX4",
                 "flight_controller.mcu": "STM32H743",
                 "gps.protocol": "NMEA"})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "not supported by firmware PX4" in r.stdout


def test_unknown_firmware_fails(mutated):
    p = mutated({"flight_controller.firmware": "Cleanflight"})
    r = run_check("firmware_check.py", p)
    assert r.returncode == 1
    assert "is unknown" in r.stdout
