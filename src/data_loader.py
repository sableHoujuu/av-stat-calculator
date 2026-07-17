import sys

import numpy as np
import pandas as pd

# Initializing the data once at runtime, we don't want to do this every time it's called.
# Later on this will be made into a function to be called at the beginning of main.py.
unit_data = pd.read_csv("data/units.csv", index_col="unit_id")
memoria_data = pd.read_csv("data/memoria.csv", index_col="memoria_id")
familiar_data = pd.read_csv("data/familiars.csv", index_col="familiar_id")


def validate_data():
    """Validates data files, ensuring they are not missing any information and are properly formatted."""
    raise NotImplementedError


def get_unit_data(name: str) -> pd.Series | pd.DataFrame:
    """Gets requested unit data from CSV data. If none is found, exits program."""
    # TODO: figure out how to remove things like apostrophes, and add alias checking (ex. gojo returns "today's strongest")
    name = name.lower()
    unit_rows = unit_data[unit_data["unit_name"].str.lower() == name]
    if unit_rows.empty:
        print("Can't find specified unit.")
        raise ValueError
    return unit_rows


def get_memoria_data(name: str) -> pd.Series | pd.DataFrame:
    # Functionally identical to get_unit_data, copy/paste grug for less bug (for now)
    name = name.lower()
    memoria_rows = memoria_data[memoria_data["memoria_name"].str.lower() == name]
    if memoria_rows.empty:
        print("Can't find specified memoria.")
        raise ValueError
    return memoria_rows

def get_familiar_data(name: str) -> pd.Series | pd.DataFrame:
    name = name.lower()
    familiar_rows = familiar_data[familiar_data["familiar_name"].str.lower() == name]
    if familiar_rows.empty:
        print("Can't find specified familiar.")
        raise ValueError
    return familiar_rows
