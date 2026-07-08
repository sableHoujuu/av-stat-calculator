# All functions and classes related to calculating things and packaging the data.
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.trait_manager import TraitStats, UnitTrait, get_unit_trait_stats


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
        return f"""Note that all values assume max upgrade.
Unit Name: {self.name}
Damage: {self.damage}
SPA: {self.spa}
Range: {self.range}
Level: {self.level}
Trait: {self.trait}
Attack Stat: {self.attack_degree}
SPA Stat: {self.spa_degree}
Range Stat: {self.range_degree}
Memoria: {self.memoria}
Familiar: {self.familiar}
Final Estimated DPS: {self.expected_dps}
"""


def calculate_unit_stats(gathered_unit_data: pd.Series) -> FinalUnitData:
    """Given a properly formatted input Series from pandas, and memoria or familiars, reads all relevant information and preforms all of the necessary calculations for final stats and DPS."""
    familiar_placeholder = 1  # replace with familiar stats
    memoria_placeholder = 0  # replace with memoria stats
    trait_stats: TraitStats = get_unit_trait_stats(
        UnitTrait(gathered_unit_data["unit_trait"])
    )

    # converting these to percentile for later, they can't change at this point
    unit_spa_degree = gathered_unit_data["unit_spa_degree"] / 100 + 1
    unit_atk_degree = gathered_unit_data["unit_atk_degree"] / 100 + 1
    unit_rng_degree = gathered_unit_data["unit_rng_degree"] / 100 + 1

    unit_damage = float(  # to silence the type checker
        (
            (
                gathered_unit_data["unit_dmg"] * familiar_placeholder
                + memoria_placeholder
            )
            * (3.9442064 * (gathered_unit_data["unit_level"] / 60))
            * trait_stats.dmg
            * unit_atk_degree
        )
    )
    unit_spa = (
        gathered_unit_data["unit_spa"] * unit_spa_degree * familiar_placeholder
        + memoria_placeholder
    )
    unit_rng = (
        gathered_unit_data["unit_rng"] * unit_rng_degree * familiar_placeholder
        + memoria_placeholder
    )

    unit_dps = unit_damage * unit_spa

    final_unit_data = FinalUnitData(
        unit_id=gathered_unit_data["unit_id"],
        name=gathered_unit_data["unit_name"],
        damage=unit_damage,
        spa=unit_spa,
        range=unit_rng,
        level=gathered_unit_data["unit_level"],
        trait=gathered_unit_data["unit_trait"],
        attack_degree=unit_atk_degree,
        spa_degree=unit_spa_degree,
        range_degree=unit_rng_degree,
        memoria=None,
        familiar=None,
        expected_dps=unit_dps,
    )
    return final_unit_data
