"""
This module provides functions to load data and generate charts
from an impulse buying dataset. It includes functions to generate
bar charts and pie charts, with the option to distinguish data by
gender, school, or income.

Functions:
- load_data: Load the CSV file and return the DataFrame.
- plot_question_data: Generate a bar chart for a selected question.
- plot_question_data_by_gender: Generate a bar chart distinguishing by gender.
- plot_question_data_by_school: Generate a bar chart distinguishing by school.
- plot_question_data_by_income: Generate a bar chart distinguishing by income.
- create_pie_chart: Generate a pie chart for a selected question.
- create_pie_chart_by_gender: Generate a pie chart distinguishing by gender.
- question_plot: Main function to generate charts for a selected question.
- create_question_combobox: Create a QComboBox for selecting a question.
"""
# Standard library imports
import os
import textwrap

# Third-party imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PySide6.QtWidgets import QComboBox
from matplotlib.figure import Figure
from pandas import DataFrame

# Local project-specific imports
from FinalProject.assets.impulse_buying_data.data_dictionary import questions, answers, gender, \
    school, income


def load_data() -> DataFrame | None:
    """Load the CSV file and return the DataFrame."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_csv_path = os.path.join(current_dir, "..", "assets",
                                    "impulse_buying_data", "cleaned_data.csv")

    try:
        # Attempt to load the CSV
        df = pd.read_csv(cleaned_csv_path)
        return df

    except FileNotFoundError:
        print(f"Error: The file {cleaned_csv_path} is not found.")
        return None

    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None

    except pd.errors.ParserError:
        print("Error: There was an issue parsing the CSV file.")
        return None

    except Exception as gen_err:
        print(f"Error loading data: {gen_err}")
        return None

def plot_question_data(df: DataFrame, selected_question: str) -> Figure | None:
    """Generate the bar chart for a selected question."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns:
        print(f"Error: The question {selected_question} is not found in the data.")
        return

    # Map the answers using the `answers` dictionary
    mapped_answers_df: DataFrame = pd.DataFrame(
        {selected_question: df[selected_question].map(answers)}
    )

    if mapped_answers_df[selected_question].isnull().any():
        print(f"Warning: There are null values for the question {selected_question}.")

    # Define the order of the categories
    custom_order: list[str] = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category
    response_counts: pd.Series = mapped_answers_df[selected_question].value_counts()

    # Reindex the categories according to the defined order and fill missing values with 0
    response_counts = response_counts.reindex(custom_order, fill_value=0)

    if response_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    figure, axis = plt.subplots(figsize=(8, 6))
    axis = sns.barplot(x=response_counts.index, y=response_counts.values,
                     palette='Blues_d', edgecolor='white', hue=response_counts.index)

    # Add values on top of the bars
    for bar in axis.patches:
        value: int = int(bar.get_height())  # Get the height of the bar (frequency)
        axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.1,
                f'{value}', ha='center', va='bottom', color='black',
                  fontsize=14, fontweight='bold'
                 )

    # Add the title and labels
    question_title: str = (questions.get(selected_question, selected_question) +
                           f" ({selected_question})")
    wrapped_title: str = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y: int = response_counts.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return figure


