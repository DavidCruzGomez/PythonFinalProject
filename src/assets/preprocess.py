"""
Preprocessing pipeline for cleaning and summarizing survey data.

This script processes survey data by performing tasks such as loading raw data,
removing outliers, cleaning the dataset, and generating a detailed summary. The goal
is to prepare the data for further analysis by ensuring its quality and consistency.

Key steps in the pipeline include:

- **Loading Data**:
  Reads survey data from Excel files located in a specific directory using
  the `read_xls_from_folder` utility function.

- **Outlier Removal**:
  Identifies and removes outliers in numeric columns based on predefined thresholds,
  such as the IQR method and column-specific limits (e.g., the `Q3_SCHOOL` column).

- **Data Cleaning**:
  Cleans the dataset by handling missing values and duplicates, ensuring only
  relevant and complete rows remain.

- **Summary Generation**:
  Produces a detailed summary of the dataset, including:
  - Missing data statistics.
  - Descriptive statistics for numeric columns (mean, median, range, etc.).
  - Entropy calculations for all columns, measuring the uncertainty of value distributions.
  - Detection and counting of outliers based on the IQR method.
  - Cardinality and duplicate counts for each column.

- **Saving Results**:
  Outputs two files:
  1. `cleaned_data.csv`: The cleaned dataset, free of outliers and duplicates.
  2. `processed_data.csv`: A comprehensive summary of the dataset's structure and contents.

Functions:
----------
1. `remove_outliers(df: pd.DataFrame) -> pd.DataFrame`:
   Removes outliers from numeric columns based on the IQR method or predefined thresholds.

2. `calculate_entropy(series: pd.Series) -> float`:
   Calculates the entropy of a column to measure the uncertainty of its value distribution.

3. `summary(df: pd.DataFrame) -> pd.DataFrame`:
   Generates a detailed summary of the dataset, including descriptive statistics,
   entropy, and outlier detection.

Output Files:
-------------
1. `cleaned_data.csv`: A cleaned version of the input dataset.
2. `processed_data.csv`: A summary of the dataset with detailed insights.
"""
# Standard library imports
import os

# Third-party imports
import numpy as np
import pandas as pd

# Local project-specific imports
from src.assets.utils import read_xls_from_folder


def remove_outliers(df: pd.DataFrame, outlier_thresholds: dict = None) -> pd.DataFrame:
    """
    Removes outliers from numeric columns in the dataframe using the IQR method
    or predefined thresholds.

    Args:
        df (pd.DataFrame): The input dataframe.
        outlier_thresholds (dict): A dictionary with column names as keys
        and upper bounds as values. If not provided, default thresholds will be used.

    Returns:
        pd.DataFrame: The dataframe with outliers removed.
    """
    try:
        print("📂 Original DataFrame:")
        print(df)
        print("⏳ [INFO] Starting outlier removal process...")
        # Select only numeric columns from the dataframe
        num_cols = df.select_dtypes(include=[np.number])

        # Define default thresholds
        default_thresholds = {col: 5 for col in num_cols.columns}
        default_thresholds["Q3_SCHOOL"] = 8  # Specific threshold for 'Q3_SCHOOL'

        # Combine default thresholds with custom thresholds (if provided)
        if outlier_thresholds is not None:
            # Update default thresholds with custom thresholds
            default_thresholds.update(outlier_thresholds)

        # Use the combined thresholds
        outlier_thresholds = default_thresholds

        print(f"📊 Outlier thresholds being used: {outlier_thresholds}")

        # Iterate over each numeric column
        for col in num_cols.columns:
            # Get the upper bound for the current column
            upper_bound = outlier_thresholds.get(col, 5)  # Default to 5 if no threshold is set
            print(f"🔍 Processing column: {col}, Upper bound: {upper_bound}")

            # Identify outliers in the current column
            outliers = df[(df[col] < 0) | (df[col] > upper_bound)][col]

            # If outliers are found, print a warning with the outlier values
            if not outliers.empty:
                print(f"⚠️ [WARNING] Outliers detected in column '{col}':\n{outliers.tolist()}")

            # Filter rows to exclude outliers
            df = df[(df[col] >= 0) & (df[col] <= upper_bound)]

        # Print a success message once the process is complete
        print("✅ [SUCCESS] Outlier removal process completed successfully."
              f" The dataset now contains {len(df)} rows.")
        print("🔄 DataFrame after removing outliers")
        print(df)
        return df

    except KeyError as key_err:
        print(f"❌ [ERROR] Column not found in DataFrame: {key_err}")
        return df

    except Exception as gen_err:
        print(f"❌ [ERROR] An error occurred during outlier removal: {gen_err}")
        return df


