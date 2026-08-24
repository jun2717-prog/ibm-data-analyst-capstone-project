"""
00_setup_and_load_data.py

Loads the Stack Overflow Developer Survey dataset used throughout this
project. Run this first in any notebook/session before the other scripts,
since they all assume a `df` DataFrame is already available.
"""

import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "n01PQ9pSmiRX6520flujwQ/survey-data.csv"
)

df = pd.read_csv(FILE_PATH)

print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(df.head())
