import sys

import numpy as np
import pandas as pd

from src.data_loader import get_unit_data


def main():
    unit_name = input("Enter unit name: ")
    print("Finding unit...")
    matching_units = get_unit_data(unit_name.lower())
    if matching_units is pd.DataFrame:
        print("More than 1 unit found, implement this later")
        sys.exit(1)
    unit_level = input("Unit found.\nEnter unit level: ")


if __name__ == "__main__":
    main()
