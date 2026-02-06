#!/usr/bin/env python3
"""
SimC Spell Morph Database Builder

Downloads SimC spell data dumps and extracts spell morphs (overrides).
Builds a local database of which spells transform into other spells.

Usage:
    python build_morph_database.py --class evoker
    python build_morph_database.py --all
    python build_morph_database.py --class evoker --output morphs.yaml
    python build_morph_database.py --all --combined
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime

# SimC base URL for spell data dumps
SIMC_BASE_URL = "https://raw.githubusercontent.com/simulationcraft/simc/refs/heads/midnight/SpellDataDump"

# All playable classes in WoW
CLASSES = [
    "deathknight", "demonhunter", "druid", "evoker",
    "hunter", "mage", "monk", "paladin",
    "priest", "rogue", "shaman", "warlock", "warrior"
]


def download_spell_dump(class_name: str) -> str:
    """Download spell data dump for a class."""
    url = f"{SIMC_BASE_URL}/{class_name}.txt"
    print(f"Downloading {url}...")
    
    try:
        with urlopen(url) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        print(f"Error downloading {class_name}: {e}", file=sys.stderr)
        return ""


def parse_spell_morphs(content: str) -> list[dict]:
    """
    Parse spell dump content and extract morphs.
    
    Looks for patterns like:
    "Override Action Spell (Misc w/ Base) (332): Azure Sweep overrides Azure Strike"
    """
    morphs = []
    current_spell = None
    current_spell_id = None
    in_effects_section = False
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Track if we're in the Effects section
        if line.startswith('Effects'):
            in_effects_section = True
        elif line.startswith('Description') or line.startswith('Name'):
            in_effects_section = False
        
        # Start of a new spell entry
        if line.startswith('Name') and 'id=' in line:
            match = re.search(r'Name\s+:\s+(.+?)\s+\(id=(\d+)\)', line)
            if match:
                current_spell = match.group(1).strip()
                current_spell_id = int(match.group(2))
            in_effects_section = False
        
        # Look for override effect - need both "Override Action Spell" and "overrides"
        if 'Override Action Spell' in line and 'overrides' in line:
            # Extract the override description
            override_match = re.search(
                r'Override Action Spell.*?:\s+(.+?)\s+overrides\s+(.+?)(?:\s*\||\s*$)',
                line
            )
            
            if override_match and current_spell:
                override_spell = override_match.group(1).strip()
                base_spell = override_match.group(2).strip()
                
                # Skip self-overrides (usually not meaningful morphs)
                if override_spell == base_spell:
                    continue
                
                # Extract base spell ID from Misc Value in current or next lines
                base_spell_id = None
                
                # Look in current line first
                misc_match = re.search(r'Misc Value:\s*(\d+)', line)
                if misc_match:
                    base_spell_id = int(misc_match.group(1))
                else:
                    # Check next few lines for Misc Value
                    for j in range(i + 1, min(i + 3, len(lines))):
                        misc_match = re.search(r'Misc Value:\s*(\d+)', lines[j])
                        if misc_match:
                            base_spell_id = int(misc_match.group(1))
                            break
                
                # Determine trigger condition based on context
                trigger_buff = guess_trigger_buff(override_spell, current_spell)
                
                morphs.append({
                    'override_spell': override_spell,
                    'override_spell_id': current_spell_id,
                    'base_spell': base_spell,
                    'base_spell_id': base_spell_id,
                    'trigger_buff': trigger_buff,
                    'rotation_usage': f"{override_spell},override={base_spell},if=buff.{trigger_buff}.up"
                })
    
    return morphs


def guess_trigger_buff(override_spell: str, aura_name: str) -> str:
    """
    Guess the buff name that triggers the morph.
    Usually it's the override spell name or the aura name.
    """
    # Common patterns:
    # Azure Sweep is triggered by buff.azure_sweep.up
    # Usually the buff name matches the override spell name
    return override_spell.lower().replace(' ', '_')


def output_yaml(morphs: list[dict], class_name: str) -> str:
    """Generate YAML output for morphs."""
    lines = []
    lines.append(f"# {class_name.title()} Spell Morphs")
    lines.append(f"# Auto-generated from SimC spell data dump")
    lines.append(f"# Source: {SIMC_BASE_URL}/{class_name}.txt")
    lines.append(f"# Generated: {datetime.now().isoformat()}")
    lines.append("")
    lines.append(f"{class_name}:")
    
    if not morphs:
        lines.append("  # No spell morphs found")
        return '\n'.join(lines)
    
    for morph in morphs:
        lines.append(f"  # {morph['override_spell']} overrides {morph['base_spell']}")
        lines.append(f"  - override_spell: {morph['override_spell']}")
        lines.append(f"    override_id: {morph['override_spell_id']}")
        lines.append(f"    base_spell: {morph['base_spell']}")
        if morph['base_spell_id']:
            lines.append(f"    base_id: {morph['base_spell_id']}")
        lines.append(f"    trigger: buff.{morph['trigger_buff']}.up")
        lines.append(f"    usage: \"{morph['rotation_usage']}\"")
        lines.append("")
    
    return '\n'.join(lines)


def output_markdown(morphs: list[dict], class_name: str) -> str:
    """Generate Markdown documentation for morphs."""
    lines = []
    lines.append(f"# {class_name.title()} Spell Morphs")
    lines.append("")
    lines.append(f"Source: [SimC Spell Data Dump]({SIMC_BASE_URL}/{class_name}.txt)")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("")
    
    if not morphs:
        lines.append("No spell morphs found for this class.")
        return '\n'.join(lines)
    
    lines.append("| Override Spell | Base Spell | Buff Trigger | Rotation Usage |")
    lines.append("|----------------|------------|--------------|----------------|")
    
    for morph in morphs:
        usage = f"`{morph['rotation_usage']}`"
        trigger = f"`buff.{morph['trigger_buff']}.up`"
        lines.append(f"| {morph['override_spell']} | {morph['base_spell']} | {trigger} | {usage} |")
    
    return '\n'.join(lines)


def output_combined_json(all_morphs: dict[str, list[dict]], output_path: Path) -> None:
    """Generate a combined JSON database of all morphs."""
    database = {
        "meta": {
            "source": SIMC_BASE_URL,
            "generated": datetime.now().isoformat(),
            "classes_processed": list(all_morphs.keys()),
            "total_morphs": sum(len(m) for m in all_morphs.values())
        },
        "morphs": all_morphs
    }
    
    output_path.write_text(json.dumps(database, indent=2))
    print(f"Combined database saved to {output_path}")


def output_combined_yaml(all_morphs: dict[str, list[dict]], output_path: Path) -> None:
    """Generate a combined YAML database of all morphs."""
    lines = []
    lines.append("# Combined Spell Morph Database")
    lines.append(f"# Source: {SIMC_BASE_URL}")
    lines.append(f"# Generated: {datetime.now().isoformat()}")
    lines.append(f"# Classes: {', '.join(all_morphs.keys())}")
    lines.append(f"# Total morphs: {sum(len(m) for m in all_morphs.values())}")
    lines.append("")
    
    for class_name, morphs in all_morphs.items():
        lines.append(f"{class_name}:")
        if not morphs:
            lines.append("  []  # No morphs")
        else:
            for morph in morphs:
                lines.append(f"  - override: {morph['override_spell']}")
                lines.append(f"    base: {morph['base_spell']}")
                lines.append(f"    trigger: buff.{morph['trigger_buff']}.up")
                lines.append(f"    usage: {morph['rotation_usage']}")
        lines.append("")
    
    output_path.write_text('\n'.join(lines))
    print(f"Combined database saved to {output_path}")


def process_class(class_name: str, output_dir: Path, format: str = "yaml") -> list[dict]:
    """Process a single class and save output. Returns the morphs found."""
    content = download_spell_dump(class_name)
    if not content:
        return []
    
    print(f"Parsing {class_name}...")
    morphs = parse_spell_morphs(content)
    print(f"Found {len(morphs)} morphs for {class_name}")
    
    if format == "yaml":
        output = output_yaml(morphs, class_name)
        ext = "yaml"
    else:
        output = output_markdown(morphs, class_name)
        ext = "md"
    
    output_path = output_dir / f"{class_name}_morphs.{ext}"
    output_path.write_text(output)
    print(f"Saved to {output_path}")
    
    return morphs


def main():
    parser = argparse.ArgumentParser(
        description="Build spell morph database from SimC data dumps"
    )
    parser.add_argument(
        "--class", "-c",
        dest="class_name",
        help="Specific class to process (e.g., evoker, warrior)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Process all classes"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("morph_database"),
        help="Output directory (default: morph_database)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["yaml", "markdown"],
        default="yaml",
        help="Output format for individual files"
    )
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Also generate a combined database file"
    )
    parser.add_argument(
        "--combined-format",
        choices=["yaml", "json"],
        default="yaml",
        help="Format for combined database"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output.mkdir(exist_ok=True)
    
    if args.all:
        print("Processing all classes...")
        all_morphs = {}
        
        for class_name in CLASSES:
            morphs = process_class(class_name, args.output, args.format)
            all_morphs[class_name] = morphs
            print()
        
        if args.combined:
            if args.combined_format == "json":
                combined_path = args.output / "all_morphs.json"
                output_combined_json(all_morphs, combined_path)
            else:
                combined_path = args.output / "all_morphs.yaml"
                output_combined_yaml(all_morphs, combined_path)
                
    elif args.class_name:
        process_class(args.class_name, args.output, args.format)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
