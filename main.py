import sys

import numpy as np
import pandas as pd

from src.common_prompts import confirm
from src.data_loader import get_unit_data
from src.trait_manager import UnitTrait


def main():
    unit_name = input("Enter unit name: ")
    print("Finding unit...")
    matching_units = get_unit_data(unit_name)
    if matching_units is pd.DataFrame:
        raise NotImplementedError
    print("Unit found.")

    # getting level
    while True:
        try:
            unit_level = int(input("Enter unit level: "))
            if unit_level > 60 or unit_level <= 0:
                print("Level must be between 1 and 60.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    # getting trait
    while True:
        usr_input = str(input("Enter unit trait: "))
        try:
            unit_trait = UnitTrait(usr_input.lower())
            break
        except ValueError:
            print("Please input a valid trait.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    # getting stat degrees
    while True:
        try:
            unit_atk_degree = float(input("Enter attack stat degree: "))
            if unit_atk_degree > 25.0 or unit_atk_degree <= 0.0:
                print("Attack stat must be between 0 and 25.")
                continue
            break
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    while True:
        try:
            unit_spa_degree = float(input("Enter SPA stat degree: "))
            if unit_spa_degree > 12.5 or unit_spa_degree <= 0.0:
                print("SPA stat must be between 0 and 12.5.")
                continue
            break
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    while True:
        try:
            unit_rng_degree = float(input("Enter range stat degree: "))
            if unit_rng_degree > 12.5 or unit_rng_degree <= 0.0:
                print("Range stat must be between 0 and 12.5.")
                continue
            break
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    # all required unit information gathered, time to start doing stuff, after one last prompt

    calc_only_unit: bool = not confirm(
        "Would you like to perform the calculations using a memoria, familiar, or external buffs?"
    )
    if calc_only_unit is True:
        print("gonna calc")
        return
    raise NotImplementedError


if __name__ == "__main__":
    main()
