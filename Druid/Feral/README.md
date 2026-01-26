# Druid Feral Rotation v103

A comprehensive World of Warcraft rotation for Feral Druids optimized for both single-target and AoE scenarios. This rotation provides intelligent resource management, cooldown synchronization, and extensive customization options for optimal gameplay.

## Features

### Core Functionality
- **Optimized Stealth Opener**: Complete opener sequence from stealth with proper ability timing
- **Resource Management**: Intelligent Energy and Combo Point usage with overflow handling
- **DoT Management**: Automatic Rake and Rip maintenance with pandemic timing
- **Cooldown Synchronization**: Coordinated usage of Berserk, Tiger's Fury, and Convoke the Spirits
- **Target Detection**: Automatic switching between single-target and AoE priorities

### Advanced Features
- **Hero Talent Support**: Full integration with Druid of the Claw talent tree
- **Proc Management**: Automatic handling of Apex Predator's Craving, Sudden Ambush, and Ravage procs
- **Talent Adaptation**: Dynamic behavior based on talent selections (Incarnation, Coiled to Spring)
- **Multi-target DoT Maintenance**: Intelligent target switching for optimal DoT coverage
- **Defensive Integration**: Automatic defensive ability usage based on health thresholds

## Configuration Options

### Resource Management
- **Energy Dump Threshold**: Percentage threshold for energy dumping before Tiger's Fury (70-95%, default: 80%)
- **Tiger's Fury Prep Time**: Time window for energy preparation before Tiger's Fury (1-5s, default: 3s)
- **Energy Cap Threshold**: Emergency energy dump threshold to prevent waste (85-100%, default: 95%)

### DoT Management
- **Pandemic Threshold**: Global pandemic refresh timing (0.2-0.4, default: 0.3)
- **Rake Pandemic Threshold**: Specific Rake refresh timing (0.2-0.4, default: 0.3)
- **Rip Pandemic Threshold**: Specific Rip refresh timing (0.2-0.4, default: 0.3)

### Target Detection
- **AoE Enemy Threshold**: Number of enemies to trigger AoE rotation (2-5, default: 3)
- **Target Switching Enabled**: Allow automatic target switching for optimal DPS
- **Target Switch Range**: Maximum range for target switching (5-15 yards, default: 8)

### Cooldown Management
- **Sync Major Cooldowns**: Synchronize Berserk, Tiger's Fury, and Convoke usage
- **Hold CDs for Sync**: Hold cooldowns to synchronize with other major CDs
- **Convoke Sync Window**: Time window for Convoke synchronization (5-15s, default: 10s)

### Opener Configuration
- **Use Stealth Opener**: Execute optimized opener sequence from stealth
- **Strict Opener Sequence**: Follow exact opener sequence or allow flexibility
- **Opener Flexibility Window**: Time window for flexible opener execution (3-10s, default: 5s)

### Proc Management
- **Apex Predator Priority**: Prioritize Ferocious Bite when Apex Predator's Craving procs
- **Sudden Ambush Priority**: Prioritize Shred when Sudden Ambush procs with active Rake
- **Ravage Proc Priority**: Prioritize Ravage procs for Druid of the Claw builds

### Defensive & Utility
- **Auto Interrupts**: Automatically interrupt important enemy casts
- **Only Important Interrupts**: Only interrupt spells marked as important
- **Interrupt Delay**: Delay before interrupting to avoid wasting interrupts (100-500ms, default: 200ms)

## Rotation Priority

### Stealth Opener Sequence
1. **Rake** - Apply from stealth for enhanced damage
2. **Swipe** - Generate 5 Combo Points
3. **Berserk + Tiger's Fury** - Activate major cooldowns simultaneously
4. **Primal Wrath** - Apply Rip to all enemies
5. **Convoke the Spirits** - Channel for massive damage
6. **Ferocious Bite** - Spend combo points
7. **Feral Frenzy** - Complete opener sequence
8. **Berserk Window** - Alternate between Ferocious Bite and Swipe

### Single-Target Priority
1. **Apex Predator's Craving** - Immediate Ferocious Bite when proc is active
2. **Ravage Procs** - High priority for Druid of the Claw builds
3. **Rip Management** - Apply/refresh when missing or in pandemic with 5 CP
4. **Rake Management** - Apply/refresh when missing or in pandemic
5. **Ferocious Bite** - At 5 combo points with active DoTs
6. **Sudden Ambush** - Prioritize Shred when proc is active with Rake
7. **Shred** - Default combo point generator

