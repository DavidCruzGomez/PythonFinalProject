"""
Unit tests for the `remove_outliers`, `calculate_entropy`, `summary`, and `main` functions
in the `FinalProject.assets.preprocess` module.

This test suite ensures that the preprocessing utilities, including data cleaning,
statistical analysis, and entropy calculations, function as expected under
a variety of conditions. It also validates the overall pipeline's correctness
from start to finish.

Key tests include:

- `TestRemoveOutliers`:
    - Verifies that the `remove_outliers` function correctly identifies and removes
      outliers from numeric columns.
    - Ensures non-outlier values are preserved and the resulting dataset is smaller.

- `TestCalculateEntropy`:
    - Confirms that the `calculate_entropy` function accurately computes entropy
      for categorical columns, including:
        - Columns with equal probabilities.
        - Columns with a dominant value.
        - Empty columns.

- `TestSummary`:
    - Tests the `summary` function to ensure it generates a comprehensive statistical
      summary for the input data, including:
        - Calculating missing values, duplicates, cardinality, and outliers.
        - Computing numeric statistics such as min, max, mean, IQR, and skewness.
        - Measuring categorical statistics like entropy and mode.

- `TestPipelineEndToEnd`:
    - Mocks an entire preprocessing pipeline using the `main` function.
    - Validates that the pipeline processes data correctly, generates cleaned datasets,
      and outputs the results to the specified directory.

Each test case focuses on validating both normal operations and edge cases, ensuring
the robustness and accuracy of the preprocessing functions. Cleanup steps are included
to remove temporary test data created during execution.
"""
# Standard library imports
import os
import shutil
import unittest
from unittest.mock import patch

# Third-party imports
import numpy as np
import pandas as pd

# Local project-specific imports
from FinalProject.assets.preprocess import remove_outliers, calculate_entropy, summary, main


