## Utah points Xeto library

This directory contains the **Utah DFCM points Xeto library**.
It defines Utah-standard point types and traits and is designed to **fill gaps in `ph.points`** or refine them for Utah-specific usage.

> **Status**: This Utah points library is **under active development**; conventions are still being set and **are subject to change**.

### What’s in this library

- Utah point traits and base types shared across equipment families (for example generic air, water, fan, pump, valve, coil, and history traits).
- Concrete `Utah*` point types that represent common Utah DFCM field points, independent of any single equipment type.

### Conventions for this library

- Use this library when **`ph.points` does not define a Utah DFCM point or behavior you need**, or when Utah needs a stricter/more specific convention.
- Keep point definitions **equipment-agnostic**; AHU/VAV-specific points live in `utah.equips.ahu` and `utah.equips.vav`.

### How to use

- **As a user**
  - Install & enable `utah` and `utah.points` in your Haxall project.
  - Map site points to the `Utah*` point types defined here, or use them as building blocks in equipment-specific libraries and models.


