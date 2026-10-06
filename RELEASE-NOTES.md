# Utah Xeto 0.0.4 — SkySpark 4

First public release of the consolidated SkySpark 4 libraries. Requires the
4.0.6 baseline and sys/ph 5.0.x; these artifacts are not compatible with SkySpark 3.

- Six libraries: `utah`, `utah.ahu`, `utah.terminal`, `utah.hotwater`,
  `utah.chilledwater`, and `utah.meter`.
- Retains additional AHU/VAV point definitions from the unpublished SkySpark 3 work.
- Public build toolchain, Windows/Linux CI, isolated compiled-library loading,
  version checks, commit manifest, and SHA-256 checksums.
- Updated installation/contribution documentation and consistent AFL-3.0 licensing.
- SkySpark 3 work is preserved on `legacy/skyspark3`.

Download the ZIP for the complete `lib/xeto/` bundle. Read `MIGRATION.md` before
upgrading: qualified names changed, and existing records are not migrated
automatically. The models remain under active development. Validate equipment
semantics and required points in your own test project before production use.
