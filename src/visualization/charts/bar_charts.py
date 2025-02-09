"""
Survey Data Visualization Module - Bar Chart Generator

This module provides a comprehensive toolkit for creating standardized bar chart
visualizations from survey response data, featuring demographic segmentation and
advanced styling capabilities.

Key Features:
- Demographic analysis by gender, school affiliation, and income brackets
- Automated data validation and type checking
- Dynamic response categorization and ordering
- Integrated null value handling with warning system
- Publication-ready styling with corporate branding

Main Functions:
    create_bar_chart_general: Base tests_visualization for response distributions
    create_bar_chart_by_gender: Gender-comparative analysis
    create_bar_chart_by_school: School-based response breakdown
    create_bar_chart_by_income: Income-level specific tests_visualization

Dependencies:
    Core: pandas, matplotlib, seaborn
    Local: data_dictionary (questions, answers, gender, school, income)

Customization Parameters:
    - category_order: Override default response ordering
    - figsize: Adjust dimensions (width, height in inches)
    - palette: Custom color schemes via seaborn palettes
    - label_rotation: X-axis label rotation (default: 30°)

"""
# Standard library imports
import textwrap

# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from pandas import DataFrame

# Local project-specific imports
from src.assets.impulse_buying_data.data_dictionary import (
    questions,
    answers,
    gender,
    school,
    income
)
from src.styles.styles import STYLES


# ======================
# MODULE CONSTANTS
# ======================
DEFAULT_CATEGORY_ORDER = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']
DEFAULT_FIGSIZE = (8, 6)        # Default width and height of the figure
SCHOOL_FIGSIZE = (10, 6)        # Width and height of the school figure


