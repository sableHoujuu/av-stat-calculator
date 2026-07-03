# Holds trait stats, and provides helper functions for traits. We don't store these in a CSV because traits don't have
# nearly as much variability as units, and there are also far fewer.
from enum import Enum


class UnitTrait(Enum):
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
