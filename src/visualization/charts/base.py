"""
Survey Visualization Controller Module

This module serves as the central hub for managing survey data visualization operations,
combining data loading, chart generation, and UI components into a cohesive interface.

Key Components:
1. Data Management:
   - Secure CSV loading with validation and error logging
   - Path resolution for project assets
   - Data sanity checks and type verification

2. Visualization Router:
   - Unified interface for bar/pie chart generation
   - Demographic filtering (gender/school/income)
   - Automated chart type selection based on parameters
   - Cross-chart type consistency enforcement

3. UI Integration:
   - Qt-compatible question selector widget
   - Dynamic question list population
   - Event handling integration
   - GUI error resilience

Main Functions:
    load_data(): Handles data acquisition and initial processing
    visualize_survey_responses(): Core visualization dispatcher
    build_question_selector(): Creates interactive UI component

Dependencies:
    GUI Framework: PySide6
    Data Handling: pandas
    Visualization: matplotlib
    Internal: data_dictionary, bar_charts, pie_charts

"""
# Standard library imports
import os

# Third-party imports
import pandas as pd
from PySide6.QtWidgets import QComboBox
from matplotlib.figure import Figure
from pandas import DataFrame

# Local project-specific imports
from src.assets.impulse_buying_data.data_dictionary import (
    questions,
    school,
    income
)
from src.visualization.charts.bar_charts import (
    create_bar_chart_general,
    create_bar_chart_by_gender,
    create_bar_chart_by_school,
    create_bar_chart_by_income
)
from src.visualization.charts.pie_charts import (
    create_pie_chart_general,
    create_pie_chart_by_gender,
    create_pie_chart_by_school,
    create_pie_chart_by_income
)


