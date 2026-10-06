# utah.ahu: Airside equipment

Air handlers, exhaust/supply/relief fans, CRACs, and humidifiers.

Major models include `UtahAhu` and the fan equipment types. Point definitions are in `points*.xeto`;
equipment models declare their required and optional points.

Requires `utah` and the sys/ph 5.0.x dependencies declared in `lib.xeto`.
Install `utah` and this domain together. Extend models for the equipment actually
present at your site; check units, history policy, reference targets, and required
points before mapping data.

See the [root README](../README.md) for build/install instructions,
[contribution guide](../CONTRIBUTING.md) for conventions, and
[migration guide](../MIGRATION.md) for SkySpark 3 namespace changes.
