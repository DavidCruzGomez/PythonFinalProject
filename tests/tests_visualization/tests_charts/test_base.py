"""
Unit tests for survey response visualization functions.

This module contains a test suite using `unittest` to validate the behavior of:
- `load_data`: Loads survey response data from a CSV file.
- `visualize_survey_responses`: Generates bar and pie charts based on survey responses.
- `build_question_selector`: Creates a question selection dropdown in a GUI.

Key Features Tested:
- Correct loading and handling of survey data.
- Proper visualization generation with different parameters.
- GUI component construction for question selection.
- Error handling for missing data, invalid inputs, and unexpected failures.

Dependencies:
- unittest
- pandas
- PySide6.QtWidgets
- matplotlib
- unittest.mock (for patching and mock testing)
"""
# Standard library imports
import unittest
from unittest.mock import patch, MagicMock

# Third-party imports
import pandas as pd
from PySide6.QtWidgets import QApplication, QComboBox, QWidget
from matplotlib.figure import Figure

# Local project-specific imports
from src.assets.impulse_buying_data.data_dictionary import questions
from src.visualization.charts.base import (
    load_data,
    visualize_survey_responses,
    build_question_selector
)

# Required for Qt tests
app = QApplication([])


class TestSurveyVisualizationController(unittest.TestCase):
    """
    Unit test suite for survey visualization functions.

    This class contains test cases for validating data loading, visualization, and GUI
    elements in `src.visualization.charts.base`. It checks for correct output types,
    error handling, and expected behavior under various conditions.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up test environment before running test cases.

        Creates a sample DataFrame simulating survey response data with columns for
        survey answers, gender, school, and income level.
        """
        # Sample data for testing
        cls.sample_data = pd.DataFrame({
            'SC1': [5, 4, 3, 2, 1], # Sample survey responses
            'Q2_GENDER': [1, 0, 1, 0, 1],   # Gender column (1 = Male, 0 = Female)
            'Q3_SCHOOL': [1, 2, 3, 4, 5],   # School identifier
            'Q4_INCOME': [1, 2, 3, 4, 1]    # Income level identifier
        })


    # Tests for load_data()
    @patch('pandas.read_csv')
    @patch('os.path.join')
    @patch('os.path.abspath')
    def test_load_data_success(self, mock_abspath, mock_join, mock_read_csv):
        """
        Test successful data loading with `load_data`.

        - Mocks file path resolution and CSV loading.
        - Ensures `pandas.read_csv` is called with the correct file path.
        - Asserts that the returned DataFrame matches expected sample data.
        """
        # Configure mocks to simulate file path resolution and CSV loading.
        mock_abspath.return_value = '/dummy/path'
        mock_join.return_value = '/dummy/path/cleaned_data.csv'
        mock_read_csv.return_value = self.sample_data

        # Execute load_data function
        result = load_data()

        # Validate that read_csv was called with the correct file path
        mock_read_csv.assert_called_once_with('/dummy/path/cleaned_data.csv')

        # Assert that the returned DataFrame matches the sample data.
        self.assertTrue(result.equals(self.sample_data))


    @patch('pandas.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        """
        Test `load_data` handling of a missing file.

        - Mocks `pandas.read_csv` to raise FileNotFoundError.
        - Ensures the function returns None when the file is missing.
        """
        # Simulate a FileNotFoundError.
        mock_read_csv.side_effect = FileNotFoundError

        # Execute the function under test.
        result = load_data()

        # Assert that the function returns None.
        self.assertIsNone(result)


    @patch('pandas.read_csv')
    def test_load_data_empty_file(self, mock_read_csv):
        """
        Test `load_data` handling of an empty file.

        - Mocks `pandas.read_csv` to raise `pandas.errors.EmptyDataError`.
        - Ensures the function returns None when the file is empty.
        """
        # Simulate an EmptyDataError.
        mock_read_csv.side_effect = pd.errors.EmptyDataError

        # Execute the function under test
        result = load_data()

        # Assert that the function returns None.
        self.assertIsNone(result)


    # Tests for visualize_survey_responses()
    @patch('src.visualization.charts.base.load_data')
    def test_visualize_default_bar_chart(self, mock_load):
        """
        Test `visualize_survey_responses` for general bar chart.

        - Mocks data loading to return sample survey data.
        - Ensures the function returns a `matplotlib.figure.Figure` object.
        """
        # Configure the mock to return sample data.
        mock_load.return_value = self.sample_data

        # Execute the function under test.
        result = visualize_survey_responses('SC1')

        # Assert that the result is a Figure object.
        self.assertIsInstance(result, Figure)


    @patch('src.visualization.charts.base.load_data')
    def test_visualize_gender_bar_chart(self, mock_load):
        """
        Test `visualize_survey_responses` for gender-segmented bar chart.

        - Mocks data loading to return sample survey data.
        - Ensures the function returns a `matplotlib.figure.Figure` object.
        """
        # Configure the mock to return sample data.
        mock_load.return_value = self.sample_data

        # Execute the function under test.
        result = visualize_survey_responses('SC1', distinction_by_gender=True)

        # Assert that the result is a Figure object.
        self.assertIsInstance(result, Figure)


    @patch('src.visualization.charts.base.load_data')
    def test_visualize_pie_chart_general(self, mock_load):
        """
        Test `visualize_survey_responses` for a general pie chart.

        - Mocks data loading to return sample survey data.
        - Ensures the function returns a `matplotlib.figure.Figure` object.
        """
        # Configure the mock to return sample data.
        mock_load.return_value = self.sample_data

        # Execute the function under test.
        result = visualize_survey_responses('SC1', pie_chart=True)

        # Assert that the result is a Figure object.
        self.assertIsInstance(result, Figure)


    @patch('src.visualization.charts.base.load_data')
    def test_visualize_invalid_gender_filter(self, mock_load):
        """
        Test `visualize_survey_responses` with an invalid gender filter.

        - Mocks data loading to return sample survey data.
        - Ensures function returns None when provided with an invalid gender.
        """
        # Configure the mock to return sample data.
        mock_load.return_value = self.sample_data

        # Execute the function under test with an invalid gender filter.
        result = visualize_survey_responses(
            'SC1',
            pie_chart_by_gender=True,
            gender_filter='Invalid'
        )

        # Assert that the function returns None.
        self.assertIsNone(result)


    @patch('src.visualization.charts.base.load_data')
    def test_visualize_missing_column(self, mock_load):
        """
        Test `visualize_survey_responses` when required columns are missing.

        - Removes 'Q2_GENDER' from sample data.
        - Ensures function returns None when gender distinction is requested but missing.
        """
        # Configure the mock to return sample data without the 'Q2_GENDER' column.
        mock_load.return_value = self.sample_data.drop(columns=['Q2_GENDER'])

        # Execute the function under test.
        result = visualize_survey_responses('SC1', distinction_by_gender=True)

        # Assert that the function returns None.
        self.assertIsNone(result)

    # Tests for build_question_selector()
    def test_build_selector_success(self):
        """
        Test successful creation of a question selector dropdown.

        - Ensures `build_question_selector` returns a `QComboBox` instance.
        - Verifies that the dropdown is correctly populated with questions.
        """
        # Create a real parent widget for the combobox.
        parent = QWidget()

        # Create a mock callback function.
        mock_callback = MagicMock()

        # Execute the function under test.
        result = build_question_selector(parent, mock_callback)

        # Assert that the result is a QComboBox.
        self.assertIsInstance(result, QComboBox)

        # Assert that the combobox is populated with the correct number of questions.
        self.assertEqual(result.count(), len(questions))

        # Clean up the parent widget.
        parent.deleteLater()

    def test_build_selector_invalid_parent(self):
        """
        Test `build_question_selector` with an invalid parent widget.

        - Ensures function returns None when given a `None` parent.
        """
        # Execute the function under test with an invalid parent.
        result = build_question_selector(None, lambda: None)

        # Assert that the function returns None.
        self.assertIsNone(result)

    def test_build_selector_invalid_callback(self):
        """
        Test `build_question_selector` with an invalid callback.

        - Ensures function returns None when provided with a non-callable callback.
        """
        # Create a real parent widget.
        parent = QWidget()

        # Execute the function under test with an invalid callback.
        result = build_question_selector(parent, "not callable")

        # Assert that the function returns None.
        self.assertIsNone(result)

        # Clean up the parent widget.
        parent.deleteLater()

    def test_build_selector_population(self):
        """
        Test question selector population from `questions` dictionary.

        - Mocks the `questions` dictionary.
        - Ensures the dropdown contains the correct number of items.
        """
        # Create real parent widget
        parent = QWidget()

        # Patch the actual questions used in the controller.
        with patch('src.visualization.charts.base.questions',
                   {'Q1': 'Question 1'}):
            # Execute the function under test.
            result = build_question_selector(parent, MagicMock())

            # Assert that the combobox contains one item.
            self.assertEqual(result.count(), 1)

            # Assert that the item text matches the expected value.
            self.assertEqual(result.itemText(0), 'Question 1')

        # Clean up the parent widget.
        parent.deleteLater()

    # Error Handling Tests

    @patch('src.visualization.charts.base.load_data')
    def test_visualize_data_load_failure(self, mock_load):
        """
        Test `visualize_survey_responses` when data loading fails.

        - Mocks `load_data` to return None.
        - Ensures the function returns None when data loading fails.
        """
        # Configure the mock to return None.
        mock_load.return_value = None

        # Execute the function under test.
        result = visualize_survey_responses('SC1')

        # Assert that the function returns None.
        self.assertIsNone(result)

    @patch('src.visualization.charts.base.load_data')
    @patch('src.visualization.charts.base.create_bar_chart_general')
    def test_unexpected_error_handling(self, mock_chart, mock_load):
        """
        Test `visualize_survey_responses` error handling for unexpected exceptions.

        - Mocks `load_data` to return sample data.
        - Simulates an exception in `create_bar_chart_general`.
        - Ensures function gracefully handles errors and returns None.
        """
        # Mock the data loading to return sample data
        mock_load.return_value = self.sample_data

        # Simulate an unexpected error during chart creation
        mock_chart.side_effect = Exception("Test error")

        # Call the function and verify the result
        result = visualize_survey_responses('SC1')

        # Verify that the mock was called.
        mock_chart.assert_called_once()

        # Ensure the function returned None due to the error
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()