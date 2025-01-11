import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from FinalProject.assets.utils import read_xls_from_folder


def remove_outliers(df: pd.DataFrame, threshold: float = 1.5) -> pd.DataFrame:
    """
    Removes outliers from numeric columns in the dataframe using the IQR method.

    Args:
        df (pd.DataFrame): The input dataframe.
        threshold (float): The multiplier for the IQR to define outlier boundaries.

    Returns:
        pd.DataFrame: The dataframe with outliers removed.
    """
    num_cols = df.select_dtypes(include=[np.number])  # Select numeric columns
    for col in num_cols.columns:
        # Determinar el límite superior según la columna
        if col == "Q3_SCHOOL":
            upper_bound = 8  # Límite superior para 'Q3_SCHOOL'
        else:
            upper_bound = 5  # Límite superior para las demás columnas

        # Identificar los outliers
        outliers = df[(df[col] < 0) | (df[col] > upper_bound)][col]

        # Imprimir los valores outliers
        if not outliers.empty:
            print(f"Outliers detected in column '{col}':\n{outliers.tolist()}")

        # Filtrar las filas para eliminar los outliers
        df = df[
            (df[col] >= 0) & (df[col] <= upper_bound) if col != "Q3_SCHOOL" else (df[col] >= 0) & (
                        df[col] <= 8)]

    return df


# Reading data from the folder
df: pd.DataFrame = read_xls_from_folder()
if df is not None:
    print("Initial Dataframe:")
    print(df)

# Remove outliers from the dataframe
df = remove_outliers(df)
print("DataFrame after outlier removal:")
print(df)

# Cleaning the data by removing rows with missing values and duplicates
df = df.dropna()
df = df.drop_duplicates()

def calculate_entropy(series: pd.Series) -> float:
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
    entropy: float = -np.sum(value_counts * np.log2(value_counts))
    return entropy


def summary(df: pd.DataFrame) -> pd.DataFrame:
    # Filter numeric and non-numeric columns
    num_cols: pd.DataFrame = df.select_dtypes(include=[np.number])
    cat_cols: pd.DataFrame = df.select_dtypes(exclude=[np.number])

    # Display the shape of the data
    print(f'data shape: {df.shape}')

    # Initialize a summary DataFrame with the data types of each column
    summ: pd.DataFrame = pd.DataFrame(df.dtypes, columns=['Data Type'])

    # Calculate missing data for each column
    summ['Missing#'] = df.isna().sum()
    summ['Missing%'] = df.isna().mean() * 100

    # Calculate duplicates and unique values for each column
    summ['Dups'] = df.duplicated().sum()
    summ['Cardinality'] = df.nunique()
    summ['Count'] = df.count()


    # Calculate descriptive statistics only for numeric columns
    if not num_cols.empty:
        desc: pd.DataFrame = num_cols.describe().transpose() # Get descriptive stats
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
    first_values: np.ndarray = df.head(3).values
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


# Save the cleaned and transformed DataFrame to a CSV file
cleaned_data_path: str = os.path.join(os.path.dirname(__file__),
                                          "impulse_buying_data",
                                          "cleaned_data.csv"
                                         )
df.to_csv(cleaned_data_path, index=False)
print(f"Cleaned data saved to: {cleaned_data_path}")

# Save the processed data to a CSV file
processed_data_path: str = os.path.join(os.path.dirname(__file__),
                                        "impulse_buying_data",
                                        "processed_data.csv"
                                       )
summary_df: pd.DataFrame = summary(df)
summary_df.to_csv(processed_data_path, index=False)

print("Data preprocessing complete and saved to 'processed_data.csv'")