### AoE Priority
1. **Apex Predator's Craving** - Immediate Ferocious Bite when proc is active
2. **Ravage Procs** - High priority for Druid of the Claw builds
3. **Primal Wrath** - Apply/refresh Rip on multiple targets
4. **Ferocious Bite** - At 5 combo points with active Rip
5. **Rake** - Apply to primary target when missing/pandemic
6. **Swipe** - Primary combo point generator for AoE

### Cooldown Management
- **Major Cooldown Sync**: Berserk + Tiger's Fury + Convoke when all available
- **Energy Dump Timing**: Dump energy before Tiger's Fury comes off cooldown
- **Independent Usage**: Feral Frenzy and Tiger's Fury on cooldown when not syncing
- **Convoke Optimization**: Use within major cooldown windows for maximum benefit

## Talent Integration

### Incarnation: Avatar of Ashamane
- Replaces Berserk mechanics when talented
- Enhanced Prowl usage during Incarnation windows
- Extended duration and energy cost reduction

### Druid of the Claw
- **Ravage Proc Priority**: Automatic prioritization of Ravage procs
- **Proc Preservation**: Uses Ferocious Bite to prevent Ravage munching
- **Claw Rampage Synergy**: Enhanced Ravage generation during Berserk windows
- **Stack Management**: Optimal usage of multiple Ravage stacks

### Coiled to Spring
- **Overflow Handling**: Manages combo points above 5 during Berserk
- **Storage Optimization**: Efficient usage of stored combo points
- **Synergy Benefits**: Enhanced combo point efficiency during cooldown windows

## Advanced Features

### Multi-Target DoT Maintenance
- **Intelligent Target Switching**: Automatically switches targets to maintain DoTs
- **Priority Target Focus**: Focuses on elite/rare/boss targets when available
- **DoT Spread Optimization**: Efficiently spreads DoTs across multiple enemies
- **Coverage Assessment**: Monitors DoT coverage and adjusts priorities

### Defensive Integration
- **Health-Based Triggers**: Automatic defensive usage based on health thresholds
- **Damage Prediction**: Proactive defensive usage before predictable damage
- **Ability Stacking**: Intelligent combination of defensive abilities
- **Emergency Response**: Immediate response to critical health situations

### Utility Management
- **Smart Interrupts**: Interrupts important casts with proper timing
- **Crowd Control**: Uses utility spells when interrupts are unavailable
- **Enrage Removal**: Automatically removes dangerous enrage effects
- **Beast Control**: Specialized crowd control for beast-type enemies

## Performance Optimization

### Efficient Condition Evaluation
- **Variable Caching**: Complex calculations cached for performance
- **Priority Ordering**: Frequently-used conditions evaluated first
- **Redundancy Elimination**: Minimized duplicate condition checks
- **Resource Validation**: Efficient energy and combo point availability checks

### Action List Organization
- **Hierarchical Structure**: Logical organization of action priorities
- **Modular Design**: Separate action lists for different scenarios
- **Conditional Execution**: Action lists only execute when conditions are met
- **Fallback Systems**: Comprehensive fallback actions for edge cases

## Usage Tips

### Getting Started
1. Import the rotation into your rotation addon
2. Configure basic settings (energy thresholds, AoE enemy count)
3. Test the stealth opener in a safe environment
4. Adjust pandemic thresholds based on your latency

### Optimization
- **Energy Management**: Monitor energy waste and adjust dump thresholds
- **Cooldown Timing**: Practice cooldown synchronization for maximum burst
- **Target Switching**: Enable target switching for multi-target encounters
- **Proc Awareness**: Learn to recognize and utilize proc opportunities

### Troubleshooting
- **Low DPS**: Check energy dump settings and cooldown synchronization
- **Resource Waste**: Adjust energy and combo point thresholds
- **DoT Uptime**: Verify pandemic thresholds and target switching settings
- **Opener Issues**: Ensure stealth opener is enabled and properly configured

## Version History

### v103 - Current
- Complete rotation implementation with all core features
- Full hero talent integration (Druid of the Claw)
- Advanced multi-target DoT maintenance
- Comprehensive defensive and utility integration
- Extensive configuration options
- Performance optimizations

## Support

For issues, suggestions, or contributions, please refer to the main rotation library documentation and community resources.

## Requirements
- Feral Druid specialization
- Basic understanding of Feral Druid mechanics

---

*This rotation is designed for optimal performance across all content types including raids, dungeons, and solo play. Regular updates ensure compatibility with game changes and balance adjustments.*