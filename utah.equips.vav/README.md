## Utah VAV Xeto library

This directory contains the **Utah DFCM VAV tagging standard – Xeto implementation**.

### What’s in this library

- **`vav*.xeto`**
  - Defines Utah VAV equipment types (for example base `VAV` plus variants like cooling-only, reheat, fan-powered, dual-duct, venturi).
  - Each type composes Utah traits/points into concrete VAV models.

- **`points.*.xeto`**
  - Defines the `Utah*` VAV point types used by the VAV equipment models (flows, temperatures, dampers, valves, fans, occupancy, overrides, misc).
  - Each point sets a canonical `navName` and typical history settings, with units/precision where applicable.

- **`lib.xeto`**
  - Declares the `utah.equips.vav` library and its dependencies.

### Conventions for this library

- Utah-specific VAV equipment and point types are prefixed with `Utah` and follow the Utah DFCM VAV conventions.
- Prefer reusing existing `Utah*` VAV point types and VAV equipment variants before adding new ones; if you add new types, follow existing naming and `navName` patterns.

### How to use

- **As a user**
  - Install & enable `utah`, `utah.points`, and `utah.equips.vav` in your Haxall project.
  - Choose the appropriate VAV equipment type (or extend it) and map your VAV points to the existing `Utah*` VAV point types where possible.


