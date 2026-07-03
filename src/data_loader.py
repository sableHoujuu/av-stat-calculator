import sys

import numpy as np
import pandas as pd

# Initializing the data once at runtime, we don't want to do this every time it's called
unit_data = pd.read_csv("data/units.csv", index_col="unit_id")


def get_unit_data(name: str) -> pd.Series | pd.DataFrame:
    # TODO: figure out how to remove things like apostrophes, and add alias checking (ex. gojo returns "today's strongest")
    name = name.lower()
    try:
        unit_rows = unit_data[unit_data["unit_name".lower()] == name]
    except KeyError:
        print("Can't find specified unit, exiting.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    return unit_rows
