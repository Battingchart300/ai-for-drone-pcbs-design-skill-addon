# IMU (high)

Gyroscope + accelerometer: the sensor the flight controller flies on.

- **Parts:** MPU6000, ICM42688, BMI270 — on SPI, short traces, away from the power stage.
- **Vibration:** the FC must be soft-mounted. Motor vibration saturates a hard-mounted gyro and no filter fixes it afterwards.
- **Filtering:** gyro loop rate and filtering are firmware settings (Betaflight/INAV), not board layout — but the layout decides how much noise reaches the sensor in the first place.
- **Checks:** `compatibility_check.py` (known IMU), `firmware_check.py` (gyro loop vs MCU).
