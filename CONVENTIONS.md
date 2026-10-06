# Utah Xeto Conventions

Normative conventions for `utah` and `utah.equips.*`. Subject to change while libs stabilize.

## Goals

- Consistent roles (cmd vs status vs enable, etc.)
- Unique non-abstract point types; compose/inherit instead of copy
- Aligned type / slot / navName naming
- Clear, distinguishing `doc` on every spec
- Stable history, units, and file layout

## Spec layers

Compose in this order:

```
context/component  →  phenomena  →  kind/role  →  history
```

Example: `UtahDischarge & UtahFanCmd & UtahHisCov`

| Layer | Lives in | Purpose |
|-------|----------|---------|
| Abstracts | `utah` | Reusable roles, phenomena, components |
| Shared concretes | `utah` | Cross-equip points (e.g. OA, zone-generic) |
| Equip concretes | `utah.equips.*` | Context + his + navName + doc |
| Equip defs | `utah.equips.*` | Equip type + `points:` slots |

Rules:

- Prefer extend/compose existing Utah abstracts over new from-scratch roles.
- Equip libs must not redefine a role that already exists in `utah`.
- Every **non-abstract** type name must be unique across all Utah libs.

## Point roles (closed vocabulary)

| Suffix | Meaning |
|--------|---------|
| `Enab` | Permission / interlock to allow run |
| `Cmd` | Desired output / commanded state |
| `Sts` | Feedback of the matching Cmd, Pos, or Spd |
| `Pos` | 0–100% position command |
| `Spd` | 0–100% speed command |
| `Sp` | Setpoint |
| `Alrm` | Alarm |
| `Ovrd` | Override |

Notes:

- **Enab ≠ Cmd ≠ Sts.** Enable = allowed; Cmd = told to run; Sts = proven/actual.
- Bool open/close and % position are parallel families: `Cmd`/`CmdSts` and `Pos`/`PosSts`.
- Prefer defining both cmd and feedback **types** even if the equip slot is optional (`?`).
- Measured process values: prefer short concrete names (`DaTemp`) over `…Sensor` unless disambiguation needs it.
- Prefer `Enab` / `Sts` — not `Enable` / `Status`.

## Naming triad

Keep these aligned:

| Layer | Form | Example |
|-------|------|---------|
| Type | `Utah` + PascalCase | `UtahDaFanCmd` |
| Slot | camelCase | `daFanCmd` |
| navName | PascalCase string | `"DaFanCmd"` |

- Slot ≈ type without `Utah` prefix (camelCase).
- navName ≈ slot with first letter capitalized.
- Do not invent parallel spellings for the same concept.

## Abbreviations (freeze)

| Abbr | Meaning |
|------|---------|
| `Da` / `Ra` / `Oa` / `Ma` | Discharge / return / outside / mixed air |
| `Rlf` | Relief |
| `ChW` / `HW` / `CW` | Chilled / hot / condenser water |
| `Vlv` / `Dmpr` | Valve / damper |
| `Pri` / `Sec` | Primary / secondary |
| `Clg` / `Htg` | Cooling / heating |
| `Eff` | Effective |
| `Sp` / `Sts` / `Enab` / `Cmd` | Setpoint / status / enable / command |
| `Alrm` | Alarm |
| `Spd` / `Pos` | Speed / position |
| `Hx` | Heat exchanger |
| `Blr` / `Chlr` | Boiler / chiller |

When adding an abbrev, document it here first.

## Documentation

Xeto: leading `//` on a type or slot becomes its `doc`.

Rules:

- Every spec (abstract and concrete) must have a `doc` of at least one line.
- Doc must distinguish the spec from near siblings (e.g. Cmd vs Enab vs Sts).
- Keep docs short and plain; expand only when needed.
- **Do not** put section banners as the leading `//` immediately above a type/slot — that pollutes `doc`.
- Prefer a blank line (or no comment) between organizational whitespace and the next definition; real docs only as intentional leading `//` (or equivalent formal doc).

Doc template:

> `{What it is}. {How it differs from the closest sibling}.`

Example: `Discharge fan run command (desired on/off). Not enable and not proven status.`

## History

Do not inline one-off `hisMode` / intervals on concretes. Mixin:

| Mixin | Use |
|-------|-----|
| `UtahHisCov` | Bools, cmds, enables, discrete modes |
| `UtahHisSampledDefault` | Zone/space sensors (~10 min) |
| `UtahHisSampledMajorEquip` | AHU/plant analogs (~5 min) |
| `UtahHisConsumptionDefault` | Energy/totalized default |
| `UtahHisConsumptionMajorEquip` | Energy/totalized major equip |

## Equip `points:` slots

- Group by domain in source order (occupancy → space → airpaths → coils → fans → plant → overrides). Source order is for humans only until a formal group exists.
- Required vs optional: type existence ≠ required on every equip; use `?` for site-dependent points.
- Prefer shared equip bases (`UtahTerminalUnit`, pump bases, etc.) so slot keys stay aligned across related equips.

## File layout

| Location | Contents |
|----------|----------|
| `utah/points.*.xeto` | Abstracts + shared concretes |
| `utah/equip.*.xeto` | Shared equip bases |
| `utah/points.equipComponents.xeto` | Component markers (fan, valve, zone, …) |
| `utah/points.history.xeto` | History mixins |
| `utah.equips.*/points.*.xeto` | Equip-scoped concrete points |
| `utah.equips.*/*.xeto` | Equip defs |

One file ≈ one domain. Keep files under a maintainable size; split when a domain grows large.

## Checklist (new or changed points)

- [ ] Composed from Utah abstracts (no parallel role inventing)
- [ ] Non-abstract type name unique
- [ ] Role suffix correct (`Enab` / `Cmd` / `Sts` / `Pos` / `Spd` / `Sp` / …)
- [ ] Naming triad aligned (type / slot / navName)
- [ ] Abbrevs from the glossary
- [ ] `doc` present and distinguishing; no section-banner-as-doc
- [ ] History via mixin, not one-off tags
- [ ] Matching feedback type exists when defining a Cmd/Pos/Spd (slot may still be `?`)

## Out of scope (for now)

- Formal point grouping meta (`utahGroup`, etc.)
- Automated lint (future)
- Bulk renames (do by equip family after inventory)

## Inventory

Latest read-only scan: [CONVENTIONS-INVENTORY.md](CONVENTIONS-INVENTORY.md) (regen via `_inventory_conventions.py`).
