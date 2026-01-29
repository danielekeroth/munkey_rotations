# Buff and Debuff Tracking

This guide covers how to monitor, track, and react to buffs and debuffs (collectively called "auras") in your rotations.

## Basic Syntax

### Buff Expressions

Check buffs on the **player**:

```yaml
buff.SPELL_NAME.PROPERTY
```

### Debuff Expressions

Check debuffs on the **current target**:

```yaml
debuff.SPELL_NAME.PROPERTY
```

## Available Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `.up` | 0/1 | Aura is active |
| `.down` | 0/1 | Aura is NOT active |
| `.react` | 0/1 | Same as `.up` (for procs) |
| `.remains` | seconds | Time until aura expires |
| `.elapsed` | seconds | Time since aura was applied |
| `.stack` | number | Current stack count |
| `.duration` | seconds | Base duration of aura |
| `.refreshable` | 0/1 | Within pandemic refresh window |

## Source Filtering: `.any` Suffix

> **Important**: By default, buff and debuff checks only match auras **applied by the player**.

To check for auras from **any source**, add the `.any` suffix:

| Expression | Checks |
|-----------|--------|
| `buff.renew.up` | **Your** Renew is active |
| `buff.renew.up.any` | **Any** Renew is active (from any healer) |
| `debuff.rip.up` | **Your** Rip is on target |
| `debuff.rip.up.any` | **Any** Rip is on target |

### Examples

```yaml
# Only refresh YOUR Renew if low duration
- renew,if=buff.renew.remains<3

# Skip if target already has ANY Renew
- renew,if=buff.renew.down.any

# Skip if ANY priest has Fort on the target
- power_word_fortitude,if=buff.power_word_fortitude.down.any
```

## Buff Examples

### Check if Buff is Active

```yaml
# Use empowered ability when buff is up
- empowered_strike,if=buff.empowerment.up

# Maintain buff before it falls off
- refresh_buff,if=buff.my_buff.remains<5
```

### React to Procs

```yaml
# Consume proc immediately
- instant_pyroblast,if=buff.hot_streak.react

# Use proc-based ability
- sudden_doom_strike,if=buff.sudden_doom.up
```

### Stack Tracking

```yaml
# Consume stacks at 3+
- consume_stacks,if=buff.power_stacks.stack>=3

# Wait for max stacks
- big_ability,if=buff.building_power.stack=10
```

### Pandemic Refresh

The `.refreshable` property returns true when the aura is within pandemic refresh window (typically 30% of duration or less remaining):

```yaml
# Refresh buff in pandemic window
- maintain_buff,if=buff.haste_buff.refreshable
```

## Debuff Examples

### Maintain DoTs

```yaml
# Apply DoT if missing
- corruption,if=debuff.corruption.down

# Refresh before expiry
- corruption,if=debuff.corruption.remains<3

# Use pandemic refresh
- corruption,if=debuff.corruption.refreshable
```

### Check Enemy Debuffs

```yaml
# Follow up when debuff is active
- execute,if=debuff.vulnerability.up

# Build stacks
- wound_strike,if=debuff.wound.stack<5
```

## DoT Alias

The `dot.*` syntax is equivalent to `debuff.*` for target debuffs:

```yaml
# These are equivalent:
- corruption,if=debuff.corruption.refreshable
- corruption,if=dot.corruption.refreshable
```

## Counting Active DoTs

Use `active_dot.SPELL` to count enemies with your DoT:

```yaml
# Spread DoT if fewer than 3 targets have it
- multi_dot,if=active_dot.corruption<3

# Full DoT coverage
- maintain_dots,if=active_dot.corruption=active_enemies
```

With `.any` suffix for any source:

```yaml
# Check any source
- spread_corruption,if=active_dot.corruption.any<active_enemies
```

## Checking Other Units

### Player Debuffs

Check debuffs on yourself:

```yaml
# Check if you have a debuff
player.debuff.SPELL.up
player.debuff.SPELL.remains

# Check for any debuff type
player.has_magic_debuff
player.has_curse
player.has_disease
player.has_poison
```

### Target Buffs

Check buffs on the target (enemy):

```yaml
# Target has a stealable buff
target.has_stealable

# Target has any magic buff
target.has_magic_buff

# Target is enraged
target.has_enrage
```

### Other Units (Function Syntax)

For focus/mouseover/pet, use function-call syntax:

