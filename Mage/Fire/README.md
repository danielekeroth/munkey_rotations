# Fire Mage Rotation (63)
A high-performance Fire Mage rotation for The War Within (11.0.7), featuring advanced Sun King's Blessing management, Combustion optimization, and Frostfire Hero Talent support.

## Overview
This rotation is designed to maximize Ignite damage and Combustion uptime. it handles the complex interaction between Hot Streak, Heating Up, and Sun King's Blessing stacks to ensure you always have a big Pyroblast ready for your burst windows.

## Key Features
- **Combustion Management**: Automated Combustion usage with TTD safety checks.
- **Sun King's Blessing (SKB)**: Intelligent tracking of SKB stacks (10) and automated hardcasting of Pyroblast/Flamestrike to trigger mini-Combustions.
- **Frostfire Support**: Automatic detection and usage of Frostfire Empowerment and Flash Freeze procs.
- **Smart Cleave**: Flawless transition between single-target and Flamestrike-based AoE based on enemy count.
- **Defensive Suite**: Automated Ice Barrier, Mirror Image, and emergency Ice Block usage.
- **Movement Friendly**: Seamlessly switches to Scorch when moving and out of instant procs.

## Configuration Options
### Cooldown Management
- **Use Combustion**: Enable/Disable automated Combustion usage.
- **Hold Combustion if TTD Below**: Prevents wasting major cooldowns on dying mobs (default: 15s).

### Defensives
- **Ice Barrier HP%**: Maintain shield when below threshold (default: 80%).
- **Mirror Image HP%**: Use for damage reduction when dropping low (default: 40%).
- **Ice Block HP%**: Emergency survival trigger (default: 15%).

### Utility
- **Auto-Arcane Intellect**: Automatically keeps the Intellect buff active on yourself and party.

## Rotation Priority
### Single-Target
1. **Sun King's Blessing Hardcast**: When at 10 stacks, hardcasts Pyroblast to trigger Combustion.
2. **Instant Pyroblast**: Spends Hot Streak procs immediately.
3. **Meteor**: Cast on cooldown within burst windows.
4. **Pyroclasm**: High-damage hardcast Pyroblasts when procced.
5. **Fire Blast / Phoenix Flames**: Used to convert "Heating Up" into "Hot Streak".
6. **Frostfire Bolt / Scorch**: Proc-based instant casts or movement fillers.
7. **Fireball**: Primary filler.

### Multi-Target (3+ Enemies)
1. **Flamestrike**: Replaces Pyroblast as the primary Hot Streak spender.
2. **Living Bomb**: Applied to targets when talented.
3. **Meteor**: Massive AoE burst damage.

### Combustion Phase
During Combustion, the rotation shifts to rapid fire:
1. **Pyroblast** (Instant)
2. **Fire Blast** (To generate new Hot Streaks)
3. **Phoenix Flames** (When Fire Blast is on cooldown)

## Requirements
- Fire Mage specialization (Level 70+)
- **Sun King's Blessing** talent (Highly Recommended)
- **Frostfire** or **Sunfury** Hero Talents (Supported)

## Version
Version 1.0 - Optimized for TWW 11.0.7.
