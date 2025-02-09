"""
Unit tests for pie chart visualization functions.

This module contains a test suite using `unittest` to validate the behavior of:
- `create_pie_chart_general`: Generates a general pie chart for survey responses.
- `create_pie_chart_by_gender`: Creates gender-segmented pie charts.
- `create_pie_chart_by_school`: Generates school-based pie charts.
- `create_pie_chart_by_income`: Creates income-segmented pie charts.

Key Features Tested:
- Correct pie chart generation for different segmentation criteria.
- Handling of invalid inputs, missing columns, and empty datasets.
- Proper labeling, title formatting, and data mapping.
- Minimum percentage threshold handling for pie slices.

Dependencies:
- unittest
- pandas
- matplotlib
"""
# Standard library imports
import unittest

# Third-party imports
import pandas as pd
from matplotlib.figure import Figure

# Local project-specific imports
from src.visualization.charts.pie_charts import (
    create_pie_chart_general,
    create_pie_chart_by_gender,
    create_pie_chart_by_school,
    create_pie_chart_by_income
)


class TestPieCharts(unittest.TestCase):
    """
    Unit test suite for pie chart visualization functions.

    This class contains test cases for validating pie chart generation in
    `src.visualization.charts.pie_charts`. It checks for correct output types,
    error handling, and expected behavior under various conditions.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize test data once for all test methods.
        Creates a DataFrame with:
        - SC1: Survey responses (5 = Strongly Agree, descending to 1 = Strongly Disagree)
        - Q2_GENDER: Gender data (1 = Male, 0 = Female)
        - Q3_SCHOOL: School IDs (1-5 representing different institutions)
        - Q4_INCOME: Income brackets (1-4 representing different ranges)
        """
        cls.sample_data = {
            'SC1': [5, 4, 3, 2, 1],  # Survey responses
            'Q2_GENDER': [1, 0, 1, 0, 1],   # 1: Male, 0: Female
            'Q3_SCHOOL': [1, 2, 3, 4, 5],   # 5 different schools
            'Q4_INCOME': [1, 2, 3, 4, 1]    # 2x Under 3M, 1x 3-5M, 1x 5-10M, 1x Over 10M
        }
        cls.df = pd.DataFrame(cls.sample_data)


    # Tests for create_pie_chart_general
    def test_general_pie_success(self):
        """
        Test `create_pie_chart_general` with valid input.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Checks that the pie chart contains at least one slice.
        """
        fig = create_pie_chart_general(self.df, 'SC1')
        self.assertIsInstance(fig, Figure)  # Should return Figure object
        self.assertGreater(len(fig.axes[0].patches), 0)  # Verify that there are slices


    def test_general_pie_invalid_question(self):
        """
        Test `create_pie_chart_general` with an invalid question.

        - Ensures function returns None when provided with a non-existent question key.
        """
        fig = create_pie_chart_general(self.df, 'INVALID_QUESTION')
        self.assertIsNone(fig)  # Should return None for invalid columns


    # Tests for create_pie_chart_by_gender
    def test_gender_pie_comparison(self):
        """
        Test `create_pie_chart_by_gender` with valid input.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Verifies that the figure contains two subplots (one for each gender).
        """
        fig = create_pie_chart_by_gender(self.df, 'SC1')
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 2)  # Should display both genders


    def test_gender_pie_filtered(self):
        """
        Test `create_pie_chart_by_gender` with gender filtering.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Checks that the chart title correctly reflects the selected gender.
        """
        fig = create_pie_chart_by_gender(self.df, 'SC1', gender_filter='Male')
        self.assertIsInstance(fig, Figure)
        self.assertIn("Male", fig.axes[0].get_title())  # Title should reflect filter


    # Tests for create_pie_chart_by_school
    def test_school_pie_all(self):
        """
        Test `create_pie_chart_by_school` with all schools included.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Verifies that the figure contains as many subplots as there are schools.
        """
        fig = create_pie_chart_by_school(self.df, 'SC1')
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 5)  # 5 schools in the test data


    def test_school_pie_filter(self):
        """
        Test `create_pie_chart_by_school` with a specific school filter.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Checks that the chart title matches the filtered school name.
        """
        fig = create_pie_chart_by_school(self.df, 'SC1', school_filter='3')
        self.assertIsInstance(fig, Figure)  # Verify that a Figure object is returned
        # Verify school name mapping in title
        self.assertIn("Can Tho Medicine and Pharmacy University",
                      fig.axes[0].get_title())


    # Tests for create_pie_chart_by_income
    def test_income_pie_distribution(self):
        """
        Test `create_pie_chart_by_income` with all income brackets.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Verifies that the figure contains as many subplots as there are income levels.
        """
        fig = create_pie_chart_by_income(self.df, 'SC1')
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 4)  # 4 categories in the test data


    def test_income_pie_high_income(self):
        """
        Test `create_pie_chart_by_income` for a specific high-income filter.

        - Ensures the function returns a `matplotlib.figure.Figure` object.
        - Checks that the chart title correctly reflects the income category.
        - Verifies that at least one slice is present in the pie chart.
        """
        fig = create_pie_chart_by_income(self.df, 'SC1', income_filter='Over 10 million')

        # Should return a Figure since there's 1 matching entry
        self.assertIsInstance(fig, Figure)

        # Verify the title includes the income category
        self.assertIn("Over 10 million", fig.axes[0].get_title())

        # Verify there's at least 1 slice in the pie chart
        self.assertGreater(len(fig.axes[0].patches), 0)


    def test_income_pie_no_data(self):
        """
        Test `create_pie_chart_by_income` when filtering results in no data.

        - Ensures the function returns None when no entries match the filter criteria.
        """
        # Create test data with no entries for "Over 10 million"
        test_data = pd.DataFrame({
            'SC1': [5, 4, 3],
            'Q4_INCOME': [1, 2, 3]  # No entries with value 4
        })
        fig = create_pie_chart_by_income(test_data, 'SC1', income_filter='Over 10 million')
        self.assertIsNone(fig)  # No data should return None


    # Test for minimum percentage threshold
    def test_min_percentage_threshold(self):
        """
        Test `create_pie_chart_general` with a minimum percentage threshold.

        - Ensures that small categories are grouped into "Others" if they fall below the threshold.
        """
        test_data = pd.DataFrame({'SC1': [1]*20 + [2]*1})   # 95% vs 5%
        fig = create_pie_chart_general(test_data, 'SC1', min_percentage=5)
        labels = [text.get_text() for text in fig.axes[0].texts if text.get_text()]
        self.assertIn("Others", labels) # 5% value should be grouped


    # Test for answer mapping
    def test_answer_mapping(self):
        """
        Test `create_pie_chart_general` to ensure correct answer mapping.

        - Checks that response labels match expected descriptions (e.g., "Very agree").
        """
        fig = create_pie_chart_general(self.df, 'SC1')
        labels = [text.get_text() for text in fig.axes[0].texts if text.get_text()]
        self.assertIn("Very agree", labels)  # Value 5 "Very agree"


    # Test for title formatting
    def test_title_wrapping(self):
        """
        Test `create_pie_chart_general` for correct title formatting.

        - Ensures that generated titles contain expected keywords.
        - Prints the generated title for debugging if needed.
        """
        fig = create_pie_chart_general(self.df, 'SC1')
        title = fig.axes[0].get_title()

        # Verify that the title contains expected keywords
        expected_keywords = ['deadline', 'promotion', 'TikTok Shop', 'SC1']
        for keyword in expected_keywords:
            self.assertIn(keyword.lower(),
                          title.lower(),
                          f"Keyword '{keyword}' not found in title")

        # Print the generated title for debugging
        print(f"Generated title: {title}")


    # Test for empty data after filtering
    def test_empty_data_after_filter(self):
        """
        Test `create_pie_chart_by_gender` when filtering results in no matching data.

        - Ensures the function returns None when no data is available for the selected gender.
        """
        test_data = pd.DataFrame({
            'SC1': [5, 5, 5],
            'Q2_GENDER': [0, 0, 0]  # Only Female entries
        })
        fig = create_pie_chart_by_gender(test_data, 'SC1', gender_filter='Male')
        self.assertIsNone(fig)  # No Male data should return None


if __name__ == '__main__':
    unittest.main()