def create_bar_chart_general(
        df: DataFrame,
        selected_question: str,
        category_order: list[str] | None = None,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = STYLES["chart"]["palettes"]["general"]
) -> plt.Figure | None:
    """
    Generates a bar chart for a selected survey question with integrated error handling.
    Args:
        df (DataFrame): Input DataFrame containing survey data
        selected_question (str): Column name of the question to visualize
        category_order (list[str] | None): Custom order for response categories (optional)
        figsize (tuple[int, int]): Chart dimensions (width, height)
        palette (str): Seaborn color palette name

    Returns:
        matplotlib.figure.Figure | None: Generated bar chart or None on failure

    Raises:
        ValueError: Invalid DataFrame or empty input
        KeyError: Missing selected question or required columns in DataFrame
        TypeError: Incorrect type for selected_question
        Exception: Unexpected errors during execution

    Notes:
        - Maps responses using the `answers` dictionary
        - Supports custom category ordering
        - Handles null values and excludes them from tests_visualization
        - Adds value labels on top of bars for clarity
    """
    try:
        # ======================
        # INPUT VALIDATION
        # ======================

        # Check if DataFrame exists and is proper type
        if df is None or not isinstance(df, DataFrame):
            raise ValueError("❌ [ERROR] Input data is not a valid DataFrame.")

        # Check for empty DataFrame
        if df.empty:
            raise ValueError("❌ [ERROR] Input DataFrame is empty.")

        # Validate the selected question
        if not isinstance(selected_question, str):
            raise TypeError("❌ [ERROR] Selected question must be a string.")

        # Verify question exists in DataFrame columns
        if selected_question not in df.columns:
            raise KeyError(f"❌ [ERROR] The question '{selected_question}' is not found"
                           f" in the DataFrame columns.")

        # ======================
        # DATA PROCESSING
        # ======================

        # Map the answers using the `answers` dictionary
        mapped_answers_df: DataFrame = pd.DataFrame(
            {selected_question: df[selected_question].map(answers)}
        )

        # Check for null values in the mapped answers
        if mapped_answers_df[selected_question].isnull().any():
            print(f"⚠️ [WARNING] Null values found for the question '{selected_question}'."
                  f" These will be excluded.")

        # Define the order of the categories
        default_order: list[str] = DEFAULT_CATEGORY_ORDER
        category_order = category_order or default_order # Use custom order if provided

        # ======================
        # DATA ANALYSIS
        # ======================

        # Count the number of answers for each category
        response_counts: pd.Series = mapped_answers_df[selected_question].value_counts()

        # Reindex the categories according to the defined order and fill missing values with 0
        response_counts = response_counts.reindex(category_order, fill_value=0)

        # Check if there are no valid responses
        if response_counts.sum() == 0:
            raise ValueError(f"❌ [ERROR] No valid responses found for the question"
                             f" '{selected_question}'.")

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize figure
        figure, axis = plt.subplots(figsize=figsize)

        # Create Seaborn barplot
        axis = sns.barplot(
            x=response_counts.index,                # x-axis: Response categories (index of counts)
            y=response_counts.values,                       # y_axis: Count values
            palette=palette,                                # Color scheme from input parameter
            edgecolor=STYLES["chart"]["bar"]["edgecolor"],  # White borders between bars
            hue=response_counts.index                       # Color differentiation by category
        )

        # Add values on top of the bars
        for bar in axis.patches:
            value: int = int(bar.get_height())      # Get the height of the bar (frequency)
            axis.text(
                bar.get_x() + bar.get_width() / 2,      # X position: Center of the bar
                bar.get_height() - 0.1,                 # Y position: Slightly below the top of the bar
                f'{value}',                          # Text to display (the count)
                ha='center',                            # Horizontal alignment: Center
                va='bottom',                            # Vertical alignment: Bottom
                color=STYLES["chart"]["bar"]["color"],              # Text color
                fontsize=STYLES["chart"]["bar"]["fontsize"],        # Font size
                fontweight=STYLES["chart"]["bar"]["fontweight"]     # Font weight
            )

        # ======================
        # STYLING
        # ======================

        # Create full title string combining dictionary lookup and question ID
        question_title: str = (questions.get(selected_question, selected_question) +
                               f" ({selected_question})")

        # Wrap long titles to 40 character width
        wrapped_title: str = textwrap.fill(question_title, width=40)

        # Apply title styling
        plt.title(wrapped_title, **STYLES["chart"]["title"])

        # Axis labels
        plt.xlabel('Degree of agreement/disagreement', **STYLES["chart"]["axis_labels"])
        plt.ylabel('Number of Answers', **STYLES["chart"]["axis_labels"])

        # X-axis rotation for label readability
        plt.xticks(**STYLES["chart"]["x_ticks"])

        # Set y-axis ticks at 25-unit intervals
        max_y: int = response_counts.values.max()   # Find the highest bar value
        # From 0 to max+25 in steps of 25
        plt.yticks(range(0, max_y + 25, 25), **STYLES["chart"]["y_ticks"])

        # Add horizontal grid lines for easier value estimation
        plt.grid(**STYLES["chart"]["grid"])

        # Enhance chart border visibility
        for spine in axis.spines.values():
            spine.set_linewidth(STYLES["chart"]["spines"]["linewidth"])

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Display the chart
        return figure

    # ======================
    # ERROR HANDLING
    # ======================

    except ValueError as val_err:
        print(f"❌ [ERROR] {val_err}")
        return None

    except KeyError as key_err:
        print(f"❌ [ERROR] {key_err}")
        return None

    except TypeError as type_err:
        print(f"❌ [ERROR] {type_err}")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")
        return None


