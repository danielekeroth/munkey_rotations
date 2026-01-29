# Variables and Action Lists

This guide covers how to organize complex rotations using reusable variables and modular action lists.

## Variables

Variables define reusable expressions that are evaluated each tick. They help make complex conditions readable and avoid repetition.

### Defining Variables

```yaml
variables:
  variable_name: expression
  another_variable: complex&expression|here
```

### Using Variables

Reference variables with `var.variable_name`:

```yaml
lists:
  main:
    - spell,if=var.variable_name
```

### Example: State Detection

```yaml
variables:
  # Combat states
  is_aoe_combat: active_enemies>=config.aoe_threshold
  is_st_combat: active_enemies<config.aoe_threshold
  opener_complete: combat.time>gcd*7
  
  # Execute phase
  execute_phase: target.health.pct<=20
  
  # Resource pooling
  pooling: cooldown.big_cooldown.remains<5&energy<80

lists:
  main:
    - call_action_list,name=opener,if=!var.opener_complete
    - call_action_list,name=st,if=var.is_st_combat
    - call_action_list,name=aoe,if=var.is_aoe_combat
    - execute_spell,if=var.execute_phase
```

### Example: Feature Flags from Config

```yaml
variables:
  # Convert config to readable flags
  use_smart_cds: config.features.has(1)
  use_interrupts: config.features.has(2)
  use_defensives: config.features.has(3)
  
  # Defensive ability toggles
  use_wog: config.defensive_toggles.has(1)
  use_loh: config.defensive_toggles.has(2)
  use_bop: config.defensive_toggles.has(3)
```

### Example: Complex CD Logic

```yaml
variables:
  # Validate TTD/fight_remains values
  is_ttd_valid: time_to_die<9999&player.combat
  is_fight_remains_valid: fight_remains<9999&player.combat
  
  # Check if fight is long enough for CDs
  is_ttd_or_fm_above_threshold: ((fight_remains>=config.ttd_cd_usage&var.is_fight_remains_valid)|(time_to_die>config.ttd_cd_usage&var.is_ttd_valid))
  
  # Final CD decision
  should_use_cds: (state.cds&!var.use_smart_cds)|(state.cds&var.use_smart_cds&((config.ignore_ttd_on_boss&target.boss)|var.is_ttd_or_fm_above_threshold))
```

### Example: Interrupt Logic

```yaml
variables:
  should_interrupt: config.interrupt_target&(target.casting.important|target.channeling.important)&!target.interrupt_immune
  should_interrupt_mouse: config.interrupt_mouseover&(mouseover.casting.important|mouseover.channeling.important)&!mouseover.interrupt_immune
```

### Example: Talent Detection

```yaml
variables:
  is_templar: talent.lights_guidance
  is_herald: talent.dawnlight
```

### Example: Healing Conditions

```yaml
variables:
  # Empyrean Legacy proc
  emp_legacy_procc: buff.empyrean_legacy.up
  
  # Count group members
  group_members: group.count(1=1)
  
  # Check if all are healthy
  all_healthy: group.count(cycle.health.pct<85)=var.group_members
  
  # Dead member count
  dead_members: group.count(cycle.dead)
  
  # AoE vs ST healing decision
  should_use_eternal_flame: (!player.inraid&group.count(cycle.health.pct<80)<5)|buff.empyrean_legacy.up
  should_use_light_of_dawn: (player.inraid|group.count(cycle.health.pct<80)>=5)|buff.empyrean_legacy.up
```

## Action Lists

Action lists are named sequences of actions. They help organize your rotation into logical phases.

### Defining Lists

```yaml
lists:
  list_name:
    - spell1,if=condition1
    - spell2,if=condition2
    
  another_list:
    - spell3,if=condition3
```

### Calling Lists

| Syntax | Behavior |
|--------|----------|
| `call_action_list,name=X` | Run list, then continue to next action |
| `run_action_list,name=X` | Run list, then restart rotation |
| `call=X` | Alias for `call_action_list` |

```yaml
lists:
  main:
    - call_action_list,name=defensives,if=health.pct<50
    - call_action_list,name=cooldowns,if=target.boss
    - call_action_list,name=aoe,if=active_enemies>=3
    - call_action_list,name=single_target
```

### Organization Patterns

#### Sanity Checks First

