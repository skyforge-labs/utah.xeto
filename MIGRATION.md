# Moving to the SkySpark 4 libraries

Version 0.0.4 establishes the maintained SkySpark/Haxall 4.0.6 line using sys/ph
5.0.x. The previous public release (0.0.2) and the unpublished SkySpark 3 work
use a different namespace layout and dependency generation.

## Preserved legacy work

The `legacy/skyspark3` branch preserves the local SkySpark 3 source, compiled
artifacts, conventions documents, and previously unpushed changes as of
2026-10-06. It remains separate from the maintained `main` branch.
Existing 0.0.2 release assets remain available for older installations.

## Namespace changes

| Previous library | SkySpark 4 location |
| --- | --- |
| `utah` | `utah` |
| `utah.points` | `utah` |
| `utah.equips` | Shared definitions in `utah`; review obsolete system definitions individually |
| `utah.equips.ahu` | `utah.ahu` |
| `utah.equips.exhaustfan`, `.crac`, `.humidifier` | `utah.ahu` |
| `utah.equips.vav`, `.fcu`, `.heatpump` | `utah.terminal` |
| `utah.equips.boiler`, `.hws`, `.dhws` | `utah.hotwater` |
| `utah.equips.chiller`, `.chws`, `.coolingtower` | `utah.chilledwater` |
| `utah.equips.heatexchanger` | Shared heat exchanger definitions in `utah` |
| `utah.equips.meters`, `utah.meters` | `utah.meter`; shared electric points in `utah` |

This is a library-level guide, not a guarantee that every old type has an
identical replacement. Shared point types have moved into `utah`, and some
equipment-specific points have changed composition. Resolve each qualified
name against the installed catalog before updating records or downstream code.

For example, `utah.equips.ahu::UtahAhu` becomes `utah.ahu::UtahAhu`, and
`utah.equips.vav::UtahVav` becomes `utah.terminal::UtahVav`. The terminal base
definitions also now live in `utah.terminal`.

## Retained mapping definitions

The migration review retained 33 point definitions that were present in the
preserved SkySpark 3 source but absent from the initial SkySpark 4 checkout:
18 AHU points and 15 terminal points. They live in each domain's
`points.mapping.xeto` and are exposed through optional AHU/VAV slots.
These include command/status pairs, occupied/unoccupied airflow settings,
fan electrical power, humidity setpoints, inlet temperature, plant water
measurements, and effective occupancy. Existing required points are unchanged.

The port changes `<fixed>` to `<invariant>` and expresses hot/chilled water
context as markers where the 5.0 type system rejects the old multiple
inheritance. It does not attempt complete slot or semantic parity between
SkySpark 3 and 4. Type-name retention alone is not sufficient to migrate records.

The orphan `utah.equips.chiller/points.oil.xeto` file is not a library and is
excluded. Its three definitions already exist in
`utah.chilledwater/points.chiller.oil.xeto`.

## Upgrade checklist

1. Back up the project and existing Utah artifacts. Test on a project copy.
2. Install the six flat `.xetolib` artifacts using the root README instructions.
3. Update dependent library manifests to the new library names and sys/ph 5.0.x.
4. Update stored spec references, custom type bases, rule targets, queries, and
   other qualified-name strings. Check downstream Forge integrations separately;
   those extensions are not part of this public release.
5. Validate required points, units, history policies, reference targets, and
   command/status semantics against representative records.
6. Retire old library dependencies only after downstream references are migrated.

The build verifies compilation and loading all compiled libraries without source
in an isolated environment. It does not migrate customer data or validate an
entire production project. Keep SkySpark 3 artifacts on SkySpark 3.

## License and packaging

The root license is now AFL-3.0, matching the Utah source headers and library
metadata. Earlier root MIT declarations were inconsistent; this update does
not rewrite historical releases.

Compiled files are no longer checked into `main`. Each release is built from
its tagged commit, tested on Windows and Linux, and includes checksums.
The source layout is flat so this checkout can serve directly as `src/xeto/`
inside a SkySpark work directory; the portable build stages that layout itself.
