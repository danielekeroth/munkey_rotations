# SimC Spell Morph Database Builder

A Python tool to automatically extract spell morphs (transformations) from SimC (SimulationCraft) spell data dumps.

## What are Spell Morphs?

Spell morphs occur when one spell temporarily transforms into another, usually via a buff or talent. For example:
- **Azure Strike** → **Azure Sweep** (after using Eternity Surge with certain talents)
- **Death and Decay** → **Death's Due** (with specific talents)
- **Frost Strike** → **Frostbane** (with certain buffs)

In rotation YAML files, these are handled using the `override` option:
```yaml
- azure_sweep,override=azure_strike,if=buff.azure_sweep.up
```

## Installation

No installation required! Just Python 3.7+ with standard library.

## Usage

### Process a single class:
```bash
python build_morph_database.py --class evoker
```

### Process all classes:
```bash
python build_morph_database.py --all
```

### Generate combined database:
```bash
python build_morph_database.py --all --combined
```

### Output options:
```bash
# Individual files in YAML format (default)
python build_morph_database.py --all --format yaml

# Individual files in Markdown format
python build_morph_database.py --all --format markdown

# Combined database in JSON
python build_morph_database.py --all --combined --combined-format json

# Custom output directory
python build_morph_database.py --all --output ./my_morphs
```

## Output Files

### Individual Class Files
For each class, generates `{class}_morphs.yaml`:
```yaml
evoker:
  # Azure Sweep overrides Azure Strike
  - override_spell: Azure Sweep
    override_id: 1265871
    base_spell: Azure Strike
    base_id: 362969
    trigger: buff.azure_sweep.up
    usage: "Azure Sweep,override=Azure Strike,if=buff.azure_sweep.up"
```

### Combined Database
`all_morphs.yaml` contains all classes in one file:
```yaml
# Combined Spell Morph Database
# Total morphs: 111

deathknight:
  - override: Death's Due
    base: Death and Decay
    trigger: buff.death's_due.up
    usage: Death's Due,override=Death and Decay,if=buff.death's_due.up
  ...

evoker:
  - override: Azure Sweep
    base: Azure Strike
    trigger: buff.azure_sweep.up
    usage: Azure Sweep,override=Azure Strike,if=buff.azure_sweep.up
  ...
```

## Sample Results

| Class | Morphs Found | Example |
|-------|-------------|---------|
| Death Knight | 15 | Death's Due → Death and Decay |
| Demon Hunter | 16 | Various talent transforms |
| Druid | 6 | Form/ability changes |
| Evoker | 1 | Azure Sweep → Azure Strike |
| Hunter | 19 | Various talent transforms |
| Mage | 3 | Spell modifications |
| Monk | 2 | Ability transforms |
| Paladin | 15 | Various talent transforms |
| Priest | 9 | Spell modifications |
| Rogue | 2 | Ability transforms |
| Shaman | 8 | Totem/ability changes |
| Warlock | 7 | Demon/spell transforms |
| Warrior | 8 | Stance/ability changes |

## Using the Database in Rotations

When writing a rotation, check the morph database for your class:

1. Look up your class in `morph_database/{class}_morphs.yaml`
2. If a spell morph exists, use the `override` syntax:

```yaml
# Instead of checking the base spell directly:
- azure_strike,if=buff.azure_sweep.down  # ❌ Wrong

# Check the morphed spell with override:
- azure_sweep,override=azure_strike,if=buff.azure_sweep.up  # ✅ Correct
```

## How It Works

1. Downloads spell data from SimC's GitHub repository
2. Parses each spell's "Effects" section
3. Looks for "Override Action Spell" effects
4. Extracts the override relationship (Spell A overrides Spell B)
5. Filters out self-overrides (where spell overrides itself)
6. Generates YAML/Markdown documentation

## Data Source

All data comes from the official SimC spell data dumps:
- URL: `https://raw.githubusercontent.com/simulationcraft/simc/refs/heads/midnight/SpellDataDump/`
- Files: `{class}.txt` for each class

## Updating the Database

To get the latest morphs after a WoW patch:
```bash
python build_morph_database.py --all --combined
```

This re-downloads fresh data from SimC and regenerates all files.

## Integration with QUICK_REFERENCE.yaml

The morph database complements the quick reference:
- **QUICK_REFERENCE.yaml**: General syntax and patterns
- **morph_database/**: Class-specific spell transformations

When creating rotations, check both:
1. Quick reference for syntax
2. Morph database for spell transformations your class might have

## Troubleshooting

### No morphs found for a class
Some classes have few or no spell morphs. This is normal - not all classes use the override mechanic extensively.

### Spell IDs shown instead of names
Some morphs reference internal/unused spells that don't have proper names. These are filtered out when possible, but some may remain. Focus on the named spells for rotation writing.

### Download errors
If SimC's repository is unavailable, the tool will report the error. Try again later or download the files manually from:
https://github.com/simulationcraft/simc/tree/midnight/SpellDataDump