def create_bar_chart_by_gender(
        df: pd.DataFrame,
        selected_question: str,
        category_order: list[str] | None = None,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = STYLES["chart"]["palettes"]["gender"]
) -> plt.Figure | None:
    """
    Generates a gender-distinguished bar chart for a selected survey question.

    Args:
        df (pd.DataFrame): Input DataFrame containing survey data
        selected_question (str): Column name of the question to visualize
        category_order (list[str] | None): Custom order for response categories (optional)
        figsize (tuple[int, int]): Chart dimensions (width, height)
        palette (list[str]): Color palette for gender distinction (pink for female, blue for male)

    Returns:
        matplotlib.figure.Figure | None: Generated bar chart or None on failure

    Raises:
        ValueError: Invalid DataFrame or empty input
        KeyError: Missing selected question or required columns in DataFrame
        TypeError: Incorrect type for selected_question
        Exception: Unexpected errors during execution

    Notes:
        - Maps responses using the `answers` and `gender` dictionaries
        - Groups data by gender for tests_visualization
        - Supports custom category ordering
        - Adds value labels on top of bars for clarity
    """
    try:
        # ======================
        # INPUT VALIDATION
        # ======================
        # Validate input DataFrame
        if df is None or not isinstance(df, DataFrame):
            raise ValueError("❌ [ERROR] Input data is not a valid DataFrame.")

        # Check for empty DataFrame
        if df.empty:
            raise ValueError("❌ [ERROR] Input DataFrame is empty.")

        # Ensure the selected question is a string
        if not isinstance(selected_question, str):
            raise TypeError("❌ [ERROR] Selected question must be a string.")

        # Verify question exists in DataFrame columns
        if selected_question not in df.columns:
            raise KeyError(f"❌ [ERROR] The question '{selected_question}' is not found"
                           f" in the DataFrame columns.")

        # Check if required columns are present
        required_columns = [selected_question, 'Q2_GENDER']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise KeyError(f"❌ [ERROR] Missing columns: {', '.join(missing_cols)}")

        # ======================
        # DATA PROCESSING
        # ======================
        # Create a clean copy of the DataFrame with only necessary columns
        processed_df = df[[selected_question, 'Q2_GENDER']].copy()

        # Map values using predefined dictionaries (answers and gender mapping)
        processed_df[selected_question] = processed_df[selected_question].map(answers)
        processed_df['Q2_GENDER'] = processed_df['Q2_GENDER'].map(gender)

        # Check for null values in the mapped answers
        if processed_df[selected_question].isnull().any():
            print(f"⚠️ [WARNING] Null values found for the question '{selected_question}'."
                  f" These will be excluded.")

        # --- CATEGORY ORDER HANDLING ---
        # Set default response order if not provided
        category_order: list[str] = category_order or DEFAULT_CATEGORY_ORDER

        # Ensure the question column is treated as a categorical variable with the specified order
        processed_df[selected_question] = pd.Categorical(
            processed_df[selected_question],
            categories=category_order,
            ordered=True
        )

        # ======================
        # DATA ANALYSIS
        # ======================

        # --- DATA RESHAPING ---
        # Count the number of answers for each category, grouped by gender
        gender_count_data = (processed_df
                      .groupby(['Q2_GENDER', selected_question], observed=False)
                      .size()
                      .reset_index(name='counts'))

        # Check if no data is available for the selected question
        if gender_count_data.empty:
            print(f"❌ [ERROR] No responses were found for the question {selected_question}.")
            return

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        plt.figure(figsize=figsize)

        # Create grouped bar plot using Seaborn
        axis = sns.barplot(
            x=selected_question,        # X-axis will be the selected question
            y='counts',                 # Y-axis will be the count of answers
            hue='Q2_GENDER',            # Color bars by gender
            data=gender_count_data,     # Data to plot
            palette=palette,            # Set the color palette
            edgecolor=STYLES["chart"]["bar"]["edgecolor"],      # Set the bar edge color to white
            order=category_order        # Order the categories as specified
        )

        # --- VALUE LABELS ---
        # Add value labels on top of each bar
        for bar in axis.patches:
            axis.text(
                bar.get_x() + bar.get_width() / 2,      # X position: Center of the bar
                bar.get_height() - 0.1,                 # Y position: Slightly below the top of the bar
                f'{int(bar.get_height())}',          # Display the count value
                ha='center',                            # Horizontal alignment: Center
                va='bottom',                            # Vertical alignment: Bottom
                color=STYLES["chart"]["bar"]["color"],              # Text color
                fontsize=STYLES["chart"]["bar"]["fontsize"],        # Font size
                fontweight=STYLES["chart"]["bar"]["fontweight"]     # Font weight
            )

        # ======================
        # STYLING
        # ======================
        # Title and labels
        question_title: str = (f"{questions.get(selected_question, selected_question)}"
                          f"\n({selected_question})")

        plt.title(textwrap.fill(question_title, width=40), **STYLES["chart"]["title"])

        plt.xlabel('Degree of agreement/disagreement', **STYLES["chart"]["axis_labels"])
        plt.ylabel('Number of Answers', **STYLES["chart"]["axis_labels"])

        # Adjust the X-axis labels to be centered
        plt.xticks(**STYLES["chart"]["x_ticks"])

        # Adjust the Y-axis so that the ticks are every 25 units
        max_y: int = gender_count_data['counts'].max()      # Find the highest bar value
        # From 0 to max+25 in steps of 25
        plt.yticks(range(0, max_y + 25, 25), **STYLES["chart"]["y_ticks"])

        # Add grid lines to improve readability
        plt.grid(**STYLES["chart"]["grid"])

        # Legend and borders
        axis.legend(title='Gender', frameon=True)
        for spine in axis.spines.values():
            spine.set_linewidth(STYLES["chart"]["spines"]["linewidth"])

        # Adjust space for the title
        plt.tight_layout()

        # Display the chart
        return plt.gcf()

    # ======================
    # ERROR HANDLING
    # ======================

    except ValueError as val_err:
        print(f"❌ [ERROR] {val_err}")
        return None

    except KeyError as key_err:
        print(f"❌ [ERROR] {key_err}")
        return None

    except TypeError as type_err:
        print(f"❌ [ERROR] {type_err}")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")
        return None


