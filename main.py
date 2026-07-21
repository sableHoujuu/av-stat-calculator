import sys

import numpy as np
import pandas as pd

from src.calculator import calculate_unit_stats
from src.common_prompts import confirm
from src.data_loader import get_familiar_data, get_memoria_data, get_unit_data, validate_data
from src.data_processor import process_familiar
from src.trait_manager import UnitTrait


def main():
    # validate_data()
    while True:
        usr_input = str(input("Enter unit name: "))
        try:
            unit_name = usr_input.lower()
            print("Finding unit...")
            matching_units = get_unit_data(unit_name)
            print("Unit found.")
            break
        except ValueError:
            print("Unit could not be found, please try again.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    ### BIG IMPORTANT NOTE
    # make this and the memoria and familiar getters into a function at some point
    # they really all do the same thing
    if matching_units is pd.DataFrame:
        raise NotImplementedError
    matching_unit = matching_units.reset_index().iloc[
        0
    ]  # i know this is bad, but right now while the filter itself isn't implemented, this is necessary

    usr_input_values = {}

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
        except TypeError:
            print("Please input a number.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)
    usr_input_values["unit_level"] = unit_level

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
    usr_input_values["unit_trait"] = unit_trait

    # getting stat degrees
    while True:
        try:
            unit_atk_degree = float(input("Enter attack stat degree: "))
            if unit_atk_degree > 25.0 or unit_atk_degree < 0.0:
                print("Attack stat must be between 0 and 25.")
                continue
            break
        except TypeError:
            print("Please input a number.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    while True:
        try:
            unit_spa_degree = float(input("Enter SPA stat degree: "))
            if unit_spa_degree > 12.5 or unit_spa_degree < 0.0:
                print("SPA stat must be between 0 and 12.5.")
                continue
            break
        except TypeError:
            print("Please input a number.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    while True:
        try:
            unit_rng_degree = float(input("Enter range stat degree: "))
            if unit_rng_degree > 12.5 or unit_rng_degree < 0.0:
                print("Range stat must be between 0 and 12.5.")
                continue
            break
        except TypeError:
            print("Please input a number.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    usr_input_values["unit_atk_degree"] = unit_atk_degree
    usr_input_values["unit_spa_degree"] = unit_spa_degree
    usr_input_values["unit_rng_degree"] = unit_rng_degree
    # all required unit information gathered, time to start doing stuff, like packaging the data we have

    gathered_unit_data = pd.concat([matching_unit, pd.Series(usr_input_values)])

    calc_only_unit: bool = not confirm(
        "Would you like to perform the calculations using a memoria, familiar, or external buffs?"
    )
    if calc_only_unit is True:
        print(calculate_unit_stats(gathered_unit_data))
        return

    while True:
       usr_input = str(input("Enter memoria name: "))
       try:
           memoria_name = usr_input.lower()
           print("Finding memoria...")
           matching_memorias = get_memoria_data(memoria_name)
           print("Memoria found.")
           break
       except ValueError:
           print("Memoria could not be found, please try again.")
       except Exception as e:
           print(f"Unhandled exception: {e}")
           sys.exit(1)

    matching_memoria = matching_memorias.reset_index().iloc[0]

    while True:
        usr_input = str(input("Enter familiar name: "))
        try:
            familiar_name = usr_input.lower()
            print("Finding familiar...")
            matching_familiars = get_familiar_data(familiar_name)
            print("Familiar found.")
            break
        except ValueError:
            print("Familiar could not be found, please try again.")
        except Exception as e:
            print(f"Unhandled exception: {e}")
            sys.exit(1)

    matching_familiar = matching_familiars.reset_index().iloc[0]
    processed_familiar = process_familiar(matching_familiar)

    print(calculate_unit_stats(gathered_unit_data, memoria_data=matching_memoria, familiar_data=processed_familiar))


if __name__ == "__main__":
    main()