def plot_question_data_by_gender(df: DataFrame, selected_question: str) -> Figure | None:
    """Generate the bar chart for a selected question, distinguishing by gender."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q2_GENDER' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q2_GENDER'"
              " is not found in the data."
             )
        return

    df['Q2_GENDER'] = df['Q2_GENDER'].map(gender)

    # Map the answers using the `answers` dictionary
    gender_mapped_answers_df: DataFrame = pd.DataFrame({
        'Q2_GENDER': df['Q2_GENDER'],
        selected_question: df[selected_question].map(answers)
    })

    # Define the order of the categories
    custom_order: list[str] = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category, grouped by gender
    response_counts_by_gender: DataFrame = gender_mapped_answers_df.groupby(
        ['Q2_GENDER', selected_question]
    ).size().unstack(fill_value=0)
    response_counts_by_gender = response_counts_by_gender.reindex(
        columns=custom_order, fill_value=0
    )

    if response_counts_by_gender.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    figure, axis = plt.subplots(figsize=(10, 6))
    response_counts_by_gender.T.plot(kind='bar', ax=axis,
                                     color=['pink', '#197CF4'], edgecolor='white'
                                    )

    # Add values on top of the bars
    for bar in axis.patches:
        height: int = int(bar.get_height())
        if height > 0:
            axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.1,
                    f'{height}', ha='center', va='bottom', color='black',
                      fontsize=14, fontweight='bold'
                     )

    # Add the title and labels
    question_title: str = (questions.get(selected_question, selected_question) +
                           f" ({selected_question})")
    wrapped_title: str = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y: int = response_counts_by_gender.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Change the legend title
    axis.legend(title='Gender')
    
    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return figure


def plot_question_data_by_school(df: DataFrame, selected_question: str) -> Figure | None:
    """Generate a bar chart for a selected question, distinguishing by school."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q3_SCHOOL' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q3_SCHOOL'"
              " is not found in the data.")
        return

    # Map the schools using the `school` dictionary
    df['Q3_SCHOOL'] = df['Q3_SCHOOL'].map(school)

    # Map the answers using the `answers` dictionary
    school_mapped_answers_df: DataFrame = pd.DataFrame({
        'Q3_SCHOOL': df['Q3_SCHOOL'],  # School column after mapping
        selected_question: df[selected_question].map(answers)
    })

    # Define the order of the categories
    custom_order: list[str] = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category, grouped by school
    response_counts_by_school: DataFrame = school_mapped_answers_df.groupby(
        ['Q3_SCHOOL', selected_question]
    ).size().unstack(fill_value=0)
    response_counts_by_school = response_counts_by_school.reindex(
        columns=custom_order, fill_value=0
    )

    if response_counts_by_school.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    figure, axis = plt.subplots(figsize=(12, 6))
    response_counts_by_school.T.plot(kind='bar', ax=axis, colormap='Set2', edgecolor='white')

    # Add values on top of the bars
    for bar in axis.patches:
        height: int = int(bar.get_height())
        if height > 0:
            axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.1,
                      f'{height}', ha='center', va='bottom', color='black',
                      fontsize=14, fontweight='bold'
                     )

    # Add the title and labels
    question_title: str = (questions.get(selected_question, selected_question) +
                           f" ({selected_question})"
                          )
    wrapped_title: str = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y: int = response_counts_by_school.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Change the legend title
    axis.legend(title='School')

    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return figure


