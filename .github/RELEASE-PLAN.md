# Release workflow: per-version tags

## Source of truth

- `versions.json` only.
- `buildVersion` is used only as a fallback when an item has no `version`.

## Release decision

- Every distinct version referenced by `pods[]` or `libs[]` gets a tag:
  - Tag format: `v{version}`.
- If a release for that tag already exists → skip.
- If a release is missing → create tag + release.

## Assets per release

Each release contains only assets that match its version:

- `versions.json`
- One `.pod` per matching `pods[]` entry (if file exists).
- One `.xetolib` per matching `libs[]` entry:
  - Prefer exact `{name}-{version}.xetolib` if present.
  - Otherwise zip the lib folder.
- `all.zip` (bundle of the above).

Missing artifacts are skipped (do not fail the release).

## Monorepo

- Set `PROJECT_ROOT` in `.github/workflows/release.yml` to the project subdir.
