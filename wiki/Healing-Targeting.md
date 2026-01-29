# Healing Targeting

This is one of the most important guides for healer rotations. It covers how to detect friendly units that are in range and below health thresholds - a common requirement for any healing rotation.

## Overview

The healing system provides two main targeting modes:

1. **Direct Targeting (`target=X`)** - Cast on a pre-resolved target (e.g., lowest HP member)
2. **Cycle Targeting (`cycle=X`)** - Iterate through group members and cast on first match

## The Core Question: "How do I heal friendly units in range below a threshold?"

This is solved using **cycle targeting** with range and health conditions:

```yaml
# Heal the first party/raid member who is:
# - In range (within 40 yards)
# - Below 70% health
- flash_heal,cycle=members,if=cycle.range<=40&cycle.health.pct<70
```

Let's break this down:
- `cycle=members` - Iterate through all group members (sorted by HP, lowest first)
- `cycle.range<=40` - Check if current member is within 40 yards
- `cycle.health.pct<70` - Check if current member is below 70% health

## Cycle Targeting

### Syntax

```yaml
- spell,cycle=GROUP,if=condition
```

### Available Groups

| Group | Description |
|-------|-------------|
| `members` | All party/raid members (sorted by HP, lowest first) |
| `tanks` | Only tanks (sorted by HP) |
| `healers` | Only healers (sorted by HP) |
| `dps` | Only DPS players (sorted by HP) |

### How Cycle Works

1. Gets list of members in the specified group
2. Sorts them by health (lowest first)
3. Iterates through each member
4. Evaluates your condition for each member (use `cycle.*` expressions)
5. Casts on the **first member** where all conditions pass

### Cycle Expressions

Inside `cycle=` conditions, use these expressions:

| Expression | Description |
|-----------|-------------|
| `cycle.health.pct` | Current member's health % |
| `cycle.health.current` | Current member's absolute HP |
| `cycle.health.max` | Current member's max HP |
| `cycle.health.deficit` | Missing HP (max - current) |
| `cycle.range` | Distance to current member |
| `cycle.dead` | Member is dead |
| `cycle.buff.SPELL.up` | Member has **your** buff |
| `cycle.buff.SPELL.down` | Member missing **your** buff |
| `cycle.buff.SPELL.up.any` | Member has buff from any source |
| `cycle.buff.SPELL.remains` | Your buff duration on member |
| `cycle.debuff.SPELL.*` | Debuff checks on member |

## Common Healing Patterns

### Basic Heal with Range Check

```yaml
# Heal anyone below 60% within 40 yards
- flash_heal,cycle=members,if=cycle.range<=40&cycle.health.pct<60
```

### Priority Tank Healing

```yaml
# Prioritize tanks below 50%
- heal,cycle=tanks,if=cycle.range<=40&cycle.health.pct<50

# Then heal anyone else below 40%
- heal,cycle=members,if=cycle.range<=40&cycle.health.pct<40
```

### HoT Application (Avoiding Duplicates)

```yaml
# Apply YOUR Renew to members missing YOUR Renew
- renew,cycle=members,if=cycle.range<=40&cycle.buff.renew.down

# Apply Renew to members missing ANY Renew (from any healer)
- renew,cycle=members,if=cycle.range<=40&cycle.buff.renew.down.any
```

### Configurable Threshold

```yaml
config:
  heal_threshold:
    label: "Heal below %"
    type: slider
    min: 30
    max: 90
    default: 70

lists:
  main:
    - flash_heal,cycle=members,if=cycle.range<=40&cycle.health.pct<config.heal_threshold
```

## Direct Targeting

For some spells, you want to always target the lowest member without iterating:

### Syntax

```yaml
- spell,target=TARGET_TYPE,if=condition
```

### Available Targets

| Target | Description |
|--------|-------------|
| `lowest` | Member with lowest HP |
| `tanks.lowest` | Tank with lowest HP |
| `healers.lowest` | Healer with lowest HP |
| `dps.lowest` | DPS with lowest HP |
| `missing.BUFF.lowest` | Lowest member missing a buff |

### Group Expressions for Direct Targeting

When using `target=`, use `group.*` expressions in your conditions:

| Expression | Description |
|-----------|-------------|
| `group.lowest.health.pct` | Lowest member's HP % |
| `group.lowest.health.deficit` | Lowest member's missing HP |
| `group.lowest.range` | Range to lowest member |
| `group.tanks.lowest.health.pct` | Lowest tank's HP % |
| `group.healers.lowest.health.pct` | Lowest healer's HP % |

### Examples

```yaml
# Heal lowest member when they're below 50%
- heal,target=lowest,if=group.lowest.health.pct<50

# Emergency heal on lowest tank
- emergency_heal,target=tanks.lowest,if=group.tanks.lowest.health.pct<25

# Apply buff to lowest member missing it
- fortitude,target=missing.power_word_fortitude.lowest
```

## Counting Group Members

Use `group.count()` to count members matching criteria:

### Syntax

```yaml
group.count(expression)
```

### Examples

```yaml
# Count members below 50% HP within 40 yards
group.count(cycle.health.pct<50&cycle.range<=40)

# Count members missing your Renew
group.count(cycle.buff.renew.down)

# Count dead members
group.count(cycle.dead)
```

