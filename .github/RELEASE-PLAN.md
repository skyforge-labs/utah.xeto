# Release process

`build.props` is the version source of truth. All six libraries use
`utah.version`; checked-in binaries and `versions.json` are no longer used.

1. Update the version, migration notes, and `RELEASE-NOTES.md` in a pull request.
2. Require successful Windows and Linux CI, plus review of semantic changes.
3. Merge the pull request. Tag the merged commit `v<utah.version>` and push it.
4. The tag workflow verifies the version and rebuilds. Only after both platforms
   pass does it create a GitHub release from the Linux build artifacts.

The release includes six `.xetolib` files, a ZIP with a `lib/xeto/` layout,
license, installation/migration docs, a commit manifest, and SHA-256 checksums.
Missing outputs, compiler errors, or failed compiled-only loading stop packaging.
Existing releases are not silently overwritten.

For local packaging, run `python scripts/build.py --package` from a clean commit.
The script refuses an existing `dist/v<version>` directory to prevent mixing
artifacts. Move an earlier output directory aside before repeating a package build.

Never publish the surrounding SkySpark installation, Forge extensions, customer
data, credentials, or vendor runtime archives. These are not release inputs.
