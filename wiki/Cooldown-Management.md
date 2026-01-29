# Cooldown Management

This guide covers tracking and intelligently using cooldowns, including charged abilities and trinkets.

## Basic Cooldown Syntax

```yaml
cooldown.SPELL_NAME.PROPERTY
```

## Available Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `.ready` | 0/1 | Spell is off cooldown |
| `.up` | 0/1 | Same as `.ready` |
| `.down` | 0/1 | Spell is on cooldown |
| `.remains` | seconds | Time until ready |

## Charged Ability Properties

For spells with multiple charges:

| Property | Returns | Description |
|----------|---------|-------------|
| `.charges` | number | Current charge count |
| `.max_charges` | number | Maximum charges |
| `.full_recharge_time` | seconds | Time until all charges restored |
| `.charges_fractional` | decimal | Charges including partial progress |

## Basic Examples

### Using When Ready

```yaml
# Cast major cooldown when ready
- big_cooldown,if=cooldown.big_cooldown.ready

# Use trinket when off CD
- trinket_1,if=cooldown.trinket_1.ready
```

### Pooling for Cooldowns

```yaml
# Pool resources when CD is almost ready
- pooling_action,if=cooldown.burst.remains<5

# Don't use charges if CD is about to cap
- charged_spell,if=cooldown.charged_spell.charges>=1
```

### Charge Management

```yaml
# Use if we have charges
- blink,if=cooldown.blink.charges>=1

# Don't cap charges
- roll,if=cooldown.roll.charges=cooldown.roll.max_charges

# Use charge before full recharge
- chi_torpedo,if=cooldown.chi_torpedo.full_recharge_time<3

# Precise timing with fractional charges
- fire_blast,if=cooldown.fire_blast.charges_fractional>=1.8
```

## Smart Cooldown Usage

### Time to Die (TTD) Checks

Only use cooldowns if the fight will last long enough:

```yaml
# Only use if target will live 20+ seconds
- big_cooldown,if=target.time_to_die>20

# Check fight duration
- major_cd,if=fight_remains>30
```

### Boss-Only Cooldowns

```yaml
# Save big CDs for bosses
- avenging_wrath,if=target.boss

# Or in boss encounters
- major_cooldown,if=player.boss_fight
```

### Smart CD Logic (from Retribution Paladin)

```yaml
variables:
  # Check if TTD values are valid (not default 9999)
  is_ttd_valid: time_to_die<9999&player.combat
  is_fight_remains_valid: fight_remains<9999&player.combat
  
  # Check if fight/target will last long enough
  is_ttd_or_fm_above_treshold: ((fight_remains>=config.ttd_cd_usage&is_fight_remains_valid)|(time_to_die>config.ttd_cd_usage&is_ttd_valid))
  
  # Combined logic: use if CDs enabled AND (smart mode off OR valid TTD)
  should_use_cds: (state.cds&!var.use_smart_cds)|(state.cds&var.use_smart_cds&((config.ignore_ttd_on_boss&target.boss)|var.is_ttd_or_fm_above_treshold))

lists:
  main:
    - avenging_wrath,if=var.should_use_cds
    - execution_sentence,if=var.should_use_cds
    - divine_toll,if=var.should_use_cds
```

## Trinket System

### Basic Trinket Expressions

| Expression | Description |
|-----------|-------------|
| `trinket_1.ready` | Trinket 1 off cooldown |
| `trinket_1.cd` | Trinket 1 cooldown remaining |
| `trinket_1.id` | Item ID of Trinket 1 |
| `trinket_1.usable` | Ready and CDs enabled |
| `trinket_1.sync` | Smart sync check (see below) |

### Trinket Sync

`trinket_X.sync` is a combined check:
1. Trinket is ready (off cooldown)
2. Trinket is not disabled in `_trinkets.yaml`
3. Trinket's custom condition passes (if defined)
4. Any burst buff is active (unless `check_burst: false`)

```yaml
# Use trinket with smart sync
- trinket_1,if=trinket_1.sync
- trinket_2,if=trinket_2.sync
```

### Specific Trinket Checks

```yaml
# Check for specific trinket by ID
- special_spell,if=trinket_1.id=207141

# Conditional trinket use
- trinket_2,if=trinket_2.ready&buff.bloodlust.up
```

### Living Silk Example (from Disc Priest)

```yaml
variables:
  trinket1_living_silk: trinket_1.id=242393
  trinket2_living_silk: trinket_2.id=242393
  trinket_living_silk: var.trinket1_living_silk|var.trinket2_living_silk

lists:
  living_silk:
    - trinket_1,if=var.trinket1_living_silk&trinket_1.cd=0&config.living_silk_usage!=3
    - trinket_2,if=var.trinket2_living_silk&trinket_2.cd=0&config.living_silk_usage!=3
```

## Other Equipment

