# ESC (critical)

Electronic speed controllers: 4-in-1 or singles, driving the motors from the FC's DShot signal.

- **Protocols:** PWM, OneShot125, Multishot, DShot150/300/600/1200. DShot1200 needs BLHeli_32 or AM32 and an F7/H7 FC; BLHeli_S tops out at DShot600.
- **Current:** continuous current is per channel — each motor's max current must fit one channel. Burst ratings are seconds, not minutes.
- **Voltage:** the ESC max voltage must cover the fully charged battery (6S = 25.2 V). A 4S-rated ESC on 6S dies on plug-in.
- **Heat:** FET losses are I²R — size the copper, add thermal vias, keep airflow over the ESC.
- **Checks:** `power_check.py` (voltage, currents), `compatibility_check.py` (protocol vs firmware), `firmware_check.py` (DShot ceiling).
