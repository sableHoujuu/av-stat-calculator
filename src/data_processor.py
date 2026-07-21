# Handles any necessary data processing that doesn't make sense to be handled inline
import pandas as pd

from src.data_loader import get_unit_passive_data
from src.common_prompts import range_prompt

def process_familiar(familiar_data: pd.Series) -> pd.Series:
    """Handles user input for familiars, and collecting any relevant information."""
    processed_data = pd.Series(data={
        "familiar_id": familiar_data["familiar_id"],
        "familiar_name": familiar_data["familiar_name"],
        "familiar_rarity": familiar_data["familiar_rarity"],
        "familiar_dmg_modifier": 1,
        "familiar_spa_modifier": 1,
        "familiar_rng_modifier": 1,
        "familiar_crit_chance_modifier": 0,
        "familiar_crit_dmg_modifier": 0,
    })

    if familiar_data["familiar_dmg_modifier_min"] != familiar_data["familiar_dmg_modifier_max"]:
        min, max = familiar_data["familiar_dmg_modifier_min"], familiar_data["familiar_dmg_modifier_max"]
        processed_data["familiar_dmg_modifier"] = range_prompt(f"Enter the damage value on the familiar, between {min} and {max}", min, max)
    else:
        processed_data["familiar_dmg_modifier"] = familiar_data["familiar_dmg_modifier_min"]

    if familiar_data["familiar_spa_modifier_min"] != familiar_data["familiar_spa_modifier_max"]:
        max, min = familiar_data["familiar_spa_modifier_min"], familiar_data["familiar_spa_modifier_max"]
        # remember, the spa values are inverse for calculation because spa = attack speed, so
        processed_data["familiar_spa_modifier"] = range_prompt(f"Enter the SPA value on the familiar, between {min} and {max}", min, max)
    else:
        processed_data["familiar_spa_modifier"] = familiar_data["familiar_spa_modifier_min"]

    if familiar_data["familiar_rng_modifier_min"] != familiar_data["familiar_rng_modifier_max"]:
        min, max = familiar_data["familiar_rng_modifier_min"], familiar_data["familiar_rng_modifier_max"]
        processed_data["familiar_rng_modifier"] = range_prompt(f"Enter the range value on the familiar, between {min} and {max}", min, max)
    else:
        processed_data["familiar_rng_modifier"] = familiar_data["familiar_rng_modifier_min"]

    if familiar_data["familiar_crit_chance_modifier_min"] != familiar_data["familiar_crit_chance_modifier_max"]:
        min, max = familiar_data["familiar_crit_chance_modifier_min"], familiar_data["familiar_crit_chance_modifier_max"]
        processed_data["familiar_crit_chance_modifier"] = range_prompt(f"Enter the crit chance value on the familiar, between {min} and {max}", min, max)
    else:
        processed_data["familiar_crit_chance_modifier"] = familiar_data["familiar_crit_chance_modifier_min"]

    if familiar_data["familiar_crit_dmg_modifier_min"] != familiar_data["familiar_crit_dmg_modifier_max"]:
        min, max = familiar_data["familiar_crit_dmg_modifier_min"], familiar_data["familiar_crit_dmg_modifier_max"]
        processed_data["familiar_crit_dmg_modifier"] = range_prompt(f"Enter the crit damage value on the familiar, between {min} and {max}", min, max)
    else:
        processed_data["familiar_crit_dmg_modifier"] = familiar_data["familiar_crit_dmg_modifier_min"]

    return processed_data