### Using in Actions

```yaml
# AoE heal when 3+ members are low
- prayer_of_healing,if=group.count(cycle.health.pct<70&cycle.range<=40)>=3

# Emergency cooldown when many are critical
- aura_mastery,if=group.count(cycle.health.pct<30)>=4
```

## Shortcut Expressions

For common thresholds, these shortcuts are available:

| Expression | Equivalent |
|-----------|------------|
| `group.under_pct_30` | `group.count(cycle.health.pct<30)` |
| `group.under_pct_50` | `group.count(cycle.health.pct<50)` |
| `group.under_pct_75` | `group.count(cycle.health.pct<75)` |
| `group.under_pct_80` | `group.count(cycle.health.pct<80)` |
| `group.under_pct_85` | `group.count(cycle.health.pct<85)` |
| `group.under_pct_90` | `group.count(cycle.health.pct<90)` |

## Real-World Examples

### From Holy Paladin (rotation_65.yaml)

```yaml
variables:
  # Check if we should use single-target vs AoE heal
  should_use_eternal_flame: (!player.inraid&group.count(cycle.health.pct<80)<5)|buff.empyrean_legacy.up
  should_use_light_of_dawn: (player.inraid|group.count(cycle.health.pct<80)>=5)|buff.empyrean_legacy.up

lists:
  emergency_heal:
    # Cast Lay on Hands on first member below 15%
    - lay_on_hands,cycle=members,if=cycle.health.pct<15

  combat:
    # Aura Mastery in dungeons when 3+ below 70%
    - aura_mastery,if=var.group_members=5&group.count(cycle.health.pct<70)>=3
    
    # Aura Mastery in raids when 10+ below 70%
    - aura_mastery,if=var.group_members>5&group.count(cycle.health.pct<70)>=10
    
    # Holy Shock on lowest member
    - holy_shock,cycle=members,if=cycle.range<40
    
    # Flash of Light as filler
    - flash_of_light,target=lowest,if=!player.moving&group.count(cycle.health.pct<90)>=1
```

### From Discipline Priest (rotation_256.yaml)

```yaml
variables:
  # Count members missing Atonement within range
  missing_atonement: group.count(cycle.buff.atonement.down&cycle.range<=40)
  
  # Validate mouseover is friendly and in range  
  friendly_and_valid_mo: mouseover.exists&mouseover.alive&mouseover.friendly&mouseover.range>0&mouseover.range<=40

lists:
  pain_suppression_logic:
    # Priority: Tanks first, then healers, then everyone
    - pain_suppression,cycle=tanks,if=config.pain_suppression_usage!=0&cycle.health.pct<config.pain_suppression_threshold
    - pain_suppression,cycle=healers,if=config.pain_suppression_usage>=2&cycle.health.pct<config.pain_suppression_threshold
    - pain_suppression,cycle=members,if=config.pain_suppression_usage=3&cycle.health.pct<config.pain_suppression_threshold

  atonement_spread:
    # Spread Atonement to members missing it
    - power_word_shield,cycle=members,if=cycle.range>0&cycle.range<=40&!cycle.buff.power_word_shield.up&!cycle.buff.atonement.up
    - plea,cycle=members,if=cycle.range>0&cycle.range<=40&!cycle.buff.atonement.up
```

## Mouseover Healing

For instant mouseover heals (not iterating through group):

```yaml
# Heal mouseover if friendly and low
- flash_heal.mouseover,if=mouseover.friendly&mouseover.health.pct<50&mouseover.range<=40

# Apply HoT to mouseover
- renew.mouseover,if=mouseover.friendly&mouseover.buff.remains(renew)=0
```

## Dispelling

Combine cycle targeting with dispel conditions:

```yaml
# Dispel first member with a dispellable debuff
- purify,cycle=members,if=cycle.dispelable.list.purify
```

## Best Practices

1. **Always check range** - Use `cycle.range<=40` (or appropriate range)
2. **Use shortcuts** when possible - `group.under_pct_50` is cleaner than `group.count(...)`
3. **Priority order matters** - Put emergency heals first, then tanks, then general healing
4. **Test with different group sizes** - Rotations behave differently in 5-man vs raids
5. **Use configurable thresholds** - Let users customize heal percentages

## Summary

| Pattern | Syntax |
|---------|--------|
| Heal first low member | `spell,cycle=members,if=cycle.range<=40&cycle.health.pct<X` |
| Heal lowest member | `spell,target=lowest,if=group.lowest.health.pct<X` |
| Heal tanks first | `spell,cycle=tanks,if=cycle.range<=40&cycle.health.pct<X` |
| AoE heal condition | `spell,if=group.count(cycle.health.pct<X)>=3` |
| Apply missing buff | `spell,cycle=members,if=cycle.buff.SPELL.down` |

## Next Steps

- Learn about [Buff and Debuff Tracking](Buff-and-Debuff-Tracking) for HoT/DoT management
- See [Configuration Options](Configuration-Options) to make thresholds customizable
- Check [Advanced Examples](Advanced-Examples) for complete healer rotation patterns
