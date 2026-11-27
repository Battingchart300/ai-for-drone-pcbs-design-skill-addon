# Components

Verified parts used by this addon (full tables in `scripts/config.json` — a part that is not there FAILS validation until it is added with its datasheet source):

- **FC MCUs:** STM32F405 (Cortex-M4, 168 MHz), STM32F722 (Cortex-M7, 216 MHz), STM32F745 (Cortex-M7, 216 MHz), STM32H743 (Cortex-M7, 480 MHz).
- **IMUs:** MPU6000, ICM42688, BMI270.
- **Barometers:** BMP388, BMP280, DPS310. **Magnetometers:** QMC5883L, HMC5883L, IST8310.
- **GPS:** u-blox M10, M9N, M8N.
- **ESC firmware:** BLHeli_S, BLHeli_32, AM32. Protocols: PWM, OneShot125, Multishot, DShot150/300/600/1200.
- **Cameras:** analog — RunCam Phoenix 2, Caddx Ratel 2; digital — DJI O3 Air Unit, Walksnail Avatar HD Pro, HDZero Lux.
- **Video protocols:** analog, DJI O3, HDZero, Walksnail Avatar.
- **Telemetry:** CRSF, ELRS, MAVLink, SBUS, FPort.
- **Connectors:** XT30, XT60, XT90, XT150, JST-GH, JST-SH, SMA, RP-SMA, MMCX, U.FL, USB-C.

Never invent a part number, pinout or datasheet value. When the model does not know a value, it ASKS instead of inventing. `UNVERIFIED` is an error in the validators, not a pass.
