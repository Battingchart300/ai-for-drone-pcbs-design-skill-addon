# EMI / EMC (critical)

Electromagnetic interference and compatibility — the difference between a clean gyro and a flyaway.

- Gyro SPI traces short, away from the power stage and the VTX.
- One solid GND plane under the FC; no routing over plane splits for high-speed signals.
- Switching regulator hot loops kept small; decouple per the regulator datasheet.
- VTX antenna away from GPS antenna (RF desense kills GPS lock).
- USB and high-speed lines: controlled impedance per the base skill.
- Ferrites / filtering on the VTX power feed where the video shows noise lines.
