import sys
from typing import cast, NamedTuple
from collections import namedtuple

import numpy as np
import pandas as pd

from src.common_prompts import range_prompt, confirm

# Initializing the data once at runtime, we don't want to do this every time it's called.
# Later on this will be made into a function to be called at the beginning of main.py.
unit_data = pd.read_csv("data/units.csv", index_col="unit_id")
unit_passive_data = pd.read_csv("data/unit_passives.csv")
memoria_data = pd.read_csv("data/memoria.csv", index_col="memoria_id")
familiar_data = pd.read_csv("data/familiars.csv", index_col="familiar_id")

RawUnitPassiveRow = namedtuple(
    "RawUnitPassiveRow",
    [
        'unit_id',
        'passive_type',
        'min_value',
        'max_value',
        'value_affects',
        'value_type',
        'status_duration',
        'application',
        'query_user',
        'description'
    ]
)

UnitPassiveRow = namedtuple(
    "UnitPassiveRow",
    [
        'unit_id',
        'passive_type',
        'value',
        'value_affects',
        'status_duration',
        'application',
        'description'
    ]
)



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

def get_unit_passive_data(unit_id: int) -> list | None:
    """Given a unit_id, returns a list of UnitPassiveRow(s) with the relevant data. If the query_user value of the passive is TRUE, will prompt the user for if it applies to this calculation, otherwise it is considered to be always active."""
    passive_rows: pd.DataFrame = unit_passive_data[unit_passive_data["unit_id"] == unit_id]
    if passive_rows.empty:
        print("Unit has no passives. If this is unexpected, check data formatting.")
        return None
    processed_rows = []
    for row in passive_rows.itertuples(index=False):
        row = cast(RawUnitPassiveRow, row)
        if row.query_user is True:
            skip = not confirm(f"Would you like to include this unit passive in the calculation?\n{row.description}")
            if skip is True:
                print("Skipping passive...")
                continue
        new_row = {}
        new_row["unit_id"] = row.unit_id
        new_row["passive_type"] = row.passive_type
        new_row["description"] = row.description
        new_row["application"] = row.application
        new_row["value_affects"] = row.value_affects
        new_row["status_duration"] = row.status_duration

        if row.value_type == "max":
            new_row["value"] = row.max_value
        elif row.value_type == "range":
            new_row["value"] = range_prompt(f"Please enter the desired value for the passive '{row.description}'",row.min_value, row.max_value)

        processed_rows.append(UnitPassiveRow(**new_row))

    return processed_rows