```yaml
# Focus buff remaining
focus.buff.remains(shield)>5

# Mouseover debuff check
mouseover.debuff.remains(hex)=0

# Pet buff
pet.buff.frenzy.up
```

## Dispel Type Properties

Check the dispel category of an aura:

| Property | Description |
|----------|-------------|
| `.magic` | Aura is Magic type |
| `.curse` | Aura is Curse type |
| `.disease` | Aura is Disease type |
| `.poison` | Aura is Poison type |

```yaml
# Check dispel type
- dispel_magic,if=debuff.hex.curse
- cleanse,if=player.has_disease
```

## Source Check: `.mine`

Check if you applied an aura:

```yaml
# Only refresh YOUR DoT
- refresh_dot,if=debuff.corruption.mine&debuff.corruption.remains<5
```

## Aura Point Values

Some auras have numeric values (points) in their effects:

```yaml
# Check aura point value
- consume_buff,if=player.buff.stacking_power.points.1>5
- empowered_spell,if=target.debuff.vulnerability.points.2>10
```

## Nameplate Aggregations

Track auras across all visible nameplates:

| Expression | Description |
|-----------|-------------|
| `nameplates.debuff.SPELL.count` | Count with your debuff |
| `nameplates.debuff.SPELL.count.any` | Count with any source |
| `nameplates.debuff.SPELL.lowest` | Lowest duration remaining |
| `nameplates.debuff.SPELL.highest` | Highest duration remaining |

```yaml
# Spread DoT to nameplates
- multi_dot,if=nameplates.debuff.corruption.count<3

# Refresh lowest duration DoT
- corruption,if=nameplates.debuff.corruption.lowest<3
```

## Cycle Context Buffs

When using `cycle=` for group targeting, use `cycle.buff.*`:

```yaml
# Apply HoT to first member without YOUR HoT
- renew,cycle=members,if=cycle.buff.renew.down

# Apply HoT to first missing ANY HoT
- renew,cycle=members,if=cycle.buff.renew.down.any

# Refresh YOUR HoT if low
- renew,cycle=members,if=cycle.buff.renew.mine&cycle.buff.renew.remains<3
```

## Real-World Examples

### Maintaining Buffs (Retribution Paladin)

```yaml
# Check for Empyrean Legacy proc
variables:
  emp_legacy_procc: buff.empyrean_legacy.up

lists:
  combat:
    # Use proc when active
    - final_verdict,if=var.emp_legacy_procc
```

### DoT Management (Warlock)

```yaml
lists:
  dots:
    # Apply missing DoTs
    - corruption,if=debuff.corruption.down
    - agony,if=debuff.agony.down
    
    # Pandemic refresh
    - corruption,if=debuff.corruption.refreshable
    - agony,if=debuff.agony.refreshable
    
    # Multi-DoT in AoE
    - corruption,cycle=enemies,if=cycle.debuff.corruption.down&active_dot.corruption<4
```

### Atonement Tracking (Discipline Priest)

```yaml
variables:
  # Count members missing Atonement in range
  missing_atonement: group.count(cycle.buff.atonement.down&cycle.range<=40)

lists:
  atonement_spread:
    # Spread Atonement when many are missing
    - power_word_radiance.player,if=var.missing_atonement>10
    
    # Apply Atonement to individuals
    - power_word_shield,cycle=members,if=cycle.buff.atonement.down&cycle.range<=40
```

### Checking Forbearance (Paladin)

```yaml
# Only use if Forbearance debuff is not active
- lay_on_hands,if=debuff.forbearance.down&health.pct<20
- blessing_of_protection,if=debuff.forbearance.down&health.pct<30
```

## Quick Reference

| Pattern | Syntax |
|---------|--------|
| Buff active | `buff.SPELL.up` |
| Buff missing | `buff.SPELL.down` |
| Any source buff | `buff.SPELL.up.any` |
| Buff duration | `buff.SPELL.remains<X` |
| Buff stacks | `buff.SPELL.stack>=X` |
| Debuff active | `debuff.SPELL.up` |
| DoT refreshable | `dot.SPELL.refreshable` |
| Count DoTs | `active_dot.SPELL>=X` |
| Player has debuff | `player.has_magic_debuff` |
| Target stealable | `target.has_stealable` |

## Next Steps

- Learn about [Cooldown Management](Cooldown-Management) for ability timing
- See [Healing Targeting](Healing-Targeting) for group buff tracking
- Check [Variables and Action Lists](Variables-and-Action-Lists) for organizing complex buff logic
