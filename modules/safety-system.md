# Safety System (critical)

Failsafe, arming, lab testing — the module that keeps a fault from becoming a crash.

- **Failsafe:** loss of RC link → disarm or return-to-home (where the firmware supports it). Never fly away. Tested on the bench before the first flight.
- **Arming:** deliberate switch only, with a pre-arm check (sensors OK, battery OK, GPS lock where required). Never arm on the bench with props on.
- **Lab sequence:** bench power-up → motor test WITHOUT props → range test → failsafe test. Props go on only at the field.
- **Single points of failure:** one battery, one PDB, one FC. A hexacopter can lose one motor and land; a quadcopter cannot — the review report says so.
- **Logs:** blackbox (Betaflight/INAV) or dataflash (ArduPilot/PX4) logging is required — a design without logging cannot be diagnosed after a crash.
