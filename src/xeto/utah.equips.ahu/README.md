## Utah AHU Xeto Library

This directory contains the **Utah DFCM AHU tagging standard – Xeto implementation**.

### What’s in this library

- **`ahu.xeto`**
  - Defines `UtahAhu`, an abstract AHU type with references to related equipment and a comprehensive `points` block for AHU subsystems (occupancy, safeties, space, air paths, coils, pumps, valves, economizer, humidifier/dehumidifier, heat recovery, etc.).

- **`points.*.xeto`**
  - Defines the `Utah*` AHU point types used by `UtahAhu` (for example `UtahOccCmd`, `UtahChWFlow`, `UtahCoolingBypDmprPos`).
  - Each point sets a canonical `navName` and typical history settings (mode, interval), with units/precision where applicable.

### Conventions for this library

- Utah-specific types are prefixed with `Utah` and are intended to align with the Utah DFCM AHU standard.
- Prefer reusing existing `Utah*` AHU points before adding new ones; if you add new types, follow the existing naming and `navName` patterns.

### How to use

- **As a user**
  - Install & enable `utah`, `utah.points`, and `utah.equips.ahu` in your Haxall project.
  - Define concrete AHU types that **extend `UtahAhu`** and require only the points relevant to your design.
  - When mapping site data, map AHU points to the existing `Utah*` AHU point types where possible.

