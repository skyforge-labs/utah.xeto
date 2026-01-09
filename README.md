
## Utah Xeto Libraries

This directory contains the **State of Utah DFCM Haystack tagging standard – Xeto implementation**.
It provides reusable libraries for **Utah-specific metadata, points, and equipment types**.

> **Status**: These Utah libraries are **under active development**; conventions are still being set and **are subject to change**.

### Utah library overview

- **`utah`** – Core traits and conventions capturing DFCM semantics.
- **`utah.points`** – Shared point definitions (generic across equipment).
- **`utah.equips`** – Base equipment traits and shared abstractions.
- **`utah.equips.ahu`** – AHU equipment and points.
- **`utah.equips.vav`** – VAV equipment and points.
- **`utah.equips.boiler`** – Boiler equipment and points.
- **`utah.equips.chiller`** – Chiller equipment and points.
- **`utah.equips.chws`** – Chilled water system equipment and points.
- **`utah.equips.hws`** – Hot water system equipment and points.
- **`utah.equips.coolingtower`** – Cooling tower equipment and points.

### General conventions

- **Composition first**
  - Types are built by composing lower-level spcs from `ph.*`, `utah`, and `utah.points` rather than redefining semantics.

- **Consistent naming**
  - Utah-specific types are prefixed with `Utah` (for example `UtahAhu`, `UtahChWFlow`).
  - `navName`, units, precision, and history settings are chosen to be stable and analytics-friendly.

### How to use these libraries

- **As a user**
  - Install & enable the relevant libraries (for example `utah`, `utah.points`, `utah.equips.ahu`) in your [Haxall](https://github.com/haxall/haxall) project.
  - Declare equipment and points using the provided Utah types, extending abstract base types (such as `UtahAhu`) for project-specific variants.

- **As a contributor**
  - Prefer extending or composing existing Utah traits/types instead of duplicating semantics.
  - Follow existing naming and history conventions within the Utah libraries.
  - Each Utah top-level library directory **should include a small `README.md`** that explains:
    - What the library is for.
    - What major types it defines (high level only).
    - Any important conventions specific to that library.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Development setup and guidelines
- Code style and naming conventions
- Pull request process
- Types of contributions we accept

### Quick Start for Contributors

1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Check existing [issues](https://github.com/skyforge-labs/utah.xeto/issues) for opportunities
3. Follow the [pull request template](.github/PULL_REQUEST_TEMPLATE.md) when submitting changes

### Development Resources

- **[Xeto Language](https://github.com/Project-Haystack/xeto)** - Official Xeto specification and standard libraries
- **[Haxall Framework](https://github.com/haxall/haxall)** - IoT framework that runs Xeto libraries
- **Xeto Tools** - Use `xeto build` to compile libraries and validate syntax
- **Project Haystack** - Industry standard for building data semantics

