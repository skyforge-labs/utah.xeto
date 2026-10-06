# Utah Xeto libraries

Reusable equipment and point models implementing Utah DFCM Haystack tagging
conventions. **SkySpark 4 is the maintained development line.** This project is
under active development; review migration notes before upgrading.

[Releases](https://github.com/skyforge-labs/utah.xeto/releases) ·
[Contributing](CONTRIBUTING.md) · [Migration](MIGRATION.md) · [License](LICENSE)

## Compatibility

- Baseline: SkySpark **4.0.6** or Haxall **4.0.6**, with sys/ph **5.0.x**.
- Java **21+** and Python **3.10+** for the portable build script.
- Later runtime versions need their own validation; SkySpark 3 is incompatible
  with these artifacts. Its preserved source is on
  [`legacy/skyspark3`](https://github.com/skyforge-labs/utah.xeto/tree/legacy/skyspark3).
- The libraries are open source under **AFL-3.0**. SkySpark itself is a separate product.

## Libraries

| Library | Contents |
| --- | --- |
| `utah` | Shared markers, equipment bases, points, and history policies |
| `utah.ahu` | Air handlers, exhaust/supply/relief fans, CRACs, humidifiers |
| `utah.terminal` | VAVs, fan coils, mini-splits, unit heaters, heat pumps |
| `utah.hotwater` | Hot water and steam plants, boilers, domestic hot water |
| `utah.chilledwater` | Chilled water plants, chillers, cooling towers |
| `utah.meter` | Electricity, gas, and water meters |

Every domain library depends on `utah` and the standard libraries, not another
Utah domain. Shared definitions belong in `utah`.

## Install a release

1. Download `utah-xeto-<version>-skyspark4.zip` from a SkySpark 4 release.
   `SHA256SUMS` lists checksums for the ZIP and individual artifacts.
2. Back up the existing Utah libraries and project data before upgrading.
   Stop the target runtime before replacing libraries.
3. Extract the ZIP to a temporary directory. Copy its six files from `lib/xeto/`
   into the target SkySpark/Haxall **work directory's** `lib/xeto/` directory.
   Keep the flat names such as `utah.ahu.xetolib`; do not rename them to the old
   SkySpark 3 versioned-directory layout. Preserve unrelated libraries.
4. Start the runtime and load the required libraries in the target project's
   library management view. Include `utah` plus the domains you need.
5. Verify the selected library version and a representative equipment/point
   mapping in a test project before deploying to production.

Use a work directory without another Utah source checkout for binary deployment.
Source development and compiled-only installation are separate workflows.
The release contains models, not customer records or automatic record migrations.
See [MIGRATION.md](MIGRATION.md) for renamed library namespaces.

## Build from source

```sh
git clone https://github.com/skyforge-labs/utah.xeto.git
cd utah.xeto
python scripts/build.py
python scripts/build.py --package
```

The first build downloads the [public Haxall 4.0.6 runtime](https://github.com/haxall/haxall/releases/tag/v4.0.6)
and verifies its pinned SHA-256. The build copies only the six public libraries
into a temporary work directory, compiles them, then loads every compiled library
in a second environment with **no Utah source**. Packaging writes `dist/v<version>/`.
The script never installs into a running project or modifies an existing runtime.

To use an existing runtime instead of downloading Haxall:

```sh
python scripts/build.py --runtime /path/to/skyspark-4.0.6
```

On Windows, use a quoted Windows path. `--runtime` takes the distribution directory
containing `lib/java/sys.jar`, not your project/work directory.

The repository intentionally has library folders at its root so it can also be
checked out directly as a SkySpark work directory's `src/xeto/`. In that layout,
the configured SkySpark 4 CLI can build the libraries directly:

```sh
xeto4 build utah utah.ahu utah.terminal utah.hotwater utah.chilledwater utah.meter
```

`xeto4` is a local wrapper name; the portable Python script works without it.

## Use and contribute

Reference qualified names such as `utah.ahu::UtahAhu` or
`utah.terminal::UtahVav`. Extend a model for a specific equipment configuration
and validate its required points and references against your site data.
Compilation and binary loading do not certify conformance of a real building.

Open an [issue](https://github.com/skyforge-labs/utah.xeto/issues) for missing
equipment, mapping problems, or documentation corrections. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow.
