# All functions and classes related to calculating things and packaging the data.
from dataclasses import dataclass
from typing import cast

import numpy as np
import pandas as pd

from src.trait_manager import TraitStats, UnitTrait, get_unit_trait_stats
from src.data_loader import get_unit_passive_data, UnitPassiveRow


@dataclass
class FinalUnitData:
    unit_id: int
    name: str
    damage: float
    damage_per_crit: float
    spa: float
    range: float
    level: int
    trait: UnitTrait | None
    attack_degree: float
    spa_degree: float
    range_degree: float
    memoria: str | None
    familiar: str | None
    unit_dps: float
    total_dps_including_passives: float

    def __str__(self):
        return f"""Note that all values assume max upgrade.
Unit Name: {self.name}
Damage: {self.damage}
Damage Per Crit: {self.damage_per_crit}
SPA: {self.spa}
Range: {self.range}
Level: {self.level}
Trait: {self.trait} (fix this to print the trait name)
Attack Stat: {(self.attack_degree - 1) * 100}%
SPA Stat: {(self.spa_degree - 1) * 100}%
Range Stat: {(self.range_degree - 1) * 100}%
Memoria: {self.memoria}
Familiar: {self.familiar}
Raw Unit DPS (excluding crits or dot): {self.unit_dps}
Final Estimated DPS (including everything): {self.total_dps_including_passives}
"""


def calculate_unit_stats(gathered_unit_data: pd.Series, memoria_data=None, familiar_data=None) -> FinalUnitData:
    """Given a properly formatted input Series from pandas, and memoria or familiars, reads all relevant information and preforms all of the necessary calculations for final base stats and DPS. Handles passives."""

    # converting these to percentile for later, they can't change at this point
    unit_spa_degree = 1 - (gathered_unit_data["unit_spa_degree"] / 100)
    # ^ this one makes things go down so, needs to be inverse
    unit_atk_degree = (gathered_unit_data["unit_atk_degree"] / 100) + 1
    unit_rng_degree = (gathered_unit_data["unit_rng_degree"] / 100) + 1

    if memoria_data is None:
        memoria_dmg, memoria_rng = 0, 0
        memoria_name = None
    else:
        memoria_dmg, memoria_rng = memoria_data["memoria_dmg"], memoria_data["memoria_rng"]
        memoria_name = memoria_data["memoria_name"]

    if familiar_data is None:
        familiar_dmg, familiar_spa, familiar_rng, familiar_crit_chance, familiar_crit_dmg = 1, 1, 1, 0, 0
        familiar_name = None
    else:
        familiar_dmg = familiar_data["familiar_dmg_modifier"]
        familiar_spa = familiar_data["familiar_spa_modifier"]
        familiar_rng = familiar_data["familiar_rng_modifier"]
        familiar_crit_chance = familiar_data["familiar_crit_chance_modifier"]
        familiar_crit_dmg = familiar_data["familiar_crit_chance_modifier"]
        familiar_name = familiar_data["familiar_name"]

    trait_stats: TraitStats = get_unit_trait_stats(
        UnitTrait(gathered_unit_data["unit_trait"])
    )

    # now we do unit passive stuff and begin keeping track of buffs
    unit_passives = get_unit_passive_data(gathered_unit_data["unit_id"])
    if unit_passives is not None:
        # we express all of the dot as percentages of the main damage, per second
        # ex. 100% bleed for 5 seconds = 0.2 bleed_dps_percent (20% of unit damage, per second)
        bleed_dmg = burn_dmg = non_ampable_dot_dmg = non_stackable_dot_dmg = 0
        burn_amp = bleed_amp = dot_amp = 0
        universal_amp = 0
        dmg_buff = range_buff = spa_buff = 0
        crit_rate_buff = crit_dmg_buff = 0
        for passive in unit_passives:
            passive = cast(UnitPassiveRow, passive)
            match passive.passive_type:
                case "dot_burn":
                    burn_dmg += (passive.value / passive.status_duration)
                case "dot_bleed":
                    bleed_dmg += (passive.value / passive.status_duration)
                case "diseased":
                    dot_amp += passive.value
                case "dismantle":
                    bleed_amp += passive.value
                case "universal_amp":
                    universal_amp += passive.value
                case "permanent_buff" | "conditional_buff":
                    match passive.value_affects:
                        case "damage":
                            dmg_buff += passive.value
                        case "spa":
                            spa_buff += passive.value
                        case "range":
                            range_buff += passive.value
                        case "crit_rate":
                            crit_rate_buff += passive.value
                        case "crit_dmg":
                            crit_dmg_buff += passive.value
        bleed_dps_percent = bleed_dmg * (1 + bleed_amp + dot_amp)
        burn_dps_percent = burn_dmg * (1 + burn_amp + dot_amp)
        dot_dps_percent = (burn_dps_percent + bleed_dps_percent + non_ampable_dot_dmg + non_stackable_dot_dmg) * (1 + universal_amp)

    unit_damage = float(
            (
                gathered_unit_data["unit_dmg"] * (1 + familiar_dmg)
                + (memoria_dmg  #* (3.9442064 * (memoria_level / 60))
                )
            )
            * (1 + (2.9442064 * ((gathered_unit_data["unit_level"] - 1) / 59)))
            * trait_stats.dmg
            * unit_atk_degree
    ) * (1 + dmg_buff + universal_amp)
    unit_spa = (
        gathered_unit_data["unit_spa"]
        * (1 - (1 - unit_spa_degree) - (1 - familiar_spa) - (1 - trait_stats.spa))
    ) * (1 + spa_buff)
    unit_rng = (
        (gathered_unit_data["unit_rng"] + memoria_rng)
        * (unit_rng_degree + familiar_rng + trait_stats.rng)
    ) * (1 + range_buff)

    raw_dps = unit_damage / unit_spa
    crit_dmg = unit_damage * (1 + (crit_dmg_buff + 1.25 + familiar_crit_dmg) * (crit_rate_buff + familiar_crit_chance))
    final_dps = (crit_dmg / unit_spa) * dot_dps_percent


    final_unit_data = FinalUnitData(
        unit_id=gathered_unit_data["unit_id"],
        name=gathered_unit_data["unit_name"],
        damage=unit_damage,
        damage_per_crit=unit_damage * (1 + (crit_dmg_buff + 1.25 + familiar_crit_dmg)),
        spa=unit_spa,
        range=unit_rng,
        level=gathered_unit_data["unit_level"],
        trait=gathered_unit_data["unit_trait"],
        attack_degree=unit_atk_degree,
        spa_degree=unit_spa_degree,
        range_degree=unit_rng_degree,
        memoria=memoria_name,
        familiar=familiar_name,
        unit_dps=raw_dps,
        total_dps_including_passives=final_dps,
    )

    return final_unit_data
