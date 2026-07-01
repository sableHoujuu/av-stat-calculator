# Anime Vanguards Stat Calculator
This project seeks to provide an easily updatable and robust stat calculator for the Roblox game Anime Vanguards.

## Features (unimplemented unless stated otherwise)
- Calculates stats and estimated DPS based on unit, trait, familiar, and memoria data
- Reads relevant data from CSV files, for easy modification
- Accepts user input for selection of unit, trait, buffs, etc.
- Supports crit damage calculation and takes DoT into account
- Properly supports unit passives

## Requirements
- Python 3.13 or greater
- uv 0.9.20 or greater (dependency management)

## Setup
1. Clone the repository
2. Install dependencies by running `uv sync` in project root (av-stat-calculator)
3. uv run main.py to ensure it is installed correctly

## Usage
```uv run main.py [unit-name]```

To see a list of flags and optional commands, use ```uv run main.py --help```

## Data
TBD

## Formulas Used
For Memoria stats: Base Stats x Level x Stat Degree x Trait Multiplier

For Unit damage: (Base Damage x Familiar Stats + Memoria Stats) x Unit Level x Unit Trait x Unit Stat Degree

For Crits: (Unit Damage * Crit Damage Modifier * Crit Chance) + (Unit Damage * (1 - Crit Chance))

For DoTs: They are calculated the same as above damage, based on the percentage and time (ex. 50% bleed over 8 seconds.)

For Level modifier: 3.9442, derived from official sources (difference between level 1 and 60)
