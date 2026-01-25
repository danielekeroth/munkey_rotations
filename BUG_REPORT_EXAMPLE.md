# Bug Report Template
Please use this template when reporting bugs to help us identify and resolve issues quickly. Fill out all required fields and as many optional fields as possible.

## Bug Report Information
### Character Information
- **Class & Spec**: [REQUIRED] (e.g., Priest - Discipline, Paladin - Protection)
- **Character Level**: [OPTIONAL] (Only if not max level - e.g., Level 65)
- **Talent Loadout**: [PREFERABLY] 
  ```
  Paste your talent loadout string here or describe key talents:
  - Row 15: Talent Name
  - Row 30: Talent Name
  - etc.
  ```

### Technical Information
- **Addon Version**: [REQUIRED] (e.g., Rotation Helper v2.1.3, GSE v3.0.45)
- **Keyboard Layout**: [OPTIONAL] (e.g., QWERTY US, AZERTY FR, QWERTZ DE)
- **Game Version**: [OPTIONAL] (e.g., 10.2.5, 11.0.2)

### Issue Description
**Description of the issue**: [REQUIRED]
```
Provide a clear and detailed description of what's happening:
- What you expected to happen
- What actually happened
- When the issue occurs (always, sometimes, specific conditions)
- Any error messages you see
```

**Steps to Reproduce**: [PREFERABLY]
1. Step one
2. Step two
3. Step three
4. Issue occurs

**Configuration Settings**: [OPTIONAL]
```
If relevant, list any custom configuration settings you've changed:
- Setting Name: Value
- Another Setting: Value
```

### Media Evidence
**Screenshots/Video**: [PREFERABLY]
- Please attach screenshots or video demonstrating the issue
- **IMPORTANT**: Censor all character names, guild names, and server names for privacy
- Use tools like paint, snipping tool, or video editing software to blur/black out names

### Log Files
**Loader Log Files**: [OPTIONAL]
```
If you have access to addon log files, paste relevant sections here:
- Error logs
- Debug output
- Console messages
```

---

## Example Bug Report
### Character Information
- **Class & Spec**: Priest - Discipline
- **Character Level**: Max Level (80)
- **Talent Loadout**: 
  ```
  Oracle build with:
  - Weal and Woe
  - Ultimate Penitence
  - Evangelism
  - Pain Suppression
  ```

### Technical Information
- **Addon Version**: GSE v3.0.45
- **Keyboard Layout**: QWERTY US
- **Game Version**: 11.0.2

### Issue Description
**Description of the issue**: 
```
Pain Suppression is being cast on myself instead of the mouseover target when using 
mouseover functionality. This happens consistently when I have a mouseover target 
selected and the MO Pain Suppression option is enabled in the configuration.

Expected: Pain Suppression should cast on mouseover target
Actual: Pain Suppression casts on myself regardless of mouseover target
Occurs: Every time I try to use mouseover Pain Suppression
```

**Steps to Reproduce**:
1. Enable "MO Pain Suppression" in rotation settings
2. Set Pain Suppression threshold to 40%
3. Mouseover a party member below 40% health
4. Rotation attempts to cast Pain Suppression
5. Spell casts on self instead of mouseover target

**Configuration Settings**:
```
- MO Pain Suppression: Enabled
- Pain Suppression Threshold: 40%
- Pain Suppression Usage: Everyone
```

### Media Evidence
**Screenshots/Video**: 
- Screenshot showing mouseover target at 35% health
- Screenshot showing Pain Suppression buff on myself instead of target
- (Names censored with black bars)

### Log Files
**Loader Log Files**:
```
[12:34:56] Attempting to cast Pain Suppression on mouseover target
[12:34:56] ERROR: Mouseover target not found, defaulting to self
[12:34:56] Pain Suppression cast on player
```

---

## Submission Guidelines
1. **One issue per report** - Don't combine multiple unrelated bugs
2. **Search existing reports** - Check if the issue has already been reported
3. **Be specific** - Vague descriptions make bugs harder to fix
4. **Test thoroughly** - Try to reproduce the issue multiple times
5. **Update if needed** - Add more information if requested

## Privacy Notice
- Always censor character names, guild names, and server names in screenshots/videos
- Don't include personal information in log files
- We may ask for additional information to help resolve the issue

Thank you for helping improve Munkey Rotations!