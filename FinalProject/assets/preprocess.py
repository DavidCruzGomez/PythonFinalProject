import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from FinalProject.assets.utils import read_xls_from_folder

# Example usage
df = read_xls_from_folder()
if df is not None:
    print(df)


def summary(df):
    # Display the shape of the data
    print(f'data shape: {df.shape}')

    # Initialize summary DataFrame
    summ = pd.DataFrame(df.dtypes, columns=['Data Type'])

    # Calculate missing data
    summ['Missing#'] = df.isna().sum()
    summ['Missing%'] = df.isna().mean()  # More efficient calculation

    # Calculate duplicates and unique values
    summ['Dups'] = df.duplicated().sum()
    summ['Uniques'] = df.nunique().values
    summ['Count'] = df.count().values

    # Get descriptive statistics
    desc = df.describe(include='all').transpose()

    # Fill summary DataFrame with relevant statistics
    summ['Min'] = desc.get('min', pd.Series([None] * len(df.columns))).values
    summ['Max'] = desc.get('max', pd.Series([None] * len(df.columns))).values
    summ['Average'] = desc.get('mean', pd.Series([None] * len(df.columns))).values
    summ['Standard Deviation'] = desc.get('std', pd.Series([None] * len(df.columns))).values

    # Handle the case of missing rows for first, second, and third values
    if len(df) >= 3:
        summ['First Value'] = df.iloc[0].values
        summ['Second Value'] = df.iloc[1].values
        summ['Third Value'] = df.iloc[2].values
    else:
        summ['First Value'] = df.iloc[0].values if len(df) > 0 else [None] * len(df.columns)
        summ['Second Value'] = df.iloc[1].values if len(df) > 1 else [None] * len(df.columns)
        summ['Third Value'] = [None] * len(df.columns)

    # Display the summary
    print(summ)

print(summary(df))

