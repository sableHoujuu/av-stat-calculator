# Holds trait stats, and provides helper functions for traits. We don't store these in a CSV because traits don't have
# nearly as much variability as units, and there are also far fewer.
from collections import namedtuple
from enum import Enum


class UnitTrait(Enum):
    NONE = "none"
    VIGOR = "vigor"
    SWIFT = "swift"
    RANGE = "range"
    MARKSMAN = "marksman"
    SCHOLAR = "scholar"
    BLITZ = "blitz"
    FORTUNE = "fortune"
    DEADEYE = "deadeye"
    SOLAR = "solar"
    ETHEREAL = "ethereal"
    MONARCH = "monarch"


TraitStats = namedtuple(
    "TraitStats",
    ["dmg", "spa", "rng", "crit_chance", "crit_dmg"],
    defaults=[1.0, 1.0, 1.0, 0.0, 0.0],
)


def get_unit_trait_stats(trait: UnitTrait) -> TraitStats:
    match trait:
        case UnitTrait.MONARCH:
            return TraitStats(
                dmg=4, spa=0.9, rng=1.05
            )  # remember, dmg is +300%, which is equivalent to * 4
        case UnitTrait.ETHEREAL:
            return TraitStats(dmg=1.2, spa=0.8, rng=1.05)
        case UnitTrait.SOLAR:
            return TraitStats(dmg=1.1, spa=0.95, rng=1.25)
        case UnitTrait.DEADEYE:
            return TraitStats(
                crit_chance=0.45, crit_dmg=0.5
            )  # crit is additive with itself, which is why we don't put 1.45
        case UnitTrait.BLITZ:
            return TraitStats(spa=0.8)
        case UnitTrait.FORTUNE:
            return TraitStats()
        case UnitTrait.MARKSMAN:
            return TraitStats(rng=1.3)
        case UnitTrait.SCHOLAR:
            return TraitStats()
        case UnitTrait.VIGOR:
            raise NotImplementedError
        case UnitTrait.SWIFT:
            raise NotImplementedError
        case UnitTrait.RANGE:
            raise NotImplementedError
        case UnitTrait.NONE:
            return TraitStats()
        case other:
            raise ValueError(f"impossible trait value: {other}")