def plot_question_data_by_income(df: pd.DataFrame, selected_question: str) -> Figure | None:
    """Generate a bar chart for a selected question, distinguishing by income."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    # Ensure the selected question and income column are in the data
    if selected_question not in df.columns or 'Q4_INCOME' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q4_INCOME'"
              " is not found in the data."
             )
        return

    # Map the income using the `income` dictionary (assuming it's imported or defined somewhere)
    df['Q4_INCOME'] = df['Q4_INCOME'].map(
        income)  # You need to define or import the `income` dictionary

    # Ensure the 'Q4_INCOME' column is categorical and respects the order from the dictionary
    # Use the ordered values from the `income` dictionary
    income_order: list[str] = list(income.values())
    df['Q4_INCOME'] = pd.Categorical(df['Q4_INCOME'], categories=income_order, ordered=True)

    # Map the answers using the `answers` dictionary
    question_answers_df: pd.DataFrame = pd.DataFrame({
        'Q4_INCOME': df['Q4_INCOME'],  # Income column after mapping
        selected_question: df[selected_question].map(answers)
    })

    # Define the order of the categories
    custom_order: list[str] = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category, grouped by income
    answer_counts_by_income: pd.DataFrame = question_answers_df.groupby(
        ['Q4_INCOME', selected_question]
    ).size().unstack(fill_value=0)
    answer_counts_by_income = answer_counts_by_income.reindex(columns=custom_order, fill_value=0)

    if answer_counts_by_income.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    figure, axis = plt.subplots(figsize=(12, 6))
    answer_counts_by_income.T.plot(kind='bar', ax=axis, colormap='Set1', edgecolor='white')

    # Add values on top of the bars
    for bar in axis.patches:
        height: int = int(bar.get_height())
        if height > 0:
            axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.1,
                    f'{height}', ha='center', va='bottom', color='black',
                      fontsize=14, fontweight='bold'
                     )

    # Add the title and labels
    question_title: str = (questions.get(selected_question, selected_question) +
                           f" ({selected_question})"
                          )
    wrapped_title: str = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y: int = answer_counts_by_income.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Change the legend title
    axis.legend(title='Income')

    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return figure


def create_pie_chart(df: pd.DataFrame, selected_question: str) -> Figure | None:
    """Generate a single pie chart for a selected question, aggregating all schools."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q3_SCHOOL' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q3_SCHOOL'"
              " is not found in the data.")
        return

    # Map the answers using the `answers` dictionary
    question_answers_df: pd.DataFrame = pd.DataFrame({
        'Q3_SCHOOL': df['Q3_SCHOOL'],  # School column
        selected_question: df[selected_question].map(answers)
    })

    # Count the number of answers for each category, ignoring the school distinction
    answer_counts: pd.Series = question_answers_df[selected_question].value_counts()

    # Check if the answer_counts Series is empty
    if answer_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Exploding the largest slice
    explode: list[float] = [0.1 if i == answer_counts.idxmax() else 0 for i in answer_counts.index]

    # Create a single pie chart
    figure, axis = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = axis.pie(answer_counts,
           labels=answer_counts.index,
           autopct='%1.1f%%',
           startangle=90,
           colors=sns.color_palette('Set2', len(answer_counts)),
           explode=explode,
           wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},
           pctdistance=0.85,  # Adjusts the distance of the percentages from the center
           labeldistance=1.1  # Moves labels slightly outward from the center
          )

    # Adjust the position of the percentages manually to prevent collisions
    for i, autotext in enumerate(autotexts):
        angle: float = (wedges[i].theta2 - wedges[i].theta1) / 2. + wedges[
            i].theta1  # Calculate angle of the sector
        angle_rad: float = np.radians(angle)

        # Move percentages outwards if they collide
        x_offset: float = 0.9 * np.cos(angle_rad)  # X position of the percentage
        y_offset: float = 0.9 * np.sin(angle_rad)  # Y position of the percentage

        # Adjust position slightly further out if necessary (for better readability)
        autotext.set_position((x_offset, y_offset))

    # Improve label formatting
    for text in texts + autotexts:
        text.set_fontsize(12)
        text.set_fontweight('bold')

    # Add the title
    question_title: str = (questions.get(selected_question, selected_question) +
                           f" ({selected_question})"
                          )
    wrapped_title: str = textwrap.fill(question_title, width=40)
    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')

    # Display the chart
    plt.tight_layout()

    return figure


