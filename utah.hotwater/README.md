# utah.hotwater: Hot water and steam

Hot water plants, steam plants, boilers, and domestic hot water.

Major models include `UtahHWS`, `UtahBoiler`, and `UtahDHWS`. Point definitions are in `points*.xeto`;
equipment models declare their required and optional points.

Requires `utah` and the sys/ph 5.0.x dependencies declared in `lib.xeto`.
Install `utah` and this domain together. Extend models for the equipment actually
present at your site; check units, history policy, reference targets, and required
points before mapping data.

See the [root README](../README.md) for build/install instructions,
[contribution guide](../CONTRIBUTING.md) for conventions, and
[migration guide](../MIGRATION.md) for SkySpark 3 namespace changes.