### Weapon Enchants

```yaml
# Check for temporary enchant (poison, oil)
- instant_poison,if=!mainhand.enchant.up
- deadly_poison,if=mainhand.enchant.remains<300

# Offhand for dual-wield
- wound_poison,if=!offhand.enchant.up
```

### Equipment On-Use

```yaml
# Use equipment on-use effects
- weapon_onuse,if=weapon.ready
- wrist_onuse,if=wrist.ready
- belt_onuse,if=belt.ready
```

### Tier Set Bonuses

Define tier pieces in your rotation:

```yaml
tier_sets:
  tier33:
    head: 212345
    shoulder: 212346
    chest: 212347
    hands: 212348
    legs: 212349
```

Then check bonuses:

```yaml
# 2-piece bonus
- tier_spell,if=set_bonus.tier33_2pc

# 4-piece bonus
- tier_spell,if=set_bonus.tier33_4pc
```

## Consumables

### Consumable Checks

| Expression | Description |
|-----------|-------------|
| `healthstone.ready` | Healthstone available |
| `healthstone.cd` | Healthstone cooldown |
| `health_potion.ready` | Health potion available |
| `combat_potion.ready` | DPS potion available |

### Examples

```yaml
# Emergency healthstone
- healthstone,if=health.pct<30&healthstone.ready

# Potion on boss with cooldowns
- combat_potion,if=combat_potion.ready&target.boss&buff.bloodlust.up
```

## Burst Detection

Track if major cooldowns are active:

| Expression | Description |
|-----------|-------------|
| `player.burst.active` | Any burst buff is up |
| `player.burst.count` | Number of active burst buffs |

```yaml
# Stack cooldowns during burst
- big_cooldown,if=player.burst.count>=2

# Use trinket during burst window
- trinket_1,if=player.burst.active&trinket_1.ready
```

## Usable Check

Check if a spell is usable (resources + cooldown):

```yaml
usable.SPELL_NAME
```

```yaml
# Only if we have resources and it's ready
- expensive_ability,if=usable.expensive_ability
```

## Coordinating Cooldowns

### Stacking CDs

```yaml
lists:
  cooldowns:
    # Stack when main CD is ready
    - main_cooldown,if=cooldown.main_cooldown.ready
    - secondary_cd,if=buff.main_cooldown.up
    - trinket_1,if=buff.main_cooldown.up&trinket_1.ready
    
  main:
    - call_action_list,name=cooldowns,if=state.cds&target.boss
```

### Aligning with GCD

```yaml
# Wait for GCD
- spell,if=gcd.remains<0.2&cooldown.spell.ready

# Check execute time vs cooldown
- timed_spell,if=action.nuke.execute_time<cooldown.burst.remains
```

## Action Properties

For precise timing:

| Expression | Description |
|-----------|-------------|
| `action.SPELL.charges` | Charges available |
| `action.SPELL.cast_time` | Cast time in seconds |
| `action.SPELL.execute_time` | Max of cast time and GCD |

```yaml
# Choose filler based on remaining time
- instant_spell,if=cooldown.burst.remains<action.long_cast.cast_time
```

## Real-World Example

### Retribution Paladin CD Management

```yaml
config:
  ttd_cd_usage:
    label: "TTD CD Usage (s)"
    type: slider
    default: 20
    min: 0
    max: 30

variables:
  use_smart_cds: config.features.has(1)
  is_ttd_valid: time_to_die<9999&player.combat
  should_use_cds: (state.cds&!var.use_smart_cds)|(state.cds&var.use_smart_cds&target.time_to_die>config.ttd_cd_usage)

lists:
  main:
    # Opener CD usage
    - avenging_wrath,if=!talent.radiant_glory&var.should_use_cds
    
    # Sync potion with wings
    - combat_potion,if=buff.avenging_wrath.up&player.inraid&combat_potion.ready
    
    # Trinkets with CDs
    - trinket_1,if=trinket_1.ready&var.should_use_cds
    - trinket_2,if=trinket_2.ready&var.should_use_cds
```

## Quick Reference

| Pattern | Syntax |
|---------|--------|
| Use when ready | `cooldown.SPELL.ready` |
| Pool before CD | `cooldown.SPELL.remains<5` |
| Has charges | `cooldown.SPELL.charges>=1` |
| Don't cap charges | `cooldown.SPELL.charges=cooldown.SPELL.max_charges` |
| TTD check | `target.time_to_die>20` |
| Trinket sync | `trinket_1.sync` |
| During burst | `player.burst.active` |
| Boss only | `target.boss` |

## Next Steps

- Learn about [Configuration Options](Configuration-Options) for user-customizable CD settings
- See [Variables and Action Lists](Variables-and-Action-Lists) for organizing CD logic
- Check [Advanced Examples](Advanced-Examples) for complete CD patterns