def create_bar_chart_by_school(
        df: DataFrame,
        selected_question: str,
        category_order: list[str] | None = None,
        figsize: tuple[int, int] = SCHOOL_FIGSIZE,
        palette: str = STYLES["chart"]["palettes"]["school"]
) -> Figure | None:
    """
    Generates a school-distinguished bar chart for a selected survey question.

    Args:
        df (DataFrame): Input DataFrame containing survey data
        selected_question (str): Column name of the question to visualize
        category_order (list[str] | None): Custom order for response categories (optional)
        figsize (tuple[int, int]): Chart dimensions (width, height)
        palette (str): Seaborn color palette name

    Returns:
        matplotlib.figure.Figure | None: Generated bar chart or None on failure

    Raises:
        ValueError: Invalid DataFrame or empty input
        KeyError: Missing selected question or required columns in DataFrame
        TypeError: Incorrect type for selected_question
        Exception: Unexpected errors during execution

    Notes:
        - Maps responses using the `answers` and `school` dictionaries
        - Groups data by school for tests_visualization
        - Supports custom category ordering
        - Adds value labels on top of bars for clarity
    """
    try:
        # ======================
        # INPUT VALIDATION
        # ======================
        # Validate input DataFrame
        if df is None or not isinstance(df, DataFrame):
            raise ValueError("❌ [ERROR] Input data is not a valid DataFrame.")

        # Check for empty DataFrame
        if df.empty:
            raise ValueError("❌ [ERROR] Input DataFrame is empty.")

        # Ensure the selected question is a string
        if not isinstance(selected_question, str):
            raise TypeError("❌ [ERROR] Selected question must be a string.")

        # Verify question exists in DataFrame columns
        if selected_question not in df.columns:
            raise KeyError(f"❌ [ERROR] The question '{selected_question}' is not found"
                           f" in the DataFrame columns.")

        # Check if required columns are present
        required_columns = [selected_question, 'Q3_SCHOOL']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise KeyError(f"❌ [ERROR] Missing columns: {', '.join(missing_cols)}")

        # ======================
        # DATA PROCESSING
        # ======================
        # Create a clean copy of the DataFrame with only necessary columns
        processed_df = df[[selected_question, 'Q3_SCHOOL']].copy()

        # Map values using predefined dictionaries (answers and school mapping)
        processed_df['Q3_SCHOOL'] = processed_df['Q3_SCHOOL'].map(school)
        processed_df[selected_question] = processed_df[selected_question].map(answers)

        # Check for null values in the mapped answers
        if processed_df[selected_question].isnull().any():
            print(f"⚠️ [WARNING] Null values found in '{selected_question}'. Excluded.")

        # --- CATEGORY ORDER HANDLING ---
        # Set default response order if not provided
        category_order: list[str] = category_order or DEFAULT_CATEGORY_ORDER

        # Ensure the question column is treated as a categorical variable with the specified order
        processed_df[selected_question] = pd.Categorical(
            processed_df[selected_question],
            categories=category_order,
            ordered=True
        )

        # ======================
        # DATA ANALYSIS
        # ======================

        # --- DATA RESHAPING ---
        # Count the number of answers for each category, grouped by school
        school_count_data = (processed_df
                             .groupby(['Q3_SCHOOL', selected_question], observed=False)
                             .size()
                             .reset_index(name='counts'))

        # Check if no data is available for the selected question
        if school_count_data.empty:
            print(f"❌ [ERROR] No responses were found for the question {selected_question}.")
            return

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        plt.figure(figsize=figsize)

        # Create grouped bar plot using Seaborn
        axis = sns.barplot(
            x=selected_question,        # X-axis will be the selected question
            y='counts',                 # Y-axis will be the count of answers
            hue='Q3_SCHOOL',            # Color bars by school
            data=school_count_data,     # Data to plot
            palette=palette,            # Set the color palette
            edgecolor=STYLES["chart"]["bar"]["edgecolor"],      # Set the bar edge color to white
            order=category_order        # Order the categories as specified
        )

        # --- VALUE LABELS ---
        # Add value labels on top of each bar
        for bar in axis.patches:
            axis.text(
                bar.get_x() + bar.get_width() / 2,      # X position: Center of the bar
                bar.get_height() - 0.1,                 # Y position: Slightly below the top of the bar
                f'{int(bar.get_height())}',          # Display the count value
                ha='center',                            # Horizontal alignment: Center
                va='bottom',                            # Vertical alignment: Bottom
                color=STYLES["chart"]["bar"]["color"],              # Text color
                fontsize=STYLES["chart"]["bar"]["fontsize"],        # Font size
                fontweight=STYLES["chart"]["bar"]["fontweight"]     # Font weight
            )

        # ======================
        # STYLING
        # ======================
        # Title and labels
        question_title: str = (f"{questions.get(selected_question, selected_question)}"
                               f"\n({selected_question})")

        plt.title(textwrap.fill(question_title, width=40), **STYLES["chart"]["title"])

        plt.xlabel('Degree of agreement/disagreement', **STYLES["chart"]["axis_labels"])
        plt.ylabel('Number of Answers', **STYLES["chart"]["axis_labels"])

        # Adjust the X-axis labels to be centered
        plt.xticks(**STYLES["chart"]["x_ticks"])

        # Adjust the Y-axis so that the ticks are every 25 units
        max_y: int = school_count_data['counts'].max()      # Find the highest bar value
        # From 0 to max+25 in steps of 25
        plt.yticks(range(0, max_y + 25, 25), **STYLES["chart"]["y_ticks"])

        # Add grid lines to improve readability
        plt.grid(**STYLES["chart"]["grid"])

        # Legend and borders
        axis.legend(title='School', frameon=True)
        for spine in axis.spines.values():
            spine.set_linewidth(STYLES["chart"]["spines"]["linewidth"])

        # Adjust space for the title
        plt.tight_layout()

        # Display the chart
        return plt.gcf()

    # ======================
    # ERROR HANDLING
    # ======================

    except ValueError as val_err:
        print(f"❌ [ERROR] {val_err}")
        return None

    except KeyError as key_err:
        print(f"❌ [ERROR] {key_err}")
        return None

    except TypeError as type_err:
        print(f"❌ [ERROR] {type_err}")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")
        return None


