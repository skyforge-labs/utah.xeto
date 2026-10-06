## Utah core Xeto library

Shared markers, quantity abstracts, history policies, and **cross-domain concretes**.

Domain libs depend only on `utah` (+ PH) — never on each other.

| Layer | Examples |
|-------|----------|
| Markers / components | `UtahPrimary`, `UtahDischarge`, `UtahHxChW` |
| Quantity abstracts | `UtahWaterTemp`, `UtahAirFlow` |
| History mixins | `UtahHisCov`, `UtahHisSampledMajorEquip` |
| Cross-domain points | `points.cross.xeto`, `points.plantloop.xeto`, HX |
| Terminal bases | in `utah.terminal` (`UtahTerminalUnit`, …) |

### Domain libs

- `utah.ahu` — AHU + airside hangers-on
- `utah.terminal` — VAV / FCU / HP (extends terminal bases)
- `utah.hotwater` — HWS / boiler / DHWS
- `utah.chilledwater` — CHWS / chiller / CT
- `utah.meter` — meters

### Principles

1. Types used by ≥2 domains live in `utah`
2. Optional on abstracts; required only on named variants
3. Plant ChW/HW points inherit shared loop/pump abstracts
