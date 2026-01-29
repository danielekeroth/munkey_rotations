# Rotation Syntax Basics

This page covers the core syntax used in rotation files, including spell actions, operators, and fundamental expressions.

## Action Syntax

Every action in a rotation follows this pattern:

```yaml
- spell_name,option=value,if=condition
```

### Components

| Component | Required | Description |
|-----------|----------|-------------|
| `spell_name` | Yes | The spell to cast (use underscores for spaces) |
| `option=value` | No | Additional options like `target=`, `cycle=`, `range_check=` |
| `if=condition` | No | Condition that must be true to cast |

### Examples

```yaml
# Simple spell (always casts if available)
- fireball

# Spell with condition
- fireball,if=!player.moving

# Spell with target modifier
- flash_heal.mouseover,if=mouseover.health.pct<80

# Spell with options
- holy_shock,cycle=members,if=cycle.health.pct<70
```

## Operators

### Boolean Operators

| Operator | Name | Example |
|----------|------|---------|
| `&` | AND | `health.pct<50&buff.shield.down` |
| `\|` | OR | `health.pct<30\|buff.emergency.up` |
| `!` | NOT | `!player.moving` |

### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `<` | Less than | `health.pct<50` |
| `<=` | Less or equal | `range<=8` |
| `>` | Greater than | `energy>50` |
| `>=` | Greater or equal | `holy_power>=3` |
| `=` | Equal | `combo_points=5` |
| `!=` | Not equal | `target.npcid!=12345` |

### Arithmetic Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `+` | Addition | `gcd+gcd.remaining` |
| `-` | Subtraction | `health.max-health.current` |
| `*` | Multiplication | `combat.time>gcd*7` |
| `/` | Division | `mana/mana.max` |
| `>?` | Min (SimC) | `a>?b` returns smaller value |
| `<?` | Max (SimC) | `a<?b` returns larger value |

### Operator Precedence

Use parentheses to control evaluation order:

```yaml
# Without parentheses - may not work as expected
- spell,if=health.pct<50|buff.shield.up&target.boss

# With parentheses - clear intent
- spell,if=(health.pct<50|buff.shield.up)&target.boss
```

## Cast Target Modifiers

Append these to spell names to cast on specific targets:

| Modifier | Target | Example |
|----------|--------|---------|
| `.player` | Yourself | `flash_heal.player` |
| `.focus` | Focus target | `polymorph.focus` |
| `.mouseover` | Mouseover unit | `heal.mouseover` |
| `.cursor` | Ground at cursor | `blizzard.cursor` |

```yaml
# Self-heal when low
- flash_heal.player,if=health.pct<40

# Ground-targeted AoE at cursor
- blizzard.cursor,if=active_enemies>=3

# Heal mouseover target
- renew.mouseover,if=mouseover.friendly&mouseover.health.pct<90
```

> **Note**: Range is automatically checked based on the target modifier. You don't need to add manual range conditions.

## Step Options

Actions can have additional options that control execution:

### `range_check`

Controls range validation:

```yaml
# Default - requires target in range
- attack_spell,if=target.exists

# No range check (for self-buffs)
- self_buff,range_check=none,if=buff.my_buff.down

# Require enemies nearby
- whirlwind,range_check=mob_count_8y,if=active_enemies>=2
```

### `interrupt`

Allow interrupting your current cast:

```yaml
# Emergency heal can interrupt current cast
- emergency_heal,interrupt=true,if=health.pct<15
```

### `ignore_movement`

Cast spells that can be used while moving:

```yaml
# Scorch can be cast while moving
- scorch,ignore_movement=true,if=player.moving
```

### `delay` / `global_delay`

Control timing between casts:

```yaml
# Minimum 100ms between presses for this spell
- channeled_spell,delay=100,if=condition

# Block all spells for 100ms after this cast
- channeled_spell,global_delay=100,if=condition
```

### `override`

Use another spell's keybind:

```yaml
# Check vampiric_strike but press heart_strike key
- vampiric_strike,override=heart_strike,if=buff.vampiric_strike.up
```

## Control Actions

Special actions that control rotation flow:

### `return`

Stop evaluating the current action list:

```yaml
# Skip rotation if disabled or player is dead
- return,if=!state.rotation|player.dead

# Skip if no valid target
- return,if=!target.valid
```

### `call_action_list`

Call another action list, then continue:

```yaml
- call_action_list,name=cooldowns,if=target.boss
- call_action_list,name=aoe,if=active_enemies>=3
```

### `run_action_list`

Run another list, then restart from the beginning:

```yaml
- run_action_list,name=opener,if=combat.time<10
```

## Resource Expressions

### Generic Resources

| Resource | Classes | Properties |
|----------|---------|------------|
| `rage` | Warrior, Druid | `.max`, `.deficit` |
| `energy` | Rogue, Monk, Feral | `.max`, `.deficit`, `.pct`, `.regen`, `.time_to_max` |
| `mana` | Casters | `.max`, `.deficit`, `.pct`, `.regen`, `.time_to_max` |
| `focus` | Hunter | `.max`, `.deficit`, `.pct`, `.regen`, `.time_to_max` |
| `runic_power` | Death Knight | `.max`, `.deficit` |
| `holy_power` | Paladin | `.max` |
| `combo_points` | Rogue, Feral | `.max` |
| `insanity` | Shadow Priest | `.max`, `.deficit` |
| `chi` | Monk | `.max` |
| `soul_shards` | Warlock | `.max` |
| `fury` | Demon Hunter | `.max`, `.deficit` |

### Examples

```yaml
# Cast at max combo points
- finisher,if=combo_points=combo_points.max

# Pool energy before cooldown
- pooling_action,if=energy.time_to_max<3

# Use expensive spell when mana is high
- expensive_heal,if=mana.pct>75
```

## Player State Expressions

| Expression | Description |
|-----------|-------------|
| `player.moving` | Player is moving |
| `player.casting` | Player is casting |
| `player.channeling` | Player is channeling |
| `player.combat` | Player is in combat |
| `player.mounted` | Player is mounted |
| `combat.time` | Seconds in combat |

```yaml
# Only cast when standing still
- long_cast,if=!player.moving

# Skip if mounted
- return,if=player.mounted

# Opener logic
- opener_spell,if=combat.time<5
```

## Target Expressions

| Expression | Description |
|-----------|-------------|
| `target.exists` | Target exists |
| `target.alive` | Target is alive |
| `target.enemy` | Target is hostile |
| `target.friendly` | Target is friendly |
| `target.boss` | Target is a boss |
| `target.range` | Distance in yards |
| `target.health.pct` | Target's HP % |
| `target.time_to_die` | Estimated seconds to death |
| `target.valid` | Comprehensive check (exists, enemy, alive, in combat) |

```yaml
# Skip if no valid target
- return,if=!target.valid

# Execute phase
- execute,if=target.health.pct<=20

# Long DoT only if target will live
- long_dot,if=target.time_to_die>15
```

## Enemy Count Expressions

| Expression | Description |
|-----------|-------------|
| `active_enemies` | Enemies in combat range |
| `enemies.8y` | All enemies within 8 yards |
| `enemies.combat.8y` | Combat enemies within 8 yards |
| `enemies.combat.40y` | Combat enemies within 40 yards |

```yaml
# AoE threshold
- aoe_spell,if=active_enemies>=3

# Cleave at melee range
- cleave,if=enemies.combat.8y>=2
```

## Next Steps

- Learn about [Buff and Debuff Tracking](Buff-and-Debuff-Tracking)
- Explore [Cooldown Management](Cooldown-Management)
- See [Healing Targeting](Healing-Targeting) for group-based logic
