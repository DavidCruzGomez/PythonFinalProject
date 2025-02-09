"""
Unit tests for bar chart visualization functions.

This module contains a test suite using `unittest` to validate the behavior of
bar chart generation functions from `src.visualization.charts.bar_charts`. The tests
cover general bar charts as well as segmented charts by gender, school, and income.

Tested Functions:
- `create_bar_chart_general`
- `create_bar_chart_by_gender`
- `create_bar_chart_by_school`
- `create_bar_chart_by_income`

Key Features Tested:
- Valid input handling for each function
- Invalid input handling (e.g., missing columns, incorrect question keys)
- Null value handling and expected warnings
- Custom category ordering in bar charts
- Verification of chart labels, legends, and expected output types

Mocked Data:
- Simulated survey responses
- Gender, school, and income categories
- Custom dictionaries mapping numerical codes to categorical labels

Dependencies:
- unittest
- pandas
- matplotlib
- unittest.mock (for patching)
"""
# Standard library imports
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd

# Local project-specific imports
from src.visualization.charts.bar_charts import (
    create_bar_chart_general,
    create_bar_chart_by_gender,
    create_bar_chart_by_school,
    create_bar_chart_by_income
)

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src')))

# Mock data dictionaries for testing
TEST_QUESTIONS = {
    'SC1': 'Test question 1',
    'SC2': 'Test question 2'
}

TEST_ANSWERS = {
    1: "Very disagree",
    2: "Disagree",
    3: "Normal",
    4: "Agree",
    5: "Very agree"
}

TEST_GENDER = {
    0: "Female",
    1: "Male"
}

TEST_SCHOOL = {
    1: "Can Tho FPT University",
    2: "Can Tho University"
}

TEST_INCOME = {
    1: "Under 3 million",
    2: "From 3 - 5 million"
}