class TestPreprocess(unittest.TestCase):
    """
    Unit tests for the functions in the `FinalProject.assets.preprocess` module.

    This class tests the following functions:
    - `remove_outliers`: Ensures outliers are correctly removed.
    - `calculate_entropy`: Verifies accurate entropy calculations.
    - `summary`: Checks if the summary statistics are computed correctly.
    - `main`: Validates the end-to-end preprocessing pipeline.
    """
    def setUp(self) -> None:
        """
        Setup common test data for reuse in multiple test cases.
        """
        self.sample_data: pd.DataFrame = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 100],  # Includes an outlier
            'Q3_SCHOOL': [1, 2, 3, 4, 10],    # Includes an outlier specific to Q3_SCHOOL
            'string_col': ['a', 'b', 'b', 'c', 'c'],  # Non-numeric column
            'missing_col': [1, 2, np.nan, 4, 5],  # Contains missing values
        })

    def test_remove_outliers(self) -> None:
        """
        Test the `remove_outliers` function to ensure it removes outliers correctly.
        """
        # Sample data with numeric and non-numeric columns
        self.sample_data = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 100],  # 100 is an outlier (default threshold is 5)
            'Q3_SCHOOL': [4, 5, 6, 10, 5],  # 10 is an outlier (specific threshold is 8)
            'non_numeric_col': ['a', 'b', 'c', 'd', 'e']  # Non-numeric column (should not be affected)
        })

        # Run the outlier removal function
        cleaned_df: pd.DataFrame = remove_outliers(self.sample_data.copy())

        # Assert that the outliers in numeric_col and Q3_SCHOOL are removed
        self.assertNotIn(100, cleaned_df['numeric_col'].values,
                         "Outlier 100 was not removed correctly")
        self.assertNotIn(10, cleaned_df['Q3_SCHOOL'].values, "Outlier 10 was not removed correctly")

        # Assert that non-outlier values are preserved
        self.assertIn(1, cleaned_df['numeric_col'].values, "Non-outlier value 1 was not preserved")
        self.assertIn(4, cleaned_df['Q3_SCHOOL'].values, "Non-outlier value 4 was not preserved")

        # Assert the number of rows is reduced after outlier removal
        self.assertLess(len(cleaned_df), len(self.sample_data),
                        "Number of rows did not decrease after outlier removal")

        # Assert that non-numeric columns are preserved for the remaining rows
        # After removing outliers, the non-numeric column should only contain ['a', 'b', 'c']
        expected_non_numeric_values = ['a', 'b', 'c']
        self.assertListEqual(
            cleaned_df['non_numeric_col'].tolist(),
            expected_non_numeric_values,
            "Non-numeric column was not preserved correctly after outlier removal"
        )

        # Test with custom thresholds (use a fresh copy of the original data)
        custom_thresholds = {'numeric_col': 150}  # Increase the threshold for numeric_col
        cleaned_df_custom = remove_outliers(self.sample_data.copy(),
                                            outlier_thresholds=custom_thresholds)

        # Assert that 100 is not considered an outlier with the custom threshold
        self.assertIn(100, cleaned_df_custom['numeric_col'].values,
                      "Value 100 should be preserved with the custom threshold for numeric_col")

        # Assert that 10 is still removed from Q3_SCHOOL (specific threshold remains 8)
        self.assertNotIn(10, cleaned_df_custom['Q3_SCHOOL'].values,
                         "Outlier 10 was not removed correctly with custom threshold for Q3_SCHOOL")

    def test_calculate_entropy(self) -> None:
        """
        Test the `calculate_entropy` function for accurate entropy calculation.
        """
        # Test with a column that has equal probabilities
        series: pd.Series = pd.Series(['a', 'b', 'c', 'd'])
        entropy = calculate_entropy(series)
        # 2 bits of entropy for 4 equally probable values
        self.assertAlmostEqual(entropy, 2.0, places=1)

        # Test with a column that has a dominant value
        series = pd.Series(['a', 'a', 'a', 'b'])
        entropy = calculate_entropy(series)
        self.assertLess(entropy, 1.0)  # Low entropy since 'a' dominates

        # Test with a completely empty column
        series = pd.Series([])
        entropy = calculate_entropy(series)
        self.assertEqual(entropy, 0.0)

    def test_summary(self) -> None:
        """
        Test the `summary` function to ensure it generates accurate statistics.
        """
        summary_df: pd.DataFrame = summary(self.sample_data)

        # Assert that the summary contains the correct columns
        expected_columns: list[str] = [
            'Data Type', 'Missing#', 'Missing%', 'Dups', 'Cardinality', 'Count',
            'Min', 'Max', 'Average', 'Standard Deviation', 'Range',
            '25%', '50%', '75%', 'IQR', 'Entropy', 'Mode', 'Skewness', 'Kurtosis', 'Outliers'
        ]
        for col in expected_columns:
            self.assertIn(col, summary_df.columns)

        # Assert missing values are calculated correctly
        self.assertEqual(summary_df.loc['missing_col', 'Missing#'], 1)
        self.assertEqual(summary_df.loc['missing_col', 'Missing%'], 20.0)

        # Assert the numeric statistics are calculated correctly
        self.assertEqual(summary_df.loc['numeric_col', 'Min'], 1)
        self.assertEqual(summary_df.loc['numeric_col', 'Max'], 100)
        self.assertEqual(summary_df.loc['numeric_col', 'IQR'], 2.0)  # Q3=3, Q1=1

        # Assert the entropy is calculated correctly
        self.assertGreater(summary_df.loc['string_col', 'Entropy'], 0.0)

        # Assert outlier counts are correct
        self.assertEqual(summary_df.loc['numeric_col', 'Outliers'], 1) # Only 100 is outlier

    @patch('FinalProject.assets.preprocess.read_xls_from_folder')
    def test_pipeline_end_to_end(self, mock_read_xls) -> None:
        """
        Test the `main` function to validate the end-to-end preprocessing pipeline.

        Validates:
        - The pipeline correctly processes numeric, categorical, and missing data.
        - Cleaned and processed files are generated in the specified output directory.
        - Temporary directories and files are cleaned up after execution.
        """
        # Mock input data
        mock_read_xls.return_value = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 100],
            'Q3_SCHOOL': [1, 2, 3, 4, 10],
            'string_col': ['a', 'b', 'b', 'c', 'c'],
            'missing_col': [1, 2, None, 4, 5],
        })

        # Temporary output directory for the test
        output_dir: str = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(output_dir, exist_ok=True)

        # Run the preprocessing pipeline
        main(output_dir=output_dir)

        # Verify that the cleaned and processed files were created
        cleaned_file: str = os.path.join(output_dir, "cleaned_data.csv")
        processed_file: str = os.path.join(output_dir, "processed_data.csv")

        self.assertTrue(os.path.exists(cleaned_file), f"{cleaned_file} does not exist.")
        self.assertTrue(os.path.exists(processed_file), f"{processed_file} does not exist.")

        # Clean up test output directory
        shutil.rmtree(output_dir)


if __name__ == "__main__":
    unittest.main()
