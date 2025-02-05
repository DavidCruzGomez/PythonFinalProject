"""
Survey Data Visualization Module - Pie Chart Generator

This module provides specialized functions for creating standardized pie chart
visualizations from impulse buying survey data. It enables analysis of response
distributions with demographic segmentation capabilities.

Key Features:
- Demographic segmentation by gender, school, and income
- Automated data validation and cleaning
- Consistent styling following corporate visual guidelines
- Dynamic aggregation of small response categories
- Cross-platform compatible figure output

Main Functions:
    create_pie_chart_general: Primary pie chart visualization for overall response distribution
    create_pie_chart_by_gender: Gender-segmented comparative analysis
    create_pie_chart_by_school: School-affiliation based breakdown
    create_pie_chart_by_income: Income-bracket specific visualization

Dependencies:
    Data Dictionaries: questions, answers, gender, school, income
    Libraries: matplotlib, seaborn, pandas

Customization Options:
    - figsize: Adjust chart dimensions (width, height in inches)
    - palette: Choose from seaborn color palettes
    - min_percentage: Set aggregation threshold (0-100)

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
DEFAULT_FIGSIZE = (6, 6)        # Default width and height of the figure
DEFAULT_MIN_PERCENTAGE = 3.0    #Minimum percentage threshold (0-100) for individual slices.

def create_pie_chart_general(
        df: pd.DataFrame,
        selected_question: str,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = "Set2",
        min_percentage: float = DEFAULT_MIN_PERCENTAGE
) -> Figure | None:
    """Generates a styled pie chart for survey response distribution.

    Visualizes response distribution for a selected survey question, aggregating
    small percentage categories into an 'Others' group for better readability.

    Args:
        df: Input DataFrame containing raw survey data
        selected_question: Column name identifier for the question to visualize
        figsize: Chart dimensions (width, height) in inches. Default: (6, 6)
        palette: Seaborn color palette name for slice coloring. Default: 'Set2'
        min_percentage: Minimum percentage threshold (0-100) for individual slices.
            Smaller values are grouped into 'Others'. Default: 3.0

    Returns:
        matplotlib.figure.Figure: Configured pie chart figure object
        None: If input validation fails or data processing error occurs

    Raises:
        ValueError: For invalid DataFrame input or empty data
        TypeError: For incorrect parameter types
        KeyError: If specified question column doesn't exist in DataFrame
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

        # ======================
        # DATA PROCESSING
        # ======================
        # Map the answers using the `answers` dictionary
        mapped_answers = df[selected_question].map(answers)

        # Count the number of answers for each category
        answer_counts: pd.Series = mapped_answers.value_counts()

        # Check if the answer_counts Series is empty
        if answer_counts.empty:
            raise ValueError(f"❌ [ERROR] No valid responses for '{selected_question}'.")

        # Filter small percentage categories into "Others"
        total = answer_counts.sum()
        filtered_labels = []
        filtered_sizes = []
        others_size = 0

        # Process each category to separate significant vs small percentages
        for label, size in answer_counts.items():
            percentage = (size / total) * 100
            if percentage >= min_percentage:
                filtered_labels.append(label)
                filtered_sizes.append(size)
            else:
                others_size += size # Aggregate small categories

        # Add "Others" category if small percentages exist
        if others_size > 0:
            filtered_labels.append("Others")
            filtered_sizes.append(others_size)

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        figure, axis = plt.subplots(figsize=figsize)

        # Create color palette
        colors = sns.color_palette(palette, len(filtered_sizes))

        # Explode the largest slice
        max_idx = filtered_sizes.index(max(filtered_sizes))
        explode: list[float] = [0.1 if i == max_idx else 0 for i in range(len(filtered_sizes))]

        # Generate pie chart
        wedges, texts, autotexts = axis.pie(
            filtered_sizes,
            labels=filtered_labels if len(filtered_labels) > 1 else None, # Hide label if only "Others"
            autopct=lambda p: f'{p:.1f}%' if p >= min_percentage else '', # percentage display
            startangle=90,                                          # Initial rotation angle
            colors=colors,                                          # Color scheme
            explode=explode,                                        # Slice explosion effect
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},    # Slice border styling
            pctdistance=0.85,                           # Adjusts the distance of the percentages
            textprops = {                                           # Text styling parameters
                'fontsize': 10,
                'fontweight': 'bold',
            }
        )

        # ======================
        # STYLING
        # ======================

        # Title and labels
        question_title: str = (questions.get(selected_question, selected_question) +
                               f" ({selected_question})"
                              )
        wrapped_title: str = textwrap.fill(question_title, width=40)

        # Apply title styling
        plt.title(wrapped_title, **STYLES["chart"]["title"])

        # Percentage label styling
        for autotext in autotexts:
            autotext.set_color('black')     # Set percentage text color
            autotext.set_fontsize(12)       # Adjust font size
            autotext.set_fontweight('bold') # Emphasize text

        # Category label styling
        for text in texts:
            text.set_fontsize(12)           # Label text size
            text.set_color('black')         # Label text color

        # Add legend if "Others" category exists
        if "Others" in filtered_labels:
            axis.legend(
                wedges,
                filtered_labels,
                title="Categories",         # Legend title
                loc="center left",          # Position
                bbox_to_anchor=(1, 0.5),    # Placement outside chart
                fontsize=10                 # Legend text size
            )

        # Display the chart
        plt.tight_layout()

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
        print(f"❌ [ERROR] Unexpected error: {gen_err}")
        return None


