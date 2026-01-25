# Protection Paladin Rotation (66)
A comprehensive Protection Paladin rotation for tanking with extensive configuration options for survivability and utility.

## Overview
This rotation provides automated threat generation, defensive cooldown management, and utility support for Protection Paladins. It focuses on maintaining aggro, optimal survivability through smart defensive usage, and supporting party members with emergency heals and utility spells.

## KNOWN ISSUES & FIXES
- **Mouseover interrupts not working** - May require macro modification for Avenger's Shield: /cast [@mouseover, exists][@target] Avenger's Shield

## Key Features
- **Smart Defensive Management**: Automated Guardian of Ancient Kings, Ardent Defender, and Divine Shield usage
- **Mouseover Support**: Full mouseover functionality for interrupts, taunts, and emergency heals
- **Holy Power Optimization**: Intelligent Shield of the Righteous timing and holy power management
- **Emergency Healing**: Automated Word of Glory, Lay on Hands, and blessing usage
- **Interrupt Management**: Smart interrupt timing with configurable delays and priority
- **Aura Management**: Automatic aura swapping based on mounted status

## Configuration Options
### Targeting & Combat
- **Auto-target**: Automatically target enemies when none selected
- **Pull with MO**: Allow pulling enemies with mouseover abilities
- **Min/Max range for MO pull**: Range limits for mouseover pulling (10-30 yards)

### Defensive Cooldowns
- **Ardent Defender**: Health percentage to trigger (30-90%, default: 90%)
- **Divine Shield**: Emergency threshold (5-20%, default: 10%)
- **Guardian HP%**: Guardian of Ancient Kings threshold (20-70%, default: 40%)

### Emergency Healing
- **Word of Glory - Self**: Self-heal threshold (10-100%, default: 20%)
- **Word of Glory - Party**: Party heal threshold (10-100%, default: 20%)
- **Only use WG when no defensives**: Restrict Word of Glory usage
- **Buffed WG HP% - Self/Party**: Thresholds when Shining Light is active

### Lay on Hands
- **MO Lay on Hands**: Enable mouseover Lay on Hands
- **MO LOH HP%**: Mouseover threshold (1-100%, default: 20%)
- **Auto LOH - Self/Party**: Automatic usage thresholds (default: 10%)
- **LOH Min. HP%**: Safety threshold for party usage (default: 50%)

### Blessings
- **Blessing of Sacrifice**: Self and party thresholds (default: 90%/40%)
- **Blessing of Protection**: Self and party thresholds (default: 70%/10%)

### Interrupts & Utility
- **MO Interrupt/Stun**: Enable mouseover interrupts and stuns
- **Interrupt delay**: Time before interrupting (100-400ms, default: 200ms)
- **Only Important interrupts**: Filter interrupt targets
- **Blinding Light min casts**: Minimum enemies for AoE interrupt (1-10, default: 2)

### Cooldown Management
- **Hold CDs if TTD below**: Don't use cooldowns if fight ending soon (10-30s, default: 20s)
- **Auto-swap auras**: Automatically manage Crusader/Devotion/Concentration auras
- **MO Res. OOC**: Enable mouseover resurrection out of combat

## Rotation Priority
### High Priority Defensives
1. **Guardian of Ancient Kings** - When below configured threshold
2. **Ardent Defender** - Emergency defensive cooldown
3. **Divine Shield** - Last resort when Ardent Defender down

### Emergency Healing
1. **Shining Light Word of Glory** - Prioritized when buff active
2. **Word of Glory** - Self and party healing based on thresholds
3. **Blessing of Sacrifice** - Redirect damage from low-health allies
4. **Blessing of Protection** - Physical immunity for critical situations
5. **Lay on Hands** - Emergency full heal

### Mouseover Actions
- **Hand of Reckoning** - Taunt enemies targeting party members
- **Avenger's Shield** - Ranged pull and interrupt
- **Divine Toll** - AoE damage and utility
- **Lay on Hands** - Emergency healing
- **Intercession** - Combat resurrection

### Threat Generation
1. **Hammer of Light** - When buff active and at 5 Holy Power
2. **Shield of the Righteous** - Maintain active mitigation
3. **Avenger's Shield** - AoE threat and interrupts
4. **Judgment/Hammer of Wrath** - Holy Power builders
5. **Blessed Hammer** - Consistent threat and debuff maintenance
6. **Consecration** - Ground AoE when stationary

### Interrupt Priority
1. **Blinding Light** - AoE interrupt for multiple casters
2. **Rebuke** - Primary single-target interrupt
3. **Avenger's Shield** - Ranged interrupt option

## Special Features
### Smart Cooldown Usage
- Defensive cooldowns automatically triggered based on health thresholds
- Cooldown holding when fight is ending soon
- Immunity expiration tracking for emergency heals

### Proc Management
- **Shining Light**: Prioritizes Word of Glory usage
- **Hammer of Light**: Optimizes timing with Holy Power generation
- **Bulwark of Righteous Fury**: Enhances Shield of the Righteous timing

### Out-of-Combat Behavior
- Automatic aura management based on mounted status
- Mouseover resurrection for fallen allies
- Emergency healing with configurable thresholds

## Usage Tips
1. **Configure defensive thresholds** based on content difficulty and gear level
2. **Enable mouseover options** for manual override capabilities
3. **Adjust interrupt settings** for encounter-specific needs
4. **Set emergency heal thresholds** based on group composition
5. **Configure blessing usage** for optimal damage mitigation

## Requirements
- Protection Paladin specialization
- Compatible rotation addon/framework
- Proper keybinds for all configured spells

## Version
Version 1 - Latest rotation with comprehensive defensive management and utility support.