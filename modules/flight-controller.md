# Flight Controller (critical)

The flight controller is the brain: STM32 MCU + IMU + barometer, running Betaflight / INAV / PX4 / ArduPilot.

- **MCU:** STM32F405 (168 MHz), F722 (216 MHz), F745 (216 MHz), H743 (480 MHz). Gyro loop: 8 kHz max on F4/F7, 16 kHz on H7.
- **IMU:** MPU6000 / ICM42688 / BMI270 on SPI — never I2C for the gyro. Soft-mount the FC; hard-mounted gyros saturate from motor vibration.
- **Placement:** frame center, away from the power stage and the VTX, on rubber grommets or gel.
- **Checks:** `firmware_check.py` (firmware vs MCU, gyro loop), `compatibility_check.py` (known MCU/IMU/barometer).