def create_pie_chart_by_gender(
        df: pd.DataFrame,
        selected_question: str,
        gender_filter: str = None,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = "Set2",
        min_percentage: float = DEFAULT_MIN_PERCENTAGE
) -> Figure | None:
    """Generates comparative pie charts segmented by gender demographics.

    Creates either a single filtered pie chart or side-by-side comparisons
    for male/female responses based on filter parameter.

    Args:
        df: Source DataFrame containing survey responses
        selected_question: Target question column to visualize
        gender_filter: Optional filter to show only 'Male' or 'Female' responses.
            Default: None shows both genders
        figsize: Output figure dimensions. Default: (6, 6)
        palette: Color scheme for visualization. Default: 'Set2'
        min_percentage: Threshold for individual slice visibility. Default: 3.0%

    Returns:
        matplotlib.figure.Figure: Multi-subplot figure for comparisons
        None: On validation errors or missing required columns

    Raises:
        ValueError: Invalid filter value or empty processed data
        TypeError: Selected_question is not a string
        KeyError: Missing required 'Q2_GENDER' column or question
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

        # Create a working copy with only necessary columns
        processed_df = df[['Q2_GENDER', selected_question]].copy()

        # Convert gender codes to labels
        processed_df['Q2_GENDER'] = processed_df['Q2_GENDER'].map(gender)

        # Convert answer codes to text labels
        processed_df[selected_question] = processed_df[selected_question].map(answers)

        # Apply gender filter if provided
        if gender_filter:
            if gender_filter not in ('Male', 'Female'):
                raise ValueError("❌ [ERROR] gender_filter must be 'Male' or 'Female'")
            processed_df = processed_df[processed_df['Q2_GENDER'] == gender_filter]

        # Group by gender and question, count responses
        grouped_data = (processed_df
                        .groupby(['Q2_GENDER', selected_question],observed=False)
                        .size()
                        .unstack(fill_value=0))

        # Check for empty data after processing
        if grouped_data.empty:
            raise ValueError(f"❌ [ERROR] No valid responses for '{selected_question}'")

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        figure, axes = plt.subplots(1, len(grouped_data.index), figsize=figsize)
        if len(grouped_data.index) == 1:
            axes = [axes]  # Ensure axes is iterable for single subplot

        # Generate pie chart for each gender
        for idx, (gender_category, answer_counts) in enumerate(grouped_data.iterrows()):
            axis = axes[idx] if len(grouped_data.index) > 1 else axes[0]

            # Filter small percentage categories into "Others"
            total = answer_counts.sum()
            filtered_labels = []
            filtered_sizes = []
            others_size = 0

            # Process each category to separate significant vs small percentages
            for label, size in answer_counts.items():
                percentage = (size / total) * 100
                if percentage >= min_percentage:
                    filtered_labels.append(label)
                    filtered_sizes.append(size)
                else:
                    others_size += size  # Aggregate small categories

            # Add "Others" category if small percentages exist
            if others_size > 0:
                filtered_labels.append("Others")
                filtered_sizes.append(others_size)

            # Create color palette
            colors = sns.color_palette(palette, len(filtered_sizes))

            # Explode the largest slice
            max_idx = filtered_sizes.index(max(filtered_sizes)) if filtered_sizes else 0
            explode = [0.1 if i == max_idx else 0 for i in range(len(filtered_sizes))]

            # Create pie chart
            wedges, texts, autotexts = axis.pie(
                filtered_sizes,
                labels=filtered_labels if len(filtered_labels) > 1 else None, # Hide label if only "Others"
                autopct=lambda p: f'{p:.1f}%' if p >= min_percentage else '', # percentage display
                startangle=90,                                          # Initial rotation angle
                colors=colors,                                          # Color scheme
                explode=explode,                                        # Slice explosion effect
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},    # Slice border styling
                pctdistance=0.85,                       # Adjusts the distance of the percentages
                textprops={                                             # Text styling parameters
                    'fontsize': 10,
                    'fontweight': 'bold'
                }
            )

        # ======================
        # STYLING
        # ======================

        # Title and labels
        question_title: str = (questions.get(selected_question, selected_question) +
                               f" ({selected_question})"
                               )
        wrapped_title: str = textwrap.fill(question_title, width=40)

        # Apply title styling
        figure.suptitle(
            wrapped_title,
            fontsize=18,
            fontweight='bold',
            color='navy'
        )

        # Add gender title below subplot
        axis.set_title(
            gender_category,    # Title text based on the gender category
            y=-0.15,            # Position the title slightly below the plot
            fontsize=14,
            fontweight='bold',
            color='navy'
        )

        # Percentage label styling
        for autotext in autotexts:
            autotext.set_color('black')     # Set percentage text color
            autotext.set_fontsize(12)       # Adjust font size
            autotext.set_fontweight('bold') # Emphasize text

        # Category label styling
        for text in texts:
            text.set_fontsize(12)   # Label text size
            text.set_color('black') # Label text color

        # Add legend if "Others" category exists
        if "Others" in filtered_labels:
            axis.legend(
                wedges,
                filtered_labels,
                title="Categories",         # Legend title
                loc="center left",          # Position
                bbox_to_anchor=(1, 0.5),    # Placement outside chart
                fontsize=10                 # Legend text size
            )

        # Display the chart
        plt.tight_layout()

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
        print(f"❌ [ERROR] Unexpected error: {gen_err}")
        return None

def create_pie_chart_by_school(
        df: pd.DataFrame,
        selected_question: str,
        school_filter: str = None,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = "Set2",
        min_percentage: float = DEFAULT_MIN_PERCENTAGE
) -> Figure | None:
    """Generates pie charts segmented by academic school affiliation.

    Creates either a single filtered pie chart or side-by-side comparisons
    for school responses based on filter parameter.

    Args:
        df: Source DataFrame containing survey responses
        selected_question: Target question column to visualize
        school_filter: Optional school name to isolate responses.
            Valid options: school dictionary values
            Default: None shows all schools
        figsize: Output figure dimensions. Default: (6, 6)
         palette: Color scheme for visualization. Default: 'Set2'
        min_percentage: Threshold for individual slice visibility. Default: 3.0%

    Returns:
        matplotlib.figure.Figure: Multi-subplot figure for comparisons
        None: On validation errors or missing required columns

    Raises:
        ValueError: Invalid filter value or empty processed data
        TypeError: Selected_question is not a string
        KeyError: Missing required 'Q3_SCHOOL' column or question
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

        # Create a working copy with only necessary columns
        processed_df = df[['Q3_SCHOOL', selected_question]].copy()

        # Map school codes to labels
        processed_df['Q3_SCHOOL'] = processed_df['Q3_SCHOOL'].map(school)

        # Convert answer codes to text labels
        processed_df[selected_question] = processed_df[selected_question].map(answers)

        # Apply school filter
        if school_filter:
            valid_schools = list(school.values())
            if school_filter not in valid_schools:
                raise ValueError(f"❌ [ERROR] Invalid school_filter. Valid options: {valid_schools}")
            processed_df = processed_df[processed_df['Q3_SCHOOL'] == school_filter]

        # Group by gender and question, count responses
        grouped_data = (processed_df
                        .groupby(['Q3_SCHOOL', selected_question], observed=False)
                        .size()
                        .unstack(fill_value=0))

        # Check for empty data after processing
        if grouped_data.empty:
            raise ValueError(f"❌ [ERROR] No valid responses for '{selected_question}'")

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        figure, axes = plt.subplots(1, len(grouped_data.index), figsize=figsize)
        if len(grouped_data.index) == 1:
            axes = [axes]   # Ensure axes is iterable for single subplot

        # Generate a pie chart for each school
        for idx, (school_category, answer_counts) in enumerate(grouped_data.iterrows()):
            axis = axes[idx] if len(grouped_data.index) > 1 else axes[0]

            # Filter small percentage categories into "Others"
            total = answer_counts.sum()
            filtered_labels = []
            filtered_sizes = []
            others_size = 0

            # Process each category to separate significant vs small percentages
            for label, size in answer_counts.items():
                percentage = (size / total) * 100
                if percentage >= min_percentage:
                    filtered_labels.append(label)
                    filtered_sizes.append(size)
                else:
                    others_size += size  # Aggregate small categories

            # Add "Others" category if small percentages exist
            if others_size > 0:
                filtered_labels.append("Others")
                filtered_sizes.append(others_size)

            # Create color palette
            colors = sns.color_palette(palette, len(filtered_sizes))

            # Explode the largest slice
            max_idx = filtered_sizes.index(max(filtered_sizes)) if filtered_sizes else 0
            explode = [0.1 if i == max_idx else 0 for i in range(len(filtered_sizes))]

            # Create pie chart
            wedges, texts, autotexts = axis.pie(
                filtered_sizes,
                labels=filtered_labels if len(filtered_labels) > 1 else None, # Hide label if only "Others"
                autopct=lambda p: f'{p:.1f}%' if p >= min_percentage else '', # percentage display
                startangle=90,                                          # Initial rotation angle
                colors=colors,                                          # Color scheme
                explode=explode,                                        # Slice explosion effect
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},    # Slice border styling
                pctdistance=0.85,                       # Adjusts the distance of the percentages
                textprops={                                             # Text styling parameters
                    'fontsize': 10,
                    'fontweight': 'bold'
                }
            )

        # ======================
        # STYLING
        # ======================

        # Title and labels
        question_title: str = (questions.get(selected_question, selected_question) +
                               f" ({selected_question})"
                               )
        wrapped_title: str = textwrap.fill(question_title, width=40)

        # Apply title styling
        figure.suptitle(
            wrapped_title,
            fontsize=18,
            fontweight='bold',
            color='navy'
        )

        # Add school title below subplot
        axis.set_title(
            school_category,    # Title text based on the school category
            y=-0.15,            # Position the title slightly below the plot
            fontsize=14,
            fontweight='bold',
            color='navy'
        )

        # Percentage label styling
        for autotext in autotexts:
            autotext.set_color('black')     # Set percentage text color
            autotext.set_fontsize(12)       # Adjust font size
            autotext.set_fontweight('bold') # Emphasize text

        # Category label styling
        for text in texts:
            text.set_fontsize(12)   # Label text size
            text.set_color('black') # Label text color

        # Add legend if "Others" category exists
        if "Others" in filtered_labels:
            axis.legend(
                wedges,
                filtered_labels,
                title="Categories",         # Legend title
                loc="center left",          # Position
                bbox_to_anchor=(1, 0.5),    # Placement outside chart
                fontsize=10                 # Legend text size
            )

        # Display the chart
        plt.tight_layout()

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
        print(f"❌ [ERROR] Unexpected error: {gen_err}")
        return None


