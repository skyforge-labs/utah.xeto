# Release System

Auto-release for xeto libs via GitHub Actions.

## How It Works

```
bump build.props → build locally → commit lib/ → push main → auto-tag → GitHub Release
```

1. Push to `main` triggers the release workflow
2. Workflow reads `buildVersion` from `build.props`
3. If tag `v{buildVersion}` doesn't exist yet → creates tag + release
4. If tag already exists → does nothing (safe to push without releasing)

## Release Assets

Each release produces:

| Asset                     | Format        | Purpose                              |
| ------------------------- | ------------- | ------------------------------------ |
| `{libName}-{ver}.xetolib` | Zip (renamed) | Individual xeto lib                  |
| `{libName}-{ver}.sha256`  | Text          | SHA-256 checksum for xetolib         |
| `xeto-index.json`         | JSON          | Manifest of all xeto libs + versions |

### xeto-index.json Format

```json
{
  "generatedAt": "2026-02-11T12:00:00Z",
  "libs": [
    { "name": "utah", "stable": "0.1.0" },
    { "name": "utah.points", "stable": "0.1.0" }
  ]
}
```

ForgeHub's `XetoInstaller` reads this to discover available libs.

## How to Release

1. Bump `buildVersion` in `build.props` (e.g. `0.1.0` → `0.2.0`)
2. Build xeto libs: `xeto build` from `src/xeto/` dirs
3. Verify `lib/xeto/` has built libs
4. Commit and push to `main`
5. Release is created automatically

**No version bump = no release.** Safe to push code changes without releasing.

## Required Repo Structure

```
repo-root/
  build.props          # Must contain buildVersion=X.Y
  lib/
    xeto/              # Compiled xeto libs (committed)
      utah/
        lib.xeto
        ...
      utah.points/
        ...
  src/
    xeto/              # Xeto source
      utah/
      utah.points/
      utah.equips.ahu/
      ...
  .github/
    workflows/
      release.yml      # The release workflow
      tag.yml          # Auto-tagging workflow
```

### Key Files

- **`build.props`** — Single source of truth for version. All xeto libs inherit this version in the release.
- **`lib/`** — Committed build artifacts. Must be populated before pushing.

## Setting Up a New Repo

### 1. Create repo structure

```
mkdir -p lib/xeto src/xeto .github/workflows
```

### 2. Create `build.props`

```properties
buildVersion=0.1.0
org.name=Your Org
org.uri=https://example.com/
proj.name=YourProject
license.name=AFL-3.0
vcs.name=Git
```

### 3. Copy the release workflow

Copy `.github/workflows/release.yml` from this repo. No changes needed — it reads `buildVersion` from `build.props` and scans `lib/xeto/` automatically.

### 4. Add to ForgeHub (optional)

Users can register the repo in ForgeHub to install xeto libs:

```
// In SkySpark Axon shell
devRepoAdd("https://github.com/your-org/your-repo")
```

For private repos, set a token:

```
devRepoSetToken("your-repo", "ghp_xxxx")
```

## Versioning Rules

- **One version per release** — `buildVersion` applies to all xeto libs in the release. Individual `lib.xeto` versions are ignored by the release workflow.
- **Semver recommended** — Use `MAJOR.MINOR` or `MAJOR.MINOR.PATCH`.
- **Tags are immutable** — Once `v0.1.0` is released, pushing again with `buildVersion=0.1.0` is a no-op. Bump the version to release again.

## ForgeHub Install Flow

How `XetoInstaller` consumes releases:

```
1. fetchIndex(repo)           → GET /releases/latest → xeto-index.json
2. resolveStableVersion()     → index.libs[name].stable → "0.1.0"
3. fetchReleaseAssets(v0.1.0) → GET /releases/tags/v0.1.0 → asset list
4. downloadAsset(.xetolib)    → download utah-0.1.0.xetolib
5. downloadAsset(.sha256)     → download utah-0.1.0.sha256
6. verifySha256()             → compare checksums
7. install to lib/xeto/       → extract .xetolib to Env.cur.homeDir
```

## Troubleshooting

| Problem                    | Cause                     | Fix                                 |
| -------------------------- | ------------------------- | ----------------------------------- |
| Release not created        | `buildVersion` unchanged  | Bump version in `build.props`       |
| Empty release              | `lib/` not committed      | Build locally, commit `lib/`        |
| Tag already exists         | Same version pushed twice | Bump version or delete tag manually |
| Install fails: "not found" | Repo not registered       | `devRepoAdd(url)` in ForgeHub       |
| Install fails: 401         | Private repo, no token    | `devRepoSetToken(id, token)`        |