```yaml
lists:
  main:
    # Early exit conditions
    - return,if=!state.rotation|state.blocked_inputs|player.mounted|dead
    
    # Interrupts (always check)
    - call_action_list,name=interrupts,if=var.use_interrupts
    
    # Skip if out of combat
    - return,if=!player.combat
    
    # Emergency actions
    - call_action_list,name=emergency,if=health.pct<20
    
    # Main rotation
    - call_action_list,name=rotation
```

#### Phase-Based Organization

```yaml
lists:
  main:
    - call_action_list,name=sanity_checks
    - call_action_list,name=opener,if=!var.opener_complete
    - call_action_list,name=cooldowns,if=var.should_use_cds
    - call_action_list,name=finishers,if=combo_points>=5
    - call_action_list,name=builders
    
  opener:
    - spell1,name="Opener Step 1"
    - spell2,name="Opener Step 2"
    - spell3,name="Opener Step 3"
    
  cooldowns:
    - big_cd,if=cooldown.big_cd.ready
    - trinket_1,if=trinket_1.sync
    - trinket_2,if=trinket_2.sync
    
  finishers:
    - finisher1,if=buff.proc.up
    - finisher2
    
  builders:
    - builder1,if=debuff.dot.refreshable
    - builder2
```

#### AoE vs Single Target

```yaml
lists:
  main:
    - call_action_list,name=st,if=var.is_st_combat
    - call_action_list,name=aoe,if=var.is_aoe_combat
    
  st:
    - execution_sentence
    - hammer_of_light
    - final_verdict,if=holy_power>=5
    - blade_of_justice
    - hammer_of_wrath
    - judgment
    
  aoe:
    - execution_sentence
    - hammer_of_light
    - divine_storm,if=holy_power>=5
    - blade_of_justice
    - hammer_of_wrath
    - judgment
```

#### Opener Sequences

```yaml
lists:
  st_opener:
    - hammer_of_wrath,name="HoW (ST Opener - 1)",if=var.is_herald
    - divine_toll,name="Divine Toll (ST Opener - 2)",if=var.is_templar&var.should_use_cds
    - execution_sentence,name="ES (ST Opener - 3)",if=var.should_use_cds
    - final_verdict,name="FV (ST Opener - 4)",if=var.is_herald
    - wake_of_ashes,name="WoA (ST Opener - 5)",if=var.should_use_cds
    
  aoe_opener:
    - hammer_of_wrath,name="HoW (AoE Opener - 1)",if=var.is_herald
    - divine_toll,name="Divine Toll (AoE Opener - 2)",if=var.is_templar&var.should_use_cds
    - execution_sentence,name="ES (AoE Opener - 3)",if=var.should_use_cds
    - divine_storm,name="DS (AoE Opener - 4)",if=var.is_herald
    
  main:
    - call_action_list,name=st_opener,if=var.is_st_combat&!var.opener_complete
    - call_action_list,name=aoe_opener,if=var.is_aoe_combat&!var.opener_complete
```

#### Emergency Healing

```yaml
lists:
  emergency_healing:
    - divine_protection,if=var.use_dp&health.pct<=config.dp_usage
    - word_of_glory,if=var.use_wog&health.pct<=config.wog_usage
    - lay_on_hands,if=var.use_loh&debuff.forbearance.down&health.pct<=config.loh_usage
    - blessing_of_protection,if=var.use_bop&debuff.forbearance.down&health.pct<=config.bop_usage
    - divine_shield,if=var.use_ds&debuff.forbearance.down&health.pct<=config.ds_usage
    
  main:
    - call_action_list,name=emergency_healing,if=var.use_defensives
```

#### Interrupt Priority

```yaml
lists:
  interrupts:
    - rebuke,if=var.should_interrupt
    - rebuke.mouseover,if=var.should_interrupt_mouse
    
  main:
    - call_action_list,name=interrupts,if=var.use_interrupts
```

#### Movement Handling

```yaml
lists:
  moving:
    # Priority spells while moving
    - penance,cycle=members,if=cycle.health.pct<70
    - power_word_shield,cycle=members,if=!cycle.buff.power_word_shield.up
    - flash_heal,cycle=members,if=var.surge_of_light_procced
    
  main:
    - call_action_list,name=moving,if=player.moving
```

## Complete Example: Discipline Priest

