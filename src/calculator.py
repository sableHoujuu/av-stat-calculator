# All functions and classes related to calculating things and packaging the data.
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.trait_manager import UnitTrait, get_unit_trait_stats


@dataclass
class FinalUnitData:
    unit_id: int
    name: str
    damage: float
    spa: float
    range: float
    level: int
    trait: UnitTrait | None
    attack_degree: float
    spa_degree: float
    range_degree: float
    memoria: None  # not implemented
    familiar: None  # not implemented
    expected_dps: float

    def __str__(self):
        return f"Unit Name: {self.name}\nDamage: {self.damage}"


def calculate_unit_stats(gathered_unit_data: pd.Series) -> FinalUnitData:
    """Given a properly formatted input Series from pandas, and memoria or familiars, reads all relevant information and preforms all of the necessary calculations for final stats and DPS."""
    familiar_placeholder = 1  # replace with familiar stats
    memoria_placeholder = 0  # replace with memoria stats
    trait_stats = get_unit_trait_stats(UnitTrait(gathered_unit_data["unit_trait"]))
    unit_damage = (
        (gathered_unit_data["unit_damage"] * familiar_placeholder + memoria_placeholder)
        * (3.9442064 * (gathered_unit_data["unit_level"] / 60))
        * trait_stats.dmg
        * (gathered_unit_data["unit_atk_degree"] / 100 + 1)
    )
    return unit_damage
    # final_unit_data = FinalUnitData()
    # return final_unit_data