def create_bar_chart_by_income(
        df: pd.DataFrame,
        selected_question: str,
        category_order: list[str] | None = None,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = STYLES["chart"]["palettes"]["income"]
) -> plt.Figure | None:
    """
    Generates an income-distinguished bar chart for a selected survey question.

    Args:
        df (pd.DataFrame): Input DataFrame containing survey data
        selected_question (str): Column name of the question to visualize
        category_order (list[str] | None): Custom order for response categories (optional)
        figsize (tuple[int, int]): Chart dimensions (width, height)
        palette (str): Seaborn color palette name

    Returns:
        matplotlib.figure.Figure | None: Generated bar chart or None on failure

    Raises:
        ValueError: Invalid DataFrame or empty input
        KeyError: Missing selected question or required columns in DataFrame
        TypeError: Incorrect type for selected_question
        Exception: Unexpected errors during execution

    Notes:
        - Maps responses using the `answers` and `income` dictionaries
        - Groups data by income level for tests_visualization
        - Supports custom category ordering
        - Adds value labels on top of bars for clarity
    """
    try:
        # ======================
        # INPUT VALIDATION
        # ======================
        # Validate input DataFrame
        if df is None or not isinstance(df, DataFrame):
            raise ValueError("❌ [ERROR] Input data is not a valid DataFrame.")

        # Check for empty DataFrame
        if df.empty:
            raise ValueError("❌ [ERROR] Input DataFrame is empty.")

        # Ensure the selected question is a string
        if not isinstance(selected_question, str):
            raise TypeError("❌ [ERROR] Selected question must be a string.")

        # Verify question exists in DataFrame columns
        if selected_question not in df.columns:
            raise KeyError(f"❌ [ERROR] The question '{selected_question}' is not found"
                           f" in the DataFrame columns.")

        # Check if required columns are present
        required_columns = [selected_question, 'Q4_INCOME']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise KeyError(f"❌ [ERROR] Missing columns: {', '.join(missing_cols)}")

        # ======================
        # DATA PROCESSING
        # ======================
        # Create a clean copy of the DataFrame with only necessary columns
        processed_df = df[[selected_question, 'Q4_INCOME']].copy()

        # Map values using predefined dictionaries (answers and income mapping)
        processed_df['Q4_INCOME'] = processed_df['Q4_INCOME'].map(income)
        processed_df[selected_question] = processed_df[selected_question].map(answers)

        # Check for null values in the mapped answers
        if processed_df[selected_question].isnull().any():
            print(f"⚠️ [WARNING] Null values found in '{selected_question}'. Excluded.")

        # --- CATEGORY ORDER HANDLING ---
        # Set default response order if not provided
        category_order: list[str] = category_order or DEFAULT_CATEGORY_ORDER

        # Ensure the question column is treated as a categorical variable with the specified order
        processed_df[selected_question] = pd.Categorical(
            processed_df[selected_question],
            categories=category_order,
            ordered=True
        )

        # ======================
        # DATA ANALYSIS
        # ======================

        # --- DATA RESHAPING ---
        # Count the number of answers for each category, grouped by school
        income_count_data = (processed_df
                             .groupby(['Q4_INCOME', selected_question], observed=False)
                             .size()
                             .reset_index(name='counts'))

        # Check if no data is available for the selected question
        if income_count_data.empty:
            print(f"❌ [ERROR] No responses were found for the question {selected_question}.")
            return

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        plt.figure(figsize=figsize)

        # Create grouped bar plot using Seaborn
        axis = sns.barplot(
            x=selected_question,        # X-axis will be the selected question
            y='counts',                 # Y-axis will be the count of answers
            hue='Q4_INCOME',            # Color bars by school
            data=income_count_data,     # Data to plot
            palette=palette,            # Set the color palette
            edgecolor=STYLES["chart"]["bar"]["edgecolor"],      # Set the bar edge color to white
            order=category_order        # Order the categories as specified
        )

        # --- VALUE LABELS ---
        # Add value labels on top of each bar
        for bar in axis.patches:
            axis.text(
                bar.get_x() + bar.get_width() / 2,      # X position: Center of the bar
                bar.get_height() - 0.1,                 # Y position: Slightly below the top of the bar
                f'{int(bar.get_height())}',          # Display the count value
                ha='center',                            # Horizontal alignment: Center
                va='bottom',                            # Vertical alignment: Bottom
                color=STYLES["chart"]["bar"]["color"],              # Text color
                fontsize=STYLES["chart"]["bar"]["fontsize"],        # Font size
                fontweight=STYLES["chart"]["bar"]["fontweight"]     # Font weight
            )

        # ======================
        # STYLING
        # ======================

        # Title and labels
        question_title: str = (f"{questions.get(selected_question, selected_question)}"
                               f"\n({selected_question})")

        plt.title(textwrap.fill(question_title, width=40), **STYLES["chart"]["title"])

        plt.xlabel('Degree of agreement/disagreement', **STYLES["chart"]["axis_labels"])
        plt.ylabel('Number of Answers', **STYLES["chart"]["axis_labels"])

        # Adjust the X-axis labels to be centered
        plt.xticks(**STYLES["chart"]["x_ticks"])

        # Adjust the Y-axis so that the ticks are every 25 units
        max_y: int = income_count_data['counts'].max()  # Find the highest bar value
        # From 0 to max+25 in steps of 25
        plt.yticks(range(0, max_y + 25, 25), **STYLES["chart"]["y_ticks"])

        # Add grid lines to improve readability
        plt.grid(**STYLES["chart"]["grid"])

        # Legend and borders
        axis.legend(title='Income', frameon=True)
        for spine in axis.spines.values():
            spine.set_linewidth(STYLES["chart"]["spines"]["linewidth"])

        # Adjust space for the title
        plt.tight_layout()

        # Display the chart
        return plt.gcf()

    # ======================
    # ERROR HANDLING
    # ======================

    except ValueError as val_err:
        print(f"❌ [ERROR] {val_err}")
        return None

    except KeyError as key_err:
        print(f"❌ [ERROR] {key_err}")
        return None

    except TypeError as type_err:
        print(f"❌ [ERROR] {type_err}")
        return None

    except Exception as gen_err:
        print(f"❌ [ERROR] An unexpected error occurred: {gen_err}")
        return None