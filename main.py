import sys

import numpy as np
import pandas as pd

from src.data_loader import get_unit_data


def main():
    unit_name = input("Enter unit name: ")
    print("Finding unit...")
    matching_units = get_unit_data(unit_name)
    if matching_units is pd.DataFrame:
        print("More than 1 unit found, implement this later")
        sys.exit(1)
    print("Unit found.")
    while True:
        try:
            unit_level = int(input("Enter unit level: "))
            if unit_level > 60 or unit_level <= 0:
                print("Level must be between 1 and 60.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")


if __name__ == "__main__":
    main()