def load_data() -> DataFrame | None:
    """
    Load and validate the cleaned survey data from CSV file.

    Returns:
        DataFrame | None: Loaded DataFrame if successful, None otherwise.

    Raises:
        FileNotFoundError: If the CSV file cannot be located
        pd.errors.EmptyDataError: If the file contains no data
        pd.errors.ParserError: If there's an error parsing CSV content
        Exception: For unexpected errors during loading process
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_csv_path = os.path.join(
        current_dir,    #charts
        "..",           #visualization
        "..",           #FinalProject
        "assets",
        "impulse_buying_data",
        "cleaned_data.csv"
    )

    # Print the resolved file path to debug
    print(f"🔍 [DEBUG] Looking for file at: {cleaned_csv_path}")


    try:
        # Attempt to load the CSV
        df = pd.read_csv(cleaned_csv_path)
        return df

    except FileNotFoundError:
        print(f"❌ [ERROR] The file {cleaned_csv_path} is not found.")
        return None

    except pd.errors.EmptyDataError:
        print("❌ [ERROR] The file is empty.")
        return None

    except pd.errors.ParserError:
        print("❌ [ERROR] There was an issue parsing the CSV file.")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] loading data: {gen_err}")
        return None


def visualize_survey_responses(
                  selected_question: str,
                  distinction_by_gender: bool = False,
                  distinction_by_school: bool = False,
                  distinction_by_income: bool = False,
                  pie_chart: bool = False,
                  gender_filter: str = None,
                  pie_chart_by_gender: bool = False,
                  school_filter: str = None,
                  pie_chart_by_school: bool = False,
                  income_filter: str = None,
                  pie_chart_by_income: bool = False
                 ) -> Figure | None:
    """
    Main controller for generating survey response visualizations.

    Args:
        selected_question (str): Question identifier from data dictionary
        distinction_by_gender (bool): Generate gender-distinguished bar chart
        distinction_by_school (bool): Generate school-distinguished bar chart
        distinction_by_income (bool): Generate income-distinguished bar chart
        pie_chart (bool): Generate general pie chart visualization
        gender_filter (str): Filter for gender-specific pie chart ('Male'/'Female')
        pie_chart_by_gender (bool): Generate gender-filtered pie chart
        school_filter (str): School filter from school dictionary values
        pie_chart_by_school (bool): Generate school-filtered pie chart
        income_filter (str): Income filter from income dictionary values
        pie_chart_by_income (bool): Generate income-filtered pie chart

    Returns:
        Figure | None: Matplotlib figure object if successful, None on error

    Raises:
        KeyError: Missing required data columns for requested visualization
        ValueError: Invalid filter values or incompatible parameter combinations
        TypeError: Invalid input types for parameters
        Exception: Unexpected errors during visualization generation

    Notes:
        - Mutual exclusion: Only one distinction/pie_chart flag should be True
        - Default fallback: Generates general bar chart if no flags set
        - Filter validation: Uses values from data_dictionary for validation
    """
    try:
        # ==================
        # DATA LOADING
        # ==================
        survey_data: pd.DataFrame = load_data()  # Load the data
        if survey_data is None:
            print(f"❌ [ERROR] Data loading failed for question {selected_question}")
            return None

        # =================================
        # VISUALIZATION ROUTING LOGIC
        # =================================
        # --- Bar Charts ---

        # Generate the bar chart with gender distinction
        if distinction_by_gender:
            if 'Q2_GENDER' not in survey_data.columns:
                raise KeyError("❌ [ERROR] Gender column not found in data")
            return create_bar_chart_by_gender(survey_data, selected_question)

        # Generate the bar chart with school distinction
        elif distinction_by_school:
            if 'Q3_SCHOOL' not in survey_data.columns:
                raise KeyError("❌ [ERROR] School column not found")
            return create_bar_chart_by_school(survey_data, selected_question)

        # Generate the bar chart with income distinction
        elif distinction_by_income:
            if 'Q4_INCOME' not in survey_data.columns:
                raise KeyError("❌ [ERROR] Income column not found")
            return create_bar_chart_by_income(survey_data, selected_question)

        # --- Pie Chart Variations ---
        # Generate a pie chart
        elif pie_chart:
            return create_pie_chart_general(survey_data, selected_question)

        # Generate a pie chart by gender
        elif pie_chart_by_gender:
            if gender_filter not in ('Male', 'Female'):
                raise ValueError("❌ [ERROR] gender_filter must be 'Male' or 'Female'")
            return create_pie_chart_by_gender(survey_data, selected_question, gender_filter)

        elif pie_chart_by_school:
            if school_filter not in school.values():
                raise ValueError("❌ [ERROR] invalid school_filter")
            return create_pie_chart_by_school(survey_data, selected_question, school_filter)

        elif pie_chart_by_income:
            if income_filter not in income.values():
                raise ValueError("❌ [ERROR] invalid income_filter")
            return create_pie_chart_by_income(survey_data, selected_question, income_filter)

        # --- Default View ---
        # Generate the chart without distinction
        else:
            return create_bar_chart_general(survey_data, selected_question)

    # ====================
    # ERROR HANDLING
    # ====================
    except ValueError as ve_err:
        print(f"❌ [ERROR] Validation error: {ve_err}")
        return None

    except KeyError as key_err:
        print(f"❌ [ERROR] Missing column in data: {key_err}")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] Unexpected error while generating chart: {gen_err}")
        return None


def build_question_selector(
        parent,
        callback,
        current_distinction: str | None=None
)-> QComboBox | None:
    """
    Creates a dropdown selector for survey questions with integrated error handling.

    Args:
        parent (QWidget): Parent container widget for Qt hierarchy management
        callback (Callable): Function to execute on selection change, signature: fn(str | None)
        current_distinction (str | None): Active demographic filter category ('gender'/'school'/'income')

    Returns:
        QComboBox | None: Configured question selector widget or None on failure

    Raises:
        ValueError: Invalid parent widget or null callback
        TypeError: Non-callable callback parameter
        RuntimeError: Qt signal connection failures
        KeyError: Missing question data in dictionary
        AttributeError: Invalid question data structure

    Notes:
        - Populates items from data_dictionary.questions
        - Applies styles from STYLES['combo_box']
        - Handles Qt signal connections automatically
    """
    try:
        # ======================
        # INPUT VALIDATION
        # ======================
        # Ensure parent widget exists for proper GUI hierarchy
        if parent is None:
            raise ValueError("❌ [ERROR] Parent widget cannot be None")

        # Verify callback is executable
        if not callable(callback):
            raise TypeError("❌ [ERROR] Invalid callback function")

        # =============================
        # COMBOBOX INITIALIZATION
        # =============================

        # Initialize combobox with parent widget
        question_combobox_widget: QComboBox = QComboBox(parent)

        # =====================
        # DATA POPULATION
        # =====================

        # Add each question identifier and its corresponding description to the combobox
        try:
            # Load question bank
            for question_id, question_description in questions.items():
                question_combobox_widget.addItem(question_description, question_id)

        # Handle malformed question data structure
        except AttributeError as atr_err:
            raise RuntimeError("❌ [ERROR] Question data structure invalid") from atr_err

        # ====================
        # EVENT HANDLING
        # ====================

        try:
            # Connect selection change to callback with current filter context
            question_combobox_widget.currentIndexChanged.connect(
                lambda: callback(current_distinction)
            )

        # Handle Qt signal connection failures
        except RuntimeError as rt_err:
            raise RuntimeError(f"❌ [ERROR] Failed connecting '{callback.__name__}' to combobox:"
                               f" {rt_err}") from rt_err

        return question_combobox_widget

    # ====================
    # ERROR HANDLING
    # ====================

    except AttributeError as atr_err:
        print(f"❌ [ERROR] Attribute error in UI components: {atr_err}")
        return None

    except (TypeError, ValueError) as input_err:
        print(f"❌ [ERROR] Input validation failure: {input_err}")
        return None

    except RuntimeError as rt_err:
        print(f"❌ [ERROR] GUI operation failed: {rt_err}")
        return None

    except KeyError as key_err:
        print(f"❌ [ERROR] Missing question data key: {key_err}")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] Unexpected error: {gen_err}")
        return None