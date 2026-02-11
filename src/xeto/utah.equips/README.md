## Utah equipment Xeto library

This directory contains the **Utah DFCM equipment Xeto library** for high-level Utah equipment concepts.
It fills gaps in the generic `ph.equips` library and provides Utah-specific equipment traits and types that other Utah equip libraries can reuse.

> **Status**: This Utah equipment library is **under active development**; conventions are still being set and **are subject to change**.

### What’s in this library

- Utah-specific equipment traits and base types that are **not tied to a single equipment family** (for example patterns that multiple Utah equipment types share).
- High-level equipment definitions used as parents or mixins by `utah.equips.ahu`, `utah.equips.vav`, and future Utah equipment libraries.

### Conventions for this library

- Use this library to **fill gaps where `ph.equips` does not define a Utah-relevant pattern**.
- Keep definitions high-level; AHU-, VAV-, or other family-specific details belong in their own `utah.equips.*` library.

### How to use

- **As a user**
  - Install & enable `utah` and `utah.equips` in your Haxall project.
  - Use these equipment traits/types directly, or rely on them indirectly through `utah.equips.ahu`, `utah.equips.vav`, and similar libraries.