def calculate_entropy(series: pd.Series) -> float:
    """
    Calculates the entropy of a column, which measures
    the uncertainty of the distribution of values in the column.

    The entropy is calculated using the formula:
        -sum(p * log2(p)) for each unique value's probability.

    Args:
    series (pd.Series): The column from which the entropy will be calculated.

    Returns:
    float: The entropy value of the column. Returns 0 if the series is empty
    or contains only NaN values.
    """
    try:
        # Check if the input is a pandas Series
        if not isinstance(series, pd.Series):
            raise TypeError("Input must be a pandas Series.")

        # Drop missing values and calculate the value counts (probabilities)
        value_counts = series.dropna().value_counts(normalize=True)

        # If the series is empty or contains only NaN values, return 0
        if value_counts.empty:
            return 0.0

        # Entropy formula: -sum(p * log2(p)) for each unique value's probability
        # Avoid log2(0) by filtering out probabilities equal to 0
        probabilities = value_counts[value_counts > 0]
        entropy: float = -np.sum(probabilities * np.log2(probabilities))

        return entropy

    except TypeError as type_err:
        print(f"❌ [ERROR] Invalid input type: {type_err}")
        return np.nan  # Return NaN for invalid input type

    except ValueError as val_err:
        print(f"❌ [ERROR] Invalid values in the series: {val_err}")
        return np.nan  # Return NaN for invalid values

    except AttributeError as attr_err:
        print(f"❌ [ERROR] Input does not have required attributes: {attr_err}")
        return np.nan  # Return NaN for attribute errors

    except Exception as gen_err:
        print(f"❌ [ERROR] An error occurred while calculating entropy: {gen_err}")
        return np.nan  # Return NaN for any other unexpected errors


def summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a summary of the dataframe including statistics, entropy,
    outliers, and descriptive values.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A summary dataframe with detailed statistics.
    """
    try:
        print("⏳ [INFO] Generating summary of the dataset...")
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

        # Calculate the number of duplicate rows and unique values for each column
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
            if summ.at[col, 'Data Type'] in ['int64', 'float64']: # For numeric columns

                summ.at[col, 'First Value'] = first_values[0, i] if len(first_values) > 0 else None
                summ.at[col, 'Second Value'] = first_values[1, i] if len(first_values) > 1 else None
                summ.at[col, 'Third Value'] = first_values[2, i] if len(first_values) > 2 else None
            else:
                # Ensure that non-numeric columns have 'object' type (for strings)
                if col in summ.columns:  # Check if the column exists in `summ`
                    summ[col] = summ[col].astype('object')

                # Assign the values as strings
                summ.at[col, 'First Value'] = str(first_values[0, i]) if len(
                    first_values) > 0 else None
                summ.at[col, 'Second Value'] = str(first_values[1, i]) if len(
                    first_values) > 1 else None
                summ.at[col, 'Third Value'] = str(first_values[2, i]) if len(
                    first_values) > 2 else None

        print("✅ [SUCCESS] Dataset summary generated successfully.")
        return summ

    except KeyError as key_err:
        print(f"❌ [ERROR] Column not found in DataFrame: {key_err}")
        return pd.DataFrame()

    except Exception as gen_err:
        print(f"❌ [ERROR] An error occurred while generating the summary: {gen_err}")
        return pd.DataFrame()


def main(output_dir=None):
    """
    Main function for running the preprocessing pipeline.
    Args:
        output_dir (str): Optional path where the output files will be saved.
                          Defaults to the directory of this script.
    """
    try:
        # Set default output directory if not provided
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), "impulse_buying_data")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Read the Excel files from the folder into a DataFrame
        print("⏳ [INFO] Loading dataset from Excel files...")
        df: pd.DataFrame = read_xls_from_folder()

        # Check if data was loaded successfully
        if df is None:
            raise ValueError("No data was loaded. Please check the input folder.")

        print("Initial Dataframe:")
        print(df)

        print("⏳ [INFO] Removing duplicates and cleaning missing data...")
        # Remove outliers from the dataframe
        df = remove_outliers(df)
        print("DataFrame after outlier removal:")
        print(df)

        # Clean the data by dropping rows with missing values
        df = df.dropna()

        # Remove duplicate rows
        df = df.drop_duplicates()
        print("✅ [SUCCESS] Duplicates removed and missing data handled.")

        # Save the cleaned and transformed DataFrame to a CSV file
        cleaned_data_path: str = os.path.join(output_dir, "cleaned_data.csv")
        df.to_csv(cleaned_data_path, index=False)
        print(f"✅ [SUCCESS] Cleaned data saved to: {cleaned_data_path}")

        print("⏳ [INFO] Generating and saving dataset summary...")
        # Save the processed data to a CSV file
        processed_data_path: str = os.path.join(output_dir, "processed_data.csv")
        summary_df: pd.DataFrame = summary(df)
        summary_df.to_csv(processed_data_path, index=False)

        print(f"✅ [SUCCESS] Summary saved to: {processed_data_path}")

    except Exception as gen_err:
        print(f"❌ [ERROR] An error occurred during data processing: {gen_err}")


if __name__ == "__main__":
    main()
