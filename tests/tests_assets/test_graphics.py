"""
Unit tests for the `Graphics` module in the `FinalProject.assets.graphics` package.

This test suite verifies the correct functionality of various functions responsible
for loading and plotting data using the Pandas library and Matplotlib. Each function
is tested to ensure it behaves as expected under different conditions, including edge cases.

Key tests include:

- Data Loading:
    - `load_data`:
        - Verifies that the function correctly loads data from a CSV file, handling
          different scenarios like successful data loading, file not found errors,
          empty files, and parser errors.
        - Tests ensure that the function returns the expected DataFrame or `None`
          in case of errors.

- Plotting Functions:
    - `plot_question_data`:
        - Verifies the generation of a plot for a specified question, ensuring that
          the figure is correctly created for valid data and that an appropriate
          response occurs when an invalid question is requested.
    - `plot_question_data_by_gender`:
        - Ensures that the plot is correctly generated when distinguishing data by gender.
    - `plot_question_data_by_school`:
        - Verifies that the plot generation works when distinguishing data by school.
    - `plot_question_data_by_income`:
        - Ensures proper plot generation when distinguishing data by income.

- Pie Chart Creation:
    - `create_pie_chart`:
        - Verifies that a pie chart is correctly created from the given data.
    - `create_pie_chart_by_gender`:
        - Ensures that pie charts are generated correctly when distinguishing data by gender.

- Question Plot:
    - `question_plot`:
        - Tests the generation of a plot based on user-specified questions, with
          distinction options such as gender.
        - Verifies that the plot is generated and displayed correctly when the function
          is provided with valid data and a valid question.

Each test ensures that the individual components of the `Graphics` module are robust
and work correctly under various conditions, including normal, edge, and error cases.
"""
# Standard library imports
import unittest
from unittest.mock import patch

# Third-party imports
import pandas as pd

# Local project-specific imports
from FinalProject.assets.graphics import (
    load_data,
    plot_question_data,
    plot_question_data_by_gender,
    plot_question_data_by_school,
    plot_question_data_by_income,
    create_pie_chart,
    create_pie_chart_by_gender,
    question_plot,
)


class TestGraphics(unittest.TestCase):
    """
    Unit tests for the graphics-related functions in the `FinalProject.assets.graphics` module.

    This suite verifies the behavior and correctness of various functions related to data loading
    and visualization, including plotting question data, generating pie charts, and handling errors.

    It includes tests for the following functionalities:
    - `load_data`: Tests for successfully loading data, handling file not found errors, empty files, and parsing issues.
    - `plot_question_data`: Verifies the behavior of plotting data for a specific question.
    - `plot_question_data_by_gender`: Tests plotting data for a specific question, distinguished by gender.
    - `plot_question_data_by_school`: Tests plotting data for a specific question, distinguished by school.
    - `plot_question_data_by_income`: Tests plotting data for a specific question, distinguished by income.
    - `create_pie_chart`: Verifies the creation of pie charts based on question data.
    - `create_pie_chart_by_gender`: Verifies the creation of pie charts, distinguished by gender.
    - `question_plot`: Tests the overall question plotting functionality, with support for distinction by gender.

    Mocking is used to simulate data loading and external dependencies, ensuring a controlled test environment.
    """
    @patch("FinalProject.assets.graphics.pd.read_csv")
    def test_load_data_success(self, mock_read_csv) -> None:
        mock_df = pd.DataFrame({'A': [1, 2, 3]})
        mock_read_csv.return_value = mock_df
        df = load_data()
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (3, 1))

    @patch("FinalProject.assets.graphics.pd.read_csv")
    def test_load_data_file_not_found(self, mock_read_csv) -> None:
        mock_read_csv.side_effect = FileNotFoundError
        df = load_data()
        self.assertIsNone(df)

    @patch("FinalProject.assets.graphics.pd.read_csv")
    def test_load_data_empty_file(self, mock_read_csv) -> None:
        mock_read_csv.side_effect = pd.errors.EmptyDataError
        df = load_data()
        self.assertIsNone(df)

    @patch("FinalProject.assets.graphics.pd.read_csv")
    def test_load_data_parser_error(self, mock_read_csv) -> None:
        mock_read_csv.side_effect = pd.errors.ParserError
        df = load_data()
        self.assertIsNone(df)

    def test_plot_question_data(self) -> None:
        df = pd.DataFrame({
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = plot_question_data(df, 'Q1')
        self.assertIsNotNone(figure)

    def test_plot_question_data_invalid_question(self) -> None:
        df = pd.DataFrame({
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = plot_question_data(df, 'Q2')
        self.assertIsNone(figure)

    def test_plot_question_data_by_gender(self) -> None:
        df = pd.DataFrame({
            'Q2_GENDER': [1, 2, 1, 2, 1],
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = plot_question_data_by_gender(df, 'Q1')
        self.assertIsNotNone(figure)

    def test_plot_question_data_by_school(self) -> None:
        df = pd.DataFrame({
            'Q3_SCHOOL': [1, 2, 1, 2, 1],
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = plot_question_data_by_school(df, 'Q1')
        self.assertIsNotNone(figure)

    def test_plot_question_data_by_income(self) -> None:
        df = pd.DataFrame({
            'Q4_INCOME': [1, 2, 1, 2, 1],
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = plot_question_data_by_income(df, 'Q1')
        self.assertIsNotNone(figure)

    def test_create_pie_chart(self) -> None:
        df = pd.DataFrame({
            'Q3_SCHOOL': [1, 2, 1, 2, 1],
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = create_pie_chart(df, 'Q1')
        self.assertIsNotNone(figure)

    def test_create_pie_chart_by_gender(self) -> None:
        df = pd.DataFrame({
            'Q2_GENDER': [1, 2, 1, 2, 1],
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = create_pie_chart_by_gender(df, 'Q1')
        self.assertIsNotNone(figure)

    @patch("FinalProject.assets.graphics.load_data")
    def test_question_plot(self, mock_load_data) -> None:
        mock_load_data.return_value = pd.DataFrame({
            'Q2_GENDER': [1, 2, 1, 2, 1],
            'Q1': [1, 2, 3, 4, 5]
        })
        figure = question_plot('Q1', distinction_by_gender=True)
        self.assertIsNotNone(figure)

if __name__ == '__main__':
    unittest.main()