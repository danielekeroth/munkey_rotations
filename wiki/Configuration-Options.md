# Configuration Options

This guide covers how to create user-customizable settings in your rotations, allowing users to adjust behavior without editing the YAML directly.

## Overview

Configuration options create UI controls (sliders, checkboxes, dropdowns) that users can adjust. These are defined in the `config:` section and referenced with `config.OPTION_NAME`.

## Basic Syntax

```yaml
config:
  option_name:
    label: "Display Label"
    type: TYPE
    default: VALUE
    # Additional properties based on type
```

## Configuration Types

### Slider

Creates a numeric slider for threshold values:

```yaml
config:
  health_threshold:
    label: "Emergency Heal %"
    type: slider
    min: 10
    max: 100
    default: 30
```

Use in conditions:

```yaml
- emergency_heal,if=health.pct<config.health_threshold
```

### Checkbox

Creates a boolean toggle:

```yaml
config:
  use_interrupts:
    label: "Enable Interrupts"
    type: checkbox
    default: true
```

Use in conditions:

```yaml
- kick,if=config.use_interrupts&target.casting.interruptible
```

### Dropdown

Creates a single-selection dropdown:

```yaml
config:
  burst_mode:
    label: "Burst Strategy"
    type: dropdown
    options:
      - label: "Conservative"
        value: 1
      - label: "Normal"
        value: 2
      - label: "Aggressive"
        value: 3
    default: 2  # Default to "Normal"
```

Use in conditions:

```yaml
# Check exact value
- cooldown,if=config.burst_mode=3

# Check threshold
- pooling,if=config.burst_mode<=2
```

### Multi-Select

Creates a multi-selection dropdown (multiple options can be selected):

```yaml
config:
  features:
    label: "Features"
    type: multi_select
    options:
      - label: "Smart CDs"
        value: 1
      - label: "Interrupts"
        value: 2
      - label: "Defensives"
        value: 3
    default: [0, 1, 2]  # Indices (0-based) - all selected
```

Use the `.has()` function to check selections:

```yaml
# Check if option is selected (by value)
- interrupt,if=config.features.has(2)

# Check if option is selected (by label)
- defensive,if=config.features.has(Defensives)

# Check count of selected options
- spell,if=config.features>=2
```

## Real-World Examples

### Feature Toggles (Retribution Paladin)

```yaml
config:
  features:
    label: "Features"
    type: multi_select
    options:
      - label: "Smart CDs"
        value: 1
      - label: "Interrupts"
        value: 2
      - label: "Defensives"
        value: 3
    default: [0, 1, 2]

variables:
  use_smart_cds: config.features.has(1)
  use_interrupts: config.features.has(2)
  use_defensives: config.features.has(3)

lists:
  main:
    - call_action_list,name=interrupts,if=var.use_interrupts
    - call_action_list,name=emergency_healing,if=var.use_defensives
```

### Defensive Toggles with Thresholds

```yaml
config:
  defensive_toggles:
    label: "Defensive Toggles"
    type: multi_select
    options:
      - label: "Word of Glory"
        value: 1
      - label: "Lay on Hands"
        value: 2
      - label: "Divine Shield"
        value: 3
    default: [0, 1, 2]
    
  wog_usage:
    label: "Word of Glory HP%"
    type: slider
    default: 30
    min: 0
    max: 100
    
  loh_usage:
    label: "Lay on Hands HP%"
    type: slider
    default: 20
    min: 0
    max: 100

variables:
  use_wog: config.defensive_toggles.has(1)
  use_loh: config.defensive_toggles.has(2)

lists:
  defensives:
    - word_of_glory,if=var.use_wog&health.pct<=config.wog_usage
    - lay_on_hands,if=var.use_loh&health.pct<=config.loh_usage&debuff.forbearance.down
```

### Interrupt Configuration

```yaml
config:
  interrupt_target:
    label: "Interrupt Target"
    type: checkbox
    default: true
    
  interrupt_mouseover:
    label: "Interrupt Mouseover"
    type: checkbox
    default: true

variables:
  should_interrupt: config.interrupt_target&(target.casting.important|target.channeling.important)
  should_interrupt_mo: config.interrupt_mouseover&(mouseover.casting.important|mouseover.channeling.important)

lists:
  interrupts:
    - rebuke,if=var.should_interrupt
    - rebuke.mouseover,if=var.should_interrupt_mo
```

### AoE Threshold

