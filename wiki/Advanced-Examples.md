# Advanced Examples

This page provides complete, real-world examples demonstrating common rotation patterns and techniques.

## Complete Rotation Structure

Every well-organized rotation follows this pattern:

```yaml
version: 1
entry: main

# Spell transformations (talents that replace spells)
morphs:
  spell_that_transforms: replacement_spell

# User-customizable settings
config:
  setting_name:
    label: "Display Name"
    type: slider/checkbox/dropdown/multi_select
    default: value

# Reusable expressions
variables:
  readable_name: complex&expression

# Action lists
lists:
  list_name:
    - spell,if=condition
  main:
    - entry point
```

---

## Pattern: Opening Sequence

Track opener progress and execute a specific sequence:

```yaml
variables:
  opener_complete: combat.time>gcd*7
  
  # Talent builds
  is_templar: talent.lights_guidance
  is_herald: talent.dawnlight
  
  # CD logic
  should_use_cds: state.cds&(target.boss|target.time_to_die>20)

lists:
  st_opener:
    - hammer_of_wrath,name="Step 1",if=var.is_herald
    - divine_toll,name="Step 2",if=var.is_templar&var.should_use_cds
    - execution_sentence,name="Step 3",if=var.should_use_cds
    - final_verdict,name="Step 4",if=var.is_herald
    - wake_of_ashes,name="Step 5",if=var.should_use_cds
    - hammer_of_light,name="Step 6",if=var.is_templar&var.should_use_cds
    - divine_toll,name="Step 7",if=var.is_herald&var.should_use_cds
    
  main:
    # Use opener until complete
    - call_action_list,name=st_opener,if=!var.opener_complete
    
    # Then switch to normal rotation
    - call_action_list,name=st,if=var.opener_complete
```

---

## Pattern: AoE vs Single Target Switching

Dynamically switch between rotations based on enemy count:

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
  st:
    - execution_sentence,if=var.should_use_cds
    - final_verdict,if=holy_power>=5
    - blade_of_justice
    - hammer_of_wrath
    - judgment
    - final_verdict
    
  aoe:
    - execution_sentence,if=var.should_use_cds
    - divine_storm,if=holy_power>=5
    - blade_of_justice
    - hammer_of_wrath
    - judgment
    - divine_storm
    
  main:
    - call_action_list,name=st,if=var.is_st_combat
    - call_action_list,name=aoe,if=var.is_aoe_combat
```

---

## Pattern: Emergency Healing Logic

Priority-based defensive cooldown usage:

```yaml
config:
  defensive_toggles:
    label: "Defensives"
    type: multi_select
    options:
      - label: "Word of Glory"
        value: 1
      - label: "Lay on Hands"
        value: 2
      - label: "Blessing of Protection"
        value: 3
      - label: "Divine Shield"
        value: 4
    default: [0, 1, 2, 3]

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
  use_bop: config.defensive_toggles.has(3)
  use_ds: config.defensive_toggles.has(4)

lists:
  emergency_healing:
    # Smaller cooldowns first (save big CDs for emergencies)
    - word_of_glory,if=var.use_wog&health.pct<=config.wog_usage
    
    # Big cooldowns with Forbearance check
    - lay_on_hands,if=var.use_loh&debuff.forbearance.down&health.pct<=config.loh_usage
    - blessing_of_protection,if=var.use_bop&debuff.forbearance.down&health.pct<=config.bop_usage
    - divine_shield,if=var.use_ds&debuff.forbearance.down&health.pct<=config.ds_usage
    
  main:
    - call_action_list,name=emergency_healing
```

---

## Pattern: Smart Interrupt Priority

Multi-target interrupt logic with configuration:

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
  # Check for important, interruptible cast
  should_interrupt: config.interrupt_target&(target.casting.important|target.channeling.important)&!target.interrupt_immune
  
  should_interrupt_mouse: config.interrupt_mouseover&(mouseover.casting.important|mouseover.channeling.important)&!mouseover.interrupt_immune

lists:
  interrupts:
    # Primary target first
    - rebuke,if=var.should_interrupt
    
    # Mouseover second
    - rebuke.mouseover,if=var.should_interrupt_mouse
    
  main:
    # Check interrupts early (before anything else)
    - call_action_list,name=interrupts
```

---

## Pattern: Healer AoE Cooldown Logic

Use raid cooldowns based on group damage:

```yaml
variables:
  group_members: group.count(1=1)

lists:
  raid_cooldowns:
    # Dungeon: 3+ members below 70%
    - aura_mastery,if=var.group_members=5&group.count(cycle.health.pct<70)>=3
    
    # Raid: 10+ members below 70%
    - aura_mastery,if=var.group_members>5&group.count(cycle.health.pct<70)>=10
    
    # Alternative with shortcuts
    - divine_hymn,if=group.under_pct_50>=5
```

---

## Pattern: Priority Healing by Role

