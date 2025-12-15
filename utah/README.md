## Utah core Xeto library

This directory contains the **core Utah DFCM Xeto library** for generic, high-level Utah concepts.
It defines shared Utah traits and metadata that other Utah libraries (`utah.points`, `utah.equips.*`) build on.

> **Status**: This core Utah library is **under active development**; conventions are still being set and **are subject to change**.

### What’s in this library

- Core Utah metadata and markers that capture Utah DFCM semantics (for example ownership, programs, generic categories, and other cross-cutting metadata).
- Base building blocks that are **not tied to a specific piece of equipment or point**.

### Conventions for this library

- Keep types **generic and reusable** across equipment and points.
- Avoid putting AHU/VAV/plant-specific logic here; that belongs in `utah.points` or the `utah.equips.*` libraries.

### How to use

- **As a user**
  - Install & enable `utah` in your Haxall project.
  - Compose `utah` traits into your own types, or rely on them indirectly via `utah.points` and `utah.equips.*`.