```yaml
config:
  aoe_threshold:
    label: "AoE Threshold"
    type: slider
    default: 3
    min: 1
    max: 10

variables:
  is_aoe_combat: active_enemies>=config.aoe_threshold
  is_st_combat: active_enemies<config.aoe_threshold

lists:
  main:
    - call_action_list,name=st,if=var.is_st_combat
    - call_action_list,name=aoe,if=var.is_aoe_combat
```

### Cooldown Usage Strategy

```yaml
config:
  ignore_ttd_on_boss:
    label: "Ignore TTD on Boss"
    type: checkbox
    default: true
    
  ttd_cd_usage:
    label: "TTD CD Usage (s)"
    type: slider
    default: 20
    min: 0
    max: 30

variables:
  is_ttd_valid: time_to_die<9999&player.combat
  should_use_cds: state.cds&((config.ignore_ttd_on_boss&target.boss)|time_to_die>config.ttd_cd_usage)

lists:
  cooldowns:
    - major_cd,if=var.should_use_cds
```

### Mouseover Healing (Discipline Priest)

```yaml
config:
  MO_enabled:
    label: "Enable Mouseover"
    type: checkbox
    default: true
    
  MO_penance:
    label: "Use Penance on MO"
    type: checkbox
    default: true
    
  MO_penance_threshold:
    label: "MO Penance HP%"
    type: slider
    default: 60
    min: 10
    max: 100

lists:
  mouseover_friendly:
    - penance.mouseover,if=config.MO_penance&mouseover.health.pct<config.MO_penance_threshold
    
  main:
    - call_action_list,name=mouseover_friendly,if=config.MO_enabled&mouseover.friendly
```

### Trinket Usage Strategy

```yaml
config:
  living_silk_usage:
    label: "Living Silk Usage"
    type: dropdown
    options:
      - label: "On Cooldown"
        value: 1
      - label: "X Members below %"
        value: 2
      - label: "Do not use"
        value: 3
    default: 1
    
  living_silk_members_threshold:
    label: "Living Silk Members"
    type: slider
    min: 1
    max: 5
    default: 3

variables:
  trinket1_living_silk: trinket_1.id=242393
  should_use_ls: config.living_silk_usage!=3&(config.living_silk_usage=1|group.under_pct_50>=config.living_silk_members_threshold)

lists:
  trinkets:
    - trinket_1,if=var.trinket1_living_silk&trinket_1.ready&var.should_use_ls
```

## Pain Suppression Role Priority (Disc Priest)

```yaml
config:
  pain_suppression_threshold:
    label: "Pain Suppression HP%"
    type: slider
    min: 10
    max: 60
    default: 20
    
  pain_suppression_usage:
    label: "Use PS on"
    type: dropdown
    options:
      - label: "Tank Only"
        value: 1
      - label: "Tank & Healer"
        value: 2
      - label: "Everyone"
        value: 3
      - label: "Disabled"
        value: 0
    default: 2

lists:
  pain_suppression_logic:
    # Tanks always (if not disabled)
    - pain_suppression,cycle=tanks,if=config.pain_suppression_usage!=0&cycle.health.pct<config.pain_suppression_threshold
    
    # Healers if setting >= 2
    - pain_suppression,cycle=healers,if=config.pain_suppression_usage>=2&cycle.health.pct<config.pain_suppression_threshold
    
    # Everyone if setting = 3
    - pain_suppression,cycle=members,if=config.pain_suppression_usage=3&cycle.health.pct<config.pain_suppression_threshold
```

## UI Display Order

Config entries are displayed in the order they appear in the YAML file. Group related settings together for a clean UI.

## Legacy Alias

`settings.NAME` works the same as `config.NAME` for backwards compatibility.

## Shared Config

Settings can also be defined in `_shared.yaml` under `config_shared:` to be available to all rotations. Rotation-specific config takes priority over shared config.

## Best Practices

1. **Use descriptive labels** - Make it clear what each setting does
2. **Set sensible defaults** - Most users won't change settings
3. **Group related options** - Feature toggles together, thresholds together
4. **Use variables** - Convert complex config checks to readable variables
5. **Provide disable options** - Let users turn off features they don't want

## Quick Reference

| Type | Returns | Check Syntax |
|------|---------|--------------|
| `slider` | number | `config.X>=50` |
| `checkbox` | 0/1 | `config.X` or `!config.X` |
| `dropdown` | selected value | `config.X=2` |
| `multi_select` | count selected | `config.X.has(VALUE)` |

## Next Steps

- Learn about [Variables and Action Lists](Variables-and-Action-Lists) to organize config usage
- See [Advanced Examples](Advanced-Examples) for complete configuration patterns
- Check [Healing Targeting](Healing-Targeting) for configurable heal thresholds
