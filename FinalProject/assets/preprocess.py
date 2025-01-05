import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from FinalProject.assets.utils import read_xls_from_folder

# Reading data from the folder
df = read_xls_from_folder()
if df is not None:
    print(df)

# Cleaning the data by removing rows with missing values and duplicates
df = df.dropna()
df = df.drop_duplicates()

def calculate_entropy(series):
    """
    Calculates the entropy of a column, which measures
    the uncertainty of the distribution of values in the column.

    The entropy is calculated using the formula:
        -sum(p * log2(p)) for each unique value's probability.

    Args:
    series (pd.Series): The column from which the entropy will be calculated.

    Returns:
    float: The entropy value of the column.
    """
    # Drop missing values and calculate the value counts (probabilities)
    value_counts = series.dropna().value_counts(normalize=True)
    # Entropy formula: -sum(p * log2(p)) for each unique value's probability
    entropy = -np.sum(value_counts * np.log2(value_counts))
    return entropy


def summary(df):
    # Filter numeric and non-numeric columns
    num_cols = df.select_dtypes(include=[np.number])
    cat_cols = df.select_dtypes(exclude=[np.number])

    # Display the shape of the data
    print(f'data shape: {df.shape}')

    # Initialize a summary DataFrame with the data types of each column
    summ = pd.DataFrame(df.dtypes, columns=['Data Type'])

    # Calculate missing data for each column
    summ['Missing#'] = df.isna().sum()
    summ['Missing%'] = df.isna().mean() * 100

    # Calculate duplicates and unique values for each column
    summ['Dups'] = df.duplicated().sum()
    summ['Cardinality'] = df.nunique()
    summ['Count'] = df.count()


    # Calculate descriptive statistics only for numeric columns
    if not num_cols.empty:
        desc = num_cols.describe().transpose() # Get descriptive stats
        summ['Min'] = desc['min']
        summ['Max'] = desc['max']
        summ['Average'] = desc['mean']
        summ['Standard Deviation'] = desc['std']
        summ['Range'] = summ['Max'] - summ['Min']
        summ['25%'] = desc['25%']
        summ['50%'] = desc['50%'] # Median (50th percentile)
        summ['75%'] = desc['75%']
        summ['IQR'] = summ['75%'] - summ['25%'] # Interquartile range (IQR)

    # Calculate the entropy of all columns
    summ['Entropy'] = df.apply(calculate_entropy)

    # Calculate the mode only for numeric columns
    summ['Mode'] = df.mode().iloc[0] # First value of mode (most frequent value)

    # Calculate skewness and kurtosis only for numeric columns
    if not num_cols.empty:
        # Measure of asymmetry (left/right skew)
        summ['Skewness'] = num_cols.skew()
        # Measure of peakness (how sharp the distribution is)
        summ['Kurtosis'] = num_cols.kurtosis()

    # Calculate outliers for numeric columns using IQR method
    if not num_cols.empty:
        summ['Outliers'] = num_cols.apply(lambda x: sum(
            # Lower bound for outliers
            (x < (desc.loc[x.name, '25%'] - 1.5 * summ.loc[x.name, 'IQR'])) |
            # Upper bound for outliers
            (x > (desc.loc[x.name, '75%'] + 1.5 * summ.loc[x.name, 'IQR']))
        ))

    # Handle the case of missing rows for first, second, and third values
    first_values = df.head(3).values
    for i, col in enumerate(df.columns):
        # Check the column's data type before assigning values
        if summ.at[col, 'Data Type'] in ['int64', 'float64']:
            summ.at[col, 'First Value'] = first_values[0, i] if len(first_values) > 0 else None
            summ.at[col, 'Second Value'] = first_values[1, i] if len(first_values) > 1 else None
            summ.at[col, 'Third Value'] = first_values[2, i] if len(first_values) > 2 else None
        else:
            # Ensure that non-numeric columns have 'object' type (for strings)
            if col in summ.columns:  # Check if the column exists in `summ`
                summ[col] = summ[col].astype('object')

            # Assign the values as strings
            summ.at[col, 'First Value'] = str(first_values[0, i]) if len(first_values) > 0 else None
            summ.at[col, 'Second Value'] = str(first_values[1, i]) if len(
                first_values) > 1 else None
            summ.at[col, 'Third Value'] = str(first_values[2, i]) if len(first_values) > 2 else None

    return summ


print(summary(df))