def create_pie_chart_by_income(
        df: pd.DataFrame,
        selected_question: str,
        income_filter: str = None,
        figsize: tuple[int, int] = DEFAULT_FIGSIZE,
        palette: str = "Set2",
        min_percentage: float = DEFAULT_MIN_PERCENTAGE
) -> Figure | None:
    """Generates income-bracketed pie charts for response analysis.

    Creates either a single filtered pie chart or side-by-side comparisons
    for income responses based on filter parameter.

    Args:
        df: Source DataFrame containing survey responses
        selected_question: Target question column to visualize
        income_filter: Optional income bracket to isolate.
            Valid options: income dictionary values
            Default: None shows all income
        figsize: Output figure dimensions. Default: (6, 6)
         palette: Color scheme for visualization. Default: 'Set2'
        min_percentage: Threshold for individual slice visibility. Default: 3.0%

    Returns:
        matplotlib.figure.Figure: Income-segmented chart figure
        None: On validation failure or data errors

    Raises:
        ValueError: Invalid filter value or empty processed data
        TypeError: Selected_question is not a string
        KeyError: Missing required 'Q4_INCOME' column or question
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

        # Create a working copy with only necessary columns
        processed_df = df[['Q4_INCOME', selected_question]].copy()

        # Map income codes to labels
        processed_df['Q4_INCOME'] = processed_df['Q4_INCOME'].map(income)

        # Map answer codes to text labels
        processed_df[selected_question] = processed_df[selected_question].map(answers)

        # Apply income filter if provided
        if income_filter:
            valid_incomes = list(income.values())
            if income_filter not in valid_incomes:
                raise ValueError(f"❌ [ERROR] Invalid income_filter. Valid options: {valid_incomes}")
            processed_df = processed_df[processed_df['Q4_INCOME'] == income_filter]

        # Group data by income
        grouped_data = (processed_df
                        .groupby(['Q4_INCOME', selected_question],observed=False)
                        .size()
                        .unstack(fill_value=0))

        if grouped_data.empty:
            raise ValueError(f"❌ [ERROR] No valid responses for '{selected_question}'")

        # ======================
        # VISUALIZATION
        # ======================

        # Initialize the figure and axis for plotting
        figure, axes = plt.subplots(1, len(grouped_data.index), figsize=figsize)
        if len(grouped_data.index) == 1:
            axes = [axes]  # Ensure axes is iterable for single subplot

        # Generate pie chart for each income
        for idx, (income_category, answer_counts) in enumerate(grouped_data.iterrows()):
            axis = axes[idx] if len(grouped_data.index) > 1 else axes[0]

            # Filter small percentage categories into "Others"
            total = answer_counts.sum()
            filtered_labels = []
            filtered_sizes = []
            others_size = 0

            # Process each category to separate significant vs small percentages
            for label, size in answer_counts.items():
                percentage = (size / total) * 100
                if percentage >= min_percentage:
                    filtered_labels.append(label)
                    filtered_sizes.append(size)
                else:
                    others_size += size  # Aggregate small categories

            # Add "Others" category if small percentages exist
            if others_size > 0:
                filtered_labels.append("Others")
                filtered_sizes.append(others_size)

            # Create color palette
            colors = sns.color_palette(palette, len(filtered_sizes))

            # Explode the largest slice
            max_idx = filtered_sizes.index(max(filtered_sizes)) if filtered_sizes else 0
            explode = [0.1 if i == max_idx else 0 for i in range(len(filtered_sizes))]

            # Create pie chart
            wedges, texts, autotexts = axis.pie(
                filtered_sizes,
                labels=filtered_labels if len(filtered_labels) > 1 else None, # Hide label if only "Others"
                autopct=lambda p: f'{p:.1f}%' if p >= min_percentage else '', # percentage display
                startangle=90,                                          # Initial rotation angle
                colors=colors,                                          # Color scheme
                explode=explode,                                        # Slice explosion effect
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},    # Slice border styling
                pctdistance=0.85,                       # Adjusts the distance of the percentages
                textprops={                                             # Text styling parameters
                    'fontsize': 10,
                    'fontweight': 'bold'
                }
            )

        # ======================
        # STYLING
        # ======================

        # Title and labels
        question_title: str = (questions.get(selected_question, selected_question) +
                               f" ({selected_question})"
                               )
        wrapped_title: str = textwrap.fill(question_title, width=40)

        # Apply title styling
        figure.suptitle(
            wrapped_title,
            fontsize=18,
            fontweight='bold',
            color='navy'
        )

        # Add income title below subplot
        axis.set_title(
            income_category,    # Title text based on the income category
            y=-0.15,            # Position the title slightly below the plot
            fontsize=14,
            fontweight='bold',
            color='navy'
        )

        # Percentage label styling
        for autotext in autotexts:
            autotext.set_color('black')      # Set percentage text color
            autotext.set_fontsize(12)        # Adjust font size
            autotext.set_fontweight('bold')  # Emphasize text

        # Category label styling
        for text in texts:
            text.set_fontsize(12)   # Label text size
            text.set_color('black') # Label text color

        # Add legend if "Others" category exists
        if "Others" in filtered_labels:
            axis.legend(
                wedges,
                filtered_labels,
                title="Categories",         # Legend title
                loc="center left",          # Position
                bbox_to_anchor=(1, 0.5),    # Placement outside chart
                fontsize=10                 # Legend text size
            )

        # Display the chart
        plt.tight_layout()

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
        print(f"❌ [ERROR] Unexpected error: {gen_err}")
        return None