def create_pie_chart_by_gender(df: pd.DataFrame, selected_question: str) -> Figure | None:
    """Generate a pie chart for a selected question, distinguishing by gender."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q2_GENDER' not in df.columns:
        print(
            f"Error: The question {selected_question} or the column 'Q2_GENDER'"
            " is not found in the data.")
        return

    # Map the answers using the `answers` dictionary
    df['Q2_GENDER'] = df['Q2_GENDER'].map(gender)  # Map gender column

    # Map the answers using the `answers` dictionary for the selected question
    gender_answers_df: pd.DataFrame = pd.DataFrame({
        'Q2_GENDER': df['Q2_GENDER'],  # Gender column
        selected_question: df[selected_question].map(answers)
    })

    # Count the number of answers for each category, grouped by gender
    answer_counts_by_gender: pd.DataFrame = gender_answers_df.groupby(
        ['Q2_GENDER', selected_question]
    ).size().unstack(fill_value=0)

    if answer_counts_by_gender.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the pie chart for each gender
    figure, axis = plt.subplots(figsize=(12, 6))

    # Generate pie chart for each gender category
    for gender_category in answer_counts_by_gender.index:
        answer_counts = answer_counts_by_gender.loc[gender_category]

        # Exploding the largest slice
        explode: list[float] = [0.1 if i == answer_counts.idxmax()
                                else 0 for i in answer_counts.index
                               ]

        # Create the pie chart
        wedges, texts, autotexts = axis.pie(answer_counts,
                                          labels=answer_counts.index,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          colors=sns.color_palette('Set2', len(answer_counts)),
                                          explode=explode,
                                          wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},
                                          pctdistance=0.85,
                                          # Adjusts the distance of the percentages from the center
                                          labeldistance=1.1)  # Moves labels slightly outward

        # Adjust the position of the percentages manually to prevent collisions
        for i, autotext in enumerate(autotexts):
            angle: float = (wedges[i].theta2 - wedges[i].theta1) / 2. + wedges[
                i].theta1  # Calculate angle of the sector
            angle_rad: float = np.radians(angle)

            # Move percentages outwards if they collide
            x_offset: float = 0.9 * np.cos(angle_rad)  # X position of the percentage
            y_offset: float = 0.9 * np.sin(angle_rad)  # Y position of the percentage

            autotext.set_position((x_offset, y_offset))

        # Improve label formatting
        for text in texts + autotexts:
            text.set_fontsize(12)
            text.set_fontweight('bold')

    # Add the title
    question_title: str = (questions.get(selected_question, selected_question) +
                           f" ({selected_question})"
                          )
    wrapped_title: str = textwrap.fill(question_title, width=40)
    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')

    # Display the chart
    plt.tight_layout()

    return figure


def question_plot(
        selected_question: str,
        distinction_by_gender: bool = False,
        distinction_by_school: bool = False,
        distinction_by_income: bool = False,
        pie_chart: bool = False,
        pie_chart_by_gender: bool = False
        ) -> Figure | None:
    """Main function to generate the chart for a selected question."""
    survey_data: pd.DataFrame = load_data()  # Load the data
    if survey_data is None:
        print(f"Error: Data loading failed for question {selected_question}")
        return None

    # Generate the chart with gender distinction
    if distinction_by_gender:
        return plot_question_data_by_gender(survey_data, selected_question)

    # Generate the chart with school distinction
    elif distinction_by_school:
        return plot_question_data_by_school(survey_data, selected_question)

    # Generate the chart with income distinction
    elif distinction_by_income:
        return plot_question_data_by_income(survey_data, selected_question)

    # Generate a pie chart
    elif pie_chart:
        return create_pie_chart(survey_data, selected_question)

    # Generate a pie chart by gender
    elif pie_chart_by_gender:
        return create_pie_chart_by_gender(survey_data, selected_question)
    # Generate the chart without distinction
    else:
        return plot_question_data(survey_data, selected_question)


def create_question_combobox(parent, callback, current_distinction: str | None = None)\
        -> QComboBox | None:
    """Function to create a QComboBox for selecting a question."""
    try:
        # Create the QComboBox
        question_combobox_widget: QComboBox = QComboBox(parent)

        # Add each question identifier and its corresponding description to the combobox
        for question_id, question_description in questions.items():
            question_combobox_widget.addItem(question_description, question_id)

        # Connect the signal to the callback function to update the graph
        question_combobox_widget.currentIndexChanged.connect(lambda: callback(current_distinction))

        return question_combobox_widget

    except Exception as gen_err:
        print(f"Error creating question combobox: {gen_err}")
        return None