Heal tanks, then healers, then DPS:

```yaml
config:
  tank_threshold:
    label: "Tank Heal HP%"
    type: slider
    default: 60
    
  healer_threshold:
    label: "Healer Heal HP%"
    type: slider
    default: 50
    
  dps_threshold:
    label: "DPS Heal HP%"
    type: slider
    default: 40

lists:
  priority_healing:
    # 1. Emergency heal anyone critical
    - lay_on_hands,cycle=members,if=cycle.health.pct<15
    
    # 2. Strong heal on low tanks
    - flash_heal,cycle=tanks,if=cycle.range<=40&cycle.health.pct<config.tank_threshold
    
    # 3. Heal low healers
    - flash_heal,cycle=healers,if=cycle.range<=40&cycle.health.pct<config.healer_threshold
    
    # 4. Heal low DPS
    - flash_heal,cycle=dps,if=cycle.range<=40&cycle.health.pct<config.dps_threshold
```

---

## Pattern: HoT Maintenance

Apply and maintain HoTs without overwriting:

```yaml
lists:
  hot_maintenance:
    # Apply YOUR Renew if missing on tanks
    - renew,cycle=tanks,if=cycle.range<=40&cycle.buff.renew.down
    
    # Apply YOUR Renew if missing on anyone low
    - renew,cycle=members,if=cycle.range<=40&cycle.buff.renew.down&cycle.health.pct<80
    
    # Refresh YOUR Renew in pandemic window
    - renew,cycle=members,if=cycle.range<=40&cycle.buff.renew.remains<3&cycle.buff.renew.mine
```

---

## Pattern: Atonement Spreading (Discipline Priest)

Smart Atonement application:

```yaml
variables:
  missing_atonement: group.count(cycle.buff.atonement.down&cycle.range<=40)
  surge_of_light_procced: buff.surge_of_light.up

lists:
  atonement_spread:
    # Mass spread when many missing
    - evangelism.player,if=var.missing_atonement>1
    - power_word_radiance.player,if=var.missing_atonement>10
    
    # Individual application
    - penance,cycle=members,if=cycle.range<=40&cycle.buff.atonement.down
    - power_word_shield,cycle=members,if=cycle.range<=40&!cycle.buff.power_word_shield.up&!cycle.buff.atonement.up
    - flash_heal,cycle=members,if=cycle.range<=40&!cycle.buff.atonement.up&var.surge_of_light_procced
    - plea,cycle=members,if=cycle.range<=40&!cycle.buff.atonement.up
    
  main:
    - call_action_list,name=atonement_spread,if=var.missing_atonement>6
```

---

## Pattern: Smart Trinket Usage

Trinket logic with identification and conditions:

```yaml
config:
  trinket_usage:
    label: "Trinket Usage"
    type: dropdown
    options:
      - label: "On Cooldown"
        value: 1
      - label: "With Burst"
        value: 2
      - label: "Disabled"
        value: 3
    default: 2

variables:
  # Identify specific trinkets
  trinket1_is_special: trinket_1.id=242393
  trinket2_is_special: trinket_2.id=242393
  
  # Usage logic
  should_use_trinkets: config.trinket_usage!=3&(config.trinket_usage=1|player.burst.active)

lists:
  trinkets:
    # Generic trinket usage
    - trinket_1,if=trinket_1.ready&var.should_use_trinkets&!var.trinket1_is_special
    - trinket_2,if=trinket_2.ready&var.should_use_trinkets&!var.trinket2_is_special
    
    # Special trinket with custom logic
    - trinket_1,if=var.trinket1_is_special&trinket_1.ready&group.under_pct_50>=3
    - trinket_2,if=var.trinket2_is_special&trinket_2.ready&group.under_pct_50>=3
    
  main:
    - call_action_list,name=trinkets,if=state.cds
```

---

## Pattern: Movement Handling

Special actions while moving:

```yaml
config:
  angelic_feather_time:
    label: "Feather after moving (s)"
    type: slider
    min: 0
    max: 5
    default: 2

variables:
  should_feather: player.moving.time>=config.angelic_feather_time&buff.angelic_feather.down

lists:
  moving:
    # Speed boost
    - angelic_feather.player,if=var.should_feather
    
    # Instant casts only
    - penance,cycle=members,if=cycle.health.pct<70
    - power_word_shield,cycle=members,if=!cycle.buff.power_word_shield.up
    
  main:
    - call_action_list,name=moving,if=player.moving
```

---

## Pattern: Out of Combat Actions

Logic for when not in combat:

```yaml
config:
  auto_res_ooc:
    label: "Auto Resurrect"
    type: checkbox
    default: true
    
  ooc_heal_threshold:
    label: "OOC Heal HP%"
    type: slider
    default: 80

variables:
  dead_members: group.count(cycle.dead)

lists:
  out_of_combat:
    # Resurrection logic
    - resurrection,cycle=members,if=cycle.dead&var.dead_members=1
    - mass_resurrection,if=var.dead_members>1
    
    # Top off health
    - flash_heal,cycle=members,if=cycle.health.pct<config.ooc_heal_threshold
    
  main:
    - return,if=player.mounted
    - call_action_list,name=out_of_combat,if=!player.combat&config.auto_res_ooc
```

---

## Pattern: Mouseover Actions

Direct mouseover targeting:

```yaml
config:
  mo_enabled:
    label: "Enable Mouseover"
    type: checkbox
    default: true
    
  mo_heal_threshold:
    label: "MO Heal HP%"
    type: slider
    default: 60

variables:
  valid_friendly_mo: mouseover.exists&mouseover.alive&mouseover.friendly&mouseover.range<=40
  valid_enemy_mo: mouseover.exists&mouseover.alive&mouseover.enemy

lists:
  mouseover_friendly:
    - pain_suppression.mouseover,if=mouseover.health.pct<20
    - penance.mouseover,if=mouseover.health.pct<config.mo_heal_threshold
    - flash_heal.mouseover,if=mouseover.health.pct<config.mo_heal_threshold
    
  mouseover_enemy:
    - shadow_word_pain.mouseover,if=!mouseover.debuff.shadow_word_pain.up
    
  main:
    - call_action_list,name=mouseover_friendly,if=config.mo_enabled&var.valid_friendly_mo
    - call_action_list,name=mouseover_enemy,if=config.mo_enabled&var.valid_enemy_mo
```

---

## Pattern: Combat Resurrection

Battle res with priority:

```yaml
variables:
  can_battle_res: player.combat&cooldown.intercession.ready
  mo_is_resurrectable: mouseover.friendly&mouseover.dead&mouseover.range<=40

lists:
  battle_res:
    # Mouseover priority
    - intercession.mouseover,if=var.mo_is_resurrectable
    
    # Auto-target if no mouseover
    - intercession,cycle=members,if=cycle.dead
    
  main:
    - call_action_list,name=battle_res,if=var.can_battle_res
```

---

## Complete Example: Main Entry Point

Putting it all together:

```yaml
lists:
  main:
    # ========== SANITY CHECKS ==========
    - return,if=!state.rotation|state.blocked_inputs|player.mounted|dead
    
    # ========== HIGH PRIORITY ==========
    - call_action_list,name=interrupts,if=var.use_interrupts
    
    # ========== OUT OF COMBAT ==========
    - call_action_list,name=out_of_combat,if=!player.combat
    - return,if=!player.combat
    
    # ========== CONSUMABLES ==========
    - healthstone,if=health.pct<config.healthstone&healthstone.ready
    - health_potion,if=health.pct<config.healthpotion&health_potion.ready
    
    # ========== DEFENSIVES ==========
    - call_action_list,name=emergency_healing,if=var.use_defensives
    
    # ========== MOUSEOVER ==========
    - call_action_list,name=mouseover,if=config.mo_enabled&mouseover.exists
    
    # ========== BATTLE RES ==========
    - intercession.mouseover,if=var.mo_is_resurrectable
    
    # ========== TARGET VALIDATION ==========
    - return,if=!target.valid|target.range>10
    
    # ========== COOLDOWNS ==========
    - avenging_wrath,if=!talent.radiant_glory&var.should_use_cds
    - combat_potion,if=buff.avenging_wrath.up&player.inraid&combat_potion.ready
    - trinket_1,if=trinket_1.ready&var.should_use_cds
    - trinket_2,if=trinket_2.ready&var.should_use_cds
    
    # ========== ROTATION ==========
    - call_action_list,name=st_opener,if=var.is_st_combat&!var.opener_complete
    - call_action_list,name=aoe_opener,if=var.is_aoe_combat&!var.opener_complete
    - call_action_list,name=st,if=var.is_st_combat
    - call_action_list,name=aoe,if=var.is_aoe_combat
```

---

## Tips for Writing Good Rotations

1. **Start with sanity checks** - Early `return` statements prevent wasted processing
2. **Use variables** - Complex conditions become readable
3. **Organize into lists** - Logical grouping makes maintenance easier
4. **Name your actions** - Helps with debugging (`name="Step 1"`)
5. **Make it configurable** - Users have different preferences
6. **Test edge cases** - Movement, no target, out of combat, etc.
7. **Check Forbearance** - For Paladin abilities that share the debuff
8. **Validate ranges** - Always check `cycle.range<=40` for heals

---

## See Also

- [Getting Started](Getting-Started) - Basic concepts
- [Rotation Syntax Basics](Rotation-Syntax-Basics) - Detailed syntax reference
- [Healing Targeting](Healing-Targeting) - Group healing patterns
- [Configuration Options](Configuration-Options) - Creating user settings
- [Variables and Action Lists](Variables-and-Action-Lists) - Code organization