class TestBarCharts(unittest.TestCase):
    """
    Unit test suite for bar chart visualization functions.

    This class contains test cases for validating bar chart generation functions
    in `src.visualization.charts.bar_charts`. It checks for correct output types,
    error handling, and expected behavior with different input scenarios.
    """
    def setUp(self):
        """
        Set up test environment before each test case.

        Creates a sample DataFrame representing survey data with columns for responses,
        gender, school, and income. Patches external dependencies to use mock data.
        """
        # Create valid test DataFrame with sample data
        self.valid_df = pd.DataFrame({
            'SC1': [1, 2, 3, 4, 5],         # Test responses for SC1 question
            'Q2_GENDER': [0, 1, 0, 1, 0],   # Gender distribution
            'Q3_SCHOOL': [1, 2, 1, 2, 1],   # School distribution
            'Q4_INCOME': [1, 2, 1, 2, 1]    # Income distribution
        })

        # Set up mocks with the full path
        self.patchers = [
            patch.dict('src.assets.impulse_buying_data.data_dictionary.questions', TEST_QUESTIONS),
            patch.dict('src.assets.impulse_buying_data.data_dictionary.answers', TEST_ANSWERS),
            patch.dict('src.assets.impulse_buying_data.data_dictionary.gender', TEST_GENDER),
            patch.dict('src.assets.impulse_buying_data.data_dictionary.school', TEST_SCHOOL),
            patch.dict('src.assets.impulse_buying_data.data_dictionary.income', TEST_INCOME)
        ]

        # Start all patchers and schedule cleanup
        for patcher in self.patchers:
            patcher.start()
            self.addCleanup(patcher.stop)


    def test_create_bar_chart_general_valid_input(self):
        """
        Test that `create_bar_chart_general` generates a valid bar chart
        when given a proper DataFrame.

        - Ensures the function returns a matplotlib Figure.
        - Checks that axis labels match expected values.
        """
        # Use an existing column in the DataFrame
        result = create_bar_chart_general(self.valid_df, 'SC1')
        self.assertIsInstance(result, plt.Figure) # Verify figure object
        ax = result.axes[0]

        # Verify axis labels
        self.assertEqual(ax.get_xlabel(), 'Degree of agreement/disagreement')
        self.assertEqual(ax.get_ylabel(), 'Number of Answers')


    def test_create_bar_chart_general_invalid_df(self):
        """
        Test `create_bar_chart_general` with invalid DataFrame inputs.

        - Ensures function returns None when given a None or empty DataFrame.
        """
        # Case 1: DataFrame is None
        result_none = create_bar_chart_general(None, 'SC1')
        self.assertIsNone(result_none, "Should return None when the DataFrame is None")

        # Case 2: Empty DataFrame
        result_empty = create_bar_chart_general(pd.DataFrame(), 'SC1')
        self.assertIsNone(result_empty, "Should return None when the DataFrame is empty")


    def test_create_bar_chart_general_invalid_question(self):
        """
        Test `create_bar_chart_general` with a non-existent question.

        - Verifies that passing an invalid question key results in a None return value.
        """
        result = create_bar_chart_general(self.valid_df, 'INVALID_QUESTION')
        self.assertIsNone(result, "Should return None when the question does not exist")


    def test_create_bar_chart_by_gender_valid(self):
        """
        Test `create_bar_chart_by_gender` with valid input.

        - Checks that a matplotlib Figure is returned.
        - Ensures the legend title matches 'Gender'.
        """
        # Use the correct question and remove redundant patches
        result = create_bar_chart_by_gender(self.valid_df, 'SC1')
        self.assertIsInstance(result, plt.Figure)
        ax = result.axes[0]

        # Verify legend title matches segmentation type
        self.assertEqual(ax.get_legend().get_title().get_text(), 'Gender')


    def test_create_bar_chart_by_gender_missing_column(self):
        """
        Test `create_bar_chart_by_gender` when the gender column is missing.

        - Ensures function returns None when required data is not present.
        """
        test_df = self.valid_df.drop(columns=['Q2_GENDER'])
        result = create_bar_chart_by_gender(test_df, 'SC1')
        self.assertIsNone(result, "Should return None when a required column is missing")


    def test_create_bar_chart_by_school_valid(self):
        """
        Test `create_bar_chart_by_school` with valid input.

        - Ensures the function produces a Figure.
        - Verifies that the legend title is 'School'.
        """
        result = create_bar_chart_by_school(self.valid_df, 'SC1')
        self.assertIsInstance(result, plt.Figure)
        ax = result.axes[0]
        self.assertEqual(ax.get_legend().get_title().get_text(), 'School')


    def test_create_bar_chart_by_income_valid(self):
        """
        Test `create_bar_chart_by_income` with valid input.

        - Ensures the function generates a Figure.
        - Checks that the legend title matches 'Income'.
        """
        result = create_bar_chart_by_income(self.valid_df, 'SC1')
        self.assertIsInstance(result, plt.Figure)
        ax = result.axes[0]
        self.assertEqual(ax.get_legend().get_title().get_text(), 'Income')


    def test_category_ordering(self):
        """
        Test category ordering functionality in `create_bar_chart_general`.

        - Verifies that the x-axis labels match the specified custom order.
        """
        custom_order = ['Disagree', 'Agree', 'Normal']
        result = create_bar_chart_general(
            self.valid_df,
            'SC1',
            category_order=custom_order
        )
        ax = result.axes[0]

        # Verify x-axis labels match custom order
        xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
        self.assertEqual(xtick_labels, custom_order)


    def test_null_values_handling(self):
        """
        Test handling of null values in `create_bar_chart_general`.

        - Ensures the function still produces a valid Figure.
        - Captures printed warnings about missing values.
        """
        test_df = self.valid_df.copy()
        test_df.loc[0, 'SC1'] = None # Introduce null value

        # Capture the print() output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = create_bar_chart_general(test_df, 'SC1')
            self.assertIsInstance(result, plt.Figure)

            # Verify the message in the standard output
            self.assertIn("Null values found", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
