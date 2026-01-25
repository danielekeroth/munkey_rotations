# Feature Request Template

Please use this template when requesting new features or enhancements to help us understand your needs and prioritize development.

## Feature Request Information

### Basic Information
- **Class & Spec**: [REQUIRED] (e.g., Priest - Discipline, Paladin - Protection, or "All Specs")
- **Feature Type**: [REQUIRED] (New Configuration Option, New Ability Support, Rotation Logic Change, Quality of Life, New Specialization)

### Feature Description
**Summary**: [REQUIRED]
```
Brief one-line description of the requested feature
```

**Detailed Description**: [REQUIRED]
```
Provide a comprehensive description of what you want:
- What the feature should do
- How it should work
- When it should activate
- Any specific conditions or requirements
```

**Use Case/Scenario**: [REQUIRED]
```
Explain why this feature is needed:
- What problem does it solve?
- What content/situation would benefit from this?
- How would it improve gameplay experience?
```

### Implementation Details
**Suggested Configuration Options**: [OPTIONAL]
```
If this requires new settings, suggest what they might be:
- Setting Name: Description (Type: slider/checkbox/dropdown)
- Example: "Auto Dispel Threshold: Health % to trigger dispel (Type: slider, 1-100%)"
```

**Integration with Existing Features**: [OPTIONAL]
```
How should this work with current rotation features:
- Should it override existing behavior?
- Should it be a separate toggle?
- Any conflicts with current settings?
```

**Alternative Solutions**: [OPTIONAL]
```
Are there other ways to achieve the same goal?
- Workarounds you've tried
- Similar features in other rotations
- Different approaches to consider
```

### Technical Considerations
**Game Mechanics**: [OPTIONAL]
```
Any relevant game mechanics or limitations:
- Spell interactions
- Cooldown considerations
- Resource management implications
```

**Addon Limitations**: [OPTIONAL]
```
Known limitations that might affect implementation:
- API restrictions
- Targeting limitations
- Timing constraints
```

---

## Example Feature Request

### Basic Information
- **Class & Spec**: Priest - Discipline
- **Feature Type**: New Configuration Option
- **Priority Level**: Medium

### Feature Description
**Summary**: 
```
Add configurable delay for Evangelism to allow for better Atonement spreading
```

**Detailed Description**: 
```
Currently Evangelism casts immediately when multiple party members are missing Atonement.
I would like a configurable delay (0-3 seconds) that waits for more Atonements to be 
applied before casting Evangelism. This would allow for more efficient use of the spell
by spreading more Atonements rather than just extending a few.

The feature should:
- Add a slider for "Evangelism Delay" (0-3000ms)
- Track when Atonements are being applied
- Wait the configured time before casting Evangelism
- Cancel the delay if combat ends or emergency healing is needed
```

**Use Case/Scenario**: 
```
In raid encounters with spread damage, I often apply 2-3 Atonements and then Evangelism
immediately extends them. However, if I could wait 1-2 seconds, I could apply 5-6 
Atonements and then extend all of them, making the spell much more efficient.

This is particularly useful in:
- Raid encounters with predictable AoE damage
- Dungeon pulls where damage ramp-up is gradual
- Any situation where you have time to prepare before damage hits
```

### Implementation Details
**Suggested Configuration Options**: 
```
- Evangelism Delay: Time to wait before casting Evangelism (Type: slider, 0-3000ms, default: 0)
- Cancel Delay on Emergency: Cancel delay if any party member drops below X% (Type: checkbox, default: enabled)
- Emergency Threshold: Health % to cancel delay (Type: slider, 10-50%, default: 30%)
```

**Integration with Existing Features**: 
```
- Should work alongside existing Evangelism logic
- Emergency healing should override the delay
- Should be disabled during movement if movement restrictions apply
- Should respect existing Evangelism conditions (minimum missing Atonements, etc.)
```

**Alternative Solutions**: 
```
- Manual Evangelism toggle (but reduces automation)
- Smart detection based on damage patterns (more complex)
- Integration with boss mod timers (addon dependency)
```

### Technical Considerations
**Game Mechanics**: 
```
- Evangelism has a 30-second cooldown, so timing is crucial
- Atonement duration is limited, so delay can't be too long
- Combat state changes might affect the logic
```

**Addon Limitations**: 
```
- Need to track multiple buff applications over time
- Timer management for the delay system
- Cancellation conditions need to be responsive
```

---

## Additional Examples

### Quality of Life Feature
**Summary**: Add visual indicator for active configuration profile
**Use Case**: When switching between raid/dungeon configs, it's hard to remember which is active

### New Ability Support  
**Summary**: Add support for new trinket "X" with smart usage conditions
**Use Case**: Trinket has unique mechanics that require specific timing not covered by generic trinket logic

### Rotation Logic Change
**Summary**: Modify Shield of the Righteous timing to account for Bulwark of Righteous Fury stacks
**Use Case**: Current logic doesn't optimize for the new talent interaction

### New Specialization
**Summary**: Add support for Holy Paladin
**Use Case**: Complete the Paladin class coverage with healing specialization

---

## Submission Guidelines

1. **Be specific** - Vague requests are harder to implement
2. **Explain the why** - Understanding the problem helps us find the best solution
3. **Consider complexity** - Simple features are more likely to be implemented quickly
4. **Check existing features** - Make sure the functionality doesn't already exist
5. **One request per submission** - Don't combine multiple unrelated features

## Priority Guidelines

- **Critical**: Game-breaking issues or essential missing functionality
- **High**: Significantly improves rotation effectiveness or user experience
- **Medium**: Nice-to-have features that add convenience or minor improvements
- **Low**: Niche features that benefit few users or edge cases

## Development Notes

- Features will be prioritized based on impact, complexity, and available development time
- Some requests may be combined with similar requests from other users
- We may suggest alternative implementations that achieve the same goal more efficiently
- Complex features may be broken down into smaller, incremental improvements

Thank you for helping improve Munkey Rotations!