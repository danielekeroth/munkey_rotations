# Getting Started

This guide will help you understand the basics of Munkey Rotations and get you up and running quickly.

## What is a Rotation File?

A rotation file is a YAML document that defines when and how to cast spells. The system evaluates conditions in order and executes the first matching action.

## Basic File Structure

Every rotation file follows this structure:

```yaml
version: 1
entry: main

config:
  # User-customizable settings
  health_threshold:
    label: "Emergency Heal %"
    type: slider
    min: 10
    max: 50
    default: 30

variables:
  # Reusable expressions
  is_low_health: health.pct<config.health_threshold

lists:
  main:
    - spell_name,if=condition
    - another_spell,if=another_condition
```

## Key Sections

### `entry`
Specifies which action list runs first (usually `main`).

### `config`
Defines settings that users can customize in the UI. See [Configuration Options](Configuration-Options) for details.

### `variables`
Creates reusable expressions. Reference them with `var.variable_name`.

### `lists`
Contains your action lists (rotation logic). Each list is a sequence of spell actions with conditions.

## Basic Spell Syntax

The fundamental syntax is:

```yaml
- spell_name,if=condition
```

### Examples

```yaml
# Cast Fireball if target exists
- fireball,if=target.exists

# Cast Execute when target is below 20% health
- execute,if=target.health.pct<=20

# Cast Shield when you're below 50% health AND not moving
- shield,if=health.pct<50&!player.moving
```

## Essential Expressions

Here are the most commonly used expressions:

### Player Resources
| Expression | Description |
|-----------|-------------|
| `health.pct` | Your health percentage |
| `mana.pct` | Your mana percentage |
| `energy` | Current energy |
| `combo_points` | Current combo points |
| `holy_power` | Current holy power |

### Target Info
| Expression | Description |
|-----------|-------------|
| `target.exists` | Target exists |
| `target.health.pct` | Target's health % |
| `target.range` | Distance to target |
| `target.boss` | Target is a boss |

### Buffs & Debuffs
| Expression | Description |
|-----------|-------------|
| `buff.spell_name.up` | You have the buff |
| `buff.spell_name.remains` | Seconds until buff expires |
| `debuff.spell_name.up` | Target has debuff |

### Cooldowns
| Expression | Description |
|-----------|-------------|
| `cooldown.spell.ready` | Spell is off cooldown |
| `cooldown.spell.remains` | Seconds until ready |

## Operators

### Boolean Operators
| Operator | Meaning |
|----------|---------|
| `&` | AND |
| `|` | OR |
| `!` | NOT |

### Comparison Operators
| Operator | Meaning |
|----------|---------|
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `=` | Equal |
| `!=` | Not equal |

## Your First Rotation

Here's a simple example rotation:

```yaml
version: 1
entry: main

config:
  emergency_health:
    label: "Emergency Heal %"
    type: slider
    min: 10
    max: 50
    default: 30

lists:
  main:
    # Don't run if rotation is disabled
    - return,if=!state.rotation
    
    # Emergency self-heal
    - flash_heal.player,if=health.pct<config.emergency_health
    
    # Apply DoT if missing
    - shadow_word_pain,if=debuff.shadow_word_pain.down
    
    # Filler spell
    - smite
```

## Next Steps

- Learn about [Rotation Syntax Basics](Rotation-Syntax-Basics) for more operators and expressions
- Explore [Buff and Debuff Tracking](Buff-and-Debuff-Tracking) for aura management
- Check out [Configuration Options](Configuration-Options) to make your rotation customizable