```yaml
variables:
  use_af: player.moving.time>=config.angelic_feather_movement_time&buff.angelic_feather.down
  missing_atonement: group.count(cycle.buff.atonement.down&cycle.range<=40)
  surge_of_light_procced: buff.surge_of_light.up
  hold_penance: cooldown.penance.full_recharge_time<2

lists:
  out_of_combat:
    - penance,cycle=members,if=cycle.health.pct<config.OOC_penance_threshold
    - flash_heal,cycle=members,if=cycle.health.pct<config.OOC_flash_heal_threshold
    
  offensive:
    - shadow_word_pain,if=debuff.shadow_word_pain.down
    - penance,if=cooldown.penance.charges=2|buff.power_of_the_dark_side.up
    - mind_blast
    - smite
    
  high_prio:
    - ultimate_penitence,if=group.under_pct_50>=config.ultimate_penitence_members
    - desperate_prayer,if=health.pct<config.desperate_prayer_threshold
    - penance,cycle=members,if=cycle.health.pct<config.MO_penance_threshold&!var.hold_penance
    
  pain_suppression_logic:
    - pain_suppression,cycle=tanks,if=config.pain_suppression_usage!=0&cycle.health.pct<config.pain_suppression_threshold
    - pain_suppression,cycle=healers,if=config.pain_suppression_usage>=2&cycle.health.pct<config.pain_suppression_threshold
    - pain_suppression,cycle=members,if=config.pain_suppression_usage=3&cycle.health.pct<config.pain_suppression_threshold
    
  atonement_spread:
    - evangelism.player,if=var.missing_atonement>1
    - power_word_radiance.player,if=var.missing_atonement>10
    - penance,cycle=members,if=cycle.buff.atonement.down
    - plea,cycle=members,if=cycle.buff.atonement.down
    
  main:
    - return,if=mounted|!rotation_enabled|state.blocked_inputs
    - call_action_list,name=out_of_combat,if=!player.combat
    - angelic_feather.player,if=var.use_af
    - return,if=!player.combat
    - return,if=player.channeling
    - call_action_list,name=pain_suppression_logic
    - call_action_list,name=moving,if=player.moving
    - call_action_list,name=high_prio
    - call_action_list,name=atonement_spread,if=var.missing_atonement>6
    - call_action_list,name=offensive,if=target.valid
```

## Named Actions

Use the `name=` option to give actions descriptive names for debugging:

```yaml
- hammer_of_wrath,name="Hammer of Wrath (ST Opener - 1)",if=var.is_herald
- divine_toll,name="Divine Toll (ST Opener - 2)",if=var.is_templar
```

## Return Statement

Use `return` to stop processing the current list:

```yaml
lists:
  main:
    - return,if=!state.rotation
    - return,if=player.mounted|dead
    - return,if=!player.combat
    - return,if=!target.valid|target.range>10
    
    # Only reaches here if all conditions passed
    - rotation_spell
```

## Shared Lists

Lists can be defined in `_shared.yaml` to be available to all rotations:

```yaml
# In _shared.yaml
lists:
  sanity_checks:
    - return,if=player.dead
    - return,if=!state.rotation
    - return,if=state.blocked_inputs
    
  auto_heal:
    - healthstone,if=health.pct<config.healthstone&healthstone.ready
    - health_potion,if=health.pct<config.healthpotion&health_potion.ready
```

Use in rotations:

```yaml
lists:
  main:
    - call_action_list,name=sanity_checks
    - call_action_list,name=auto_heal
    # ... rest of rotation
```

## Best Practices

1. **Use variables for complex conditions** - Makes code readable
2. **Group related logic into lists** - Easier to maintain
3. **Put sanity checks first** - Early exit conditions
4. **Use descriptive names** - Self-documenting code
5. **Separate concerns** - Cooldowns, defensives, main rotation
6. **Keep lists focused** - Each list should do one thing

## Quick Reference

| Pattern | Purpose |
|---------|---------|
| `var.X: expression` | Define reusable condition |
| `call_action_list,name=X` | Run list, continue |
| `run_action_list,name=X` | Run list, restart |
| `return,if=X` | Stop processing if true |
| `name="Label"` | Debug label for action |

## Next Steps

- See [Configuration Options](Configuration-Options) for user settings
- Check [Advanced Examples](Advanced-Examples) for complete rotation patterns
- Learn about [Cooldown Management](Cooldown-Management) for CD logic
