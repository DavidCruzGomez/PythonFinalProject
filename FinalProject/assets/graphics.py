import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import pandas as pd
import os
from FinalProject.assets.impulse_buying_data.data_dictionary import questions, answers, gender, school, income
from PySide6.QtWidgets import QComboBox


def load_data():
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

def plot_question_data(df, selected_question):
    """Generate the bar chart for a selected question."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns:
        print(f"Error: The question {selected_question} is not found in the data.")
        return

    # Map the answers using the `answers` dictionary
    temp_df = pd.DataFrame({selected_question: df[selected_question].map(answers)})

    if temp_df[selected_question].isnull().any():
        print(f"Warning: There are null values for the question {selected_question}.")

    # Define the order of the categories
    custom_order = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category
    response_counts = temp_df[selected_question].value_counts()

    # Reindex the categories according to the defined order and fill missing values with 0
    response_counts = response_counts.reindex(custom_order, fill_value=0)

    if response_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.barplot(x=response_counts.index, y=response_counts.values,
                     palette='Blues_d', edgecolor='white', hue=response_counts.index)

    # Add values on top of the bars
    for p in ax.patches:
        value = int(p.get_height())  # Get the height of the bar (frequency)
        ax.text(p.get_x() + p.get_width() / 2, p.get_height() - 0.1,
                f'{value}', ha='center', va='bottom', color='black', fontsize=14, fontweight='bold')

    # Add the title and labels
    question_title = questions.get(selected_question, selected_question) + f" ({selected_question})"
    wrapped_title = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y = response_counts.values.max()
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
    return fig


def plot_question_data_by_gender(df, selected_question):
    """Generate the bar chart for a selected question, distinguishing by gender."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q2_GENDER' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q2_GENDER' is not found in the data.")
        return

    df['Q2_GENDER'] = df['Q2_GENDER'].map(gender)

    # Map the answers using the `answers` dictionary
    temp_df = pd.DataFrame({
        'Q2_GENDER': df['Q2_GENDER'],
        selected_question: df[selected_question].map(answers)
    })

    # Define the order of the categories
    custom_order = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category, grouped by gender
    response_counts = temp_df.groupby(['Q2_GENDER', selected_question]).size().unstack(fill_value=0)
    response_counts = response_counts.reindex(columns=custom_order, fill_value=0)

    if response_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    response_counts.T.plot(kind='bar', ax=ax, color=['pink', '#197CF4'], edgecolor='white')

    # Add values on top of the bars
    for p in ax.patches:
        height = int(p.get_height())
        if height > 0:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() - 0.1,
                    f'{height}', ha='center', va='bottom', color='black', fontsize=14, fontweight='bold')

    # Add the title and labels
    question_title = questions.get(selected_question, selected_question) + f" ({selected_question})"
    wrapped_title = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y = response_counts.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Change the legend title
    ax.legend(title='Gender')
    
    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return fig


def plot_question_data_by_school(df, selected_question):
    """Generate a bar chart for a selected question, distinguishing by school."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q3_SCHOOL' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q3_SCHOOL' is not found in the data.")
        return

    # Map the schools using the `school` dictionary
    df['Q3_SCHOOL'] = df['Q3_SCHOOL'].map(school)

    # Map the answers using the `answers` dictionary
    temp_df = pd.DataFrame({
        'Q3_SCHOOL': df['Q3_SCHOOL'],  # School column after mapping
        selected_question: df[selected_question].map(answers)
    })

    # Define the order of the categories
    custom_order = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category, grouped by school
    response_counts = temp_df.groupby(['Q3_SCHOOL', selected_question]).size().unstack(fill_value=0)
    response_counts = response_counts.reindex(columns=custom_order, fill_value=0)

    if response_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    fig, ax = plt.subplots(figsize=(12, 6))
    response_counts.T.plot(kind='bar', ax=ax, colormap='Set2', edgecolor='white')

    # Add values on top of the bars
    for p in ax.patches:
        height = int(p.get_height())
        if height > 0:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() - 0.1,
                    f'{height}', ha='center', va='bottom', color='black', fontsize=14, fontweight='bold')

    # Add the title and labels
    question_title = questions.get(selected_question, selected_question) + f" ({selected_question})"
    wrapped_title = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y = response_counts.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Change the legend title
    ax.legend(title='School')

    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return fig


def plot_question_data_by_income(df, selected_question):
    """Generate a bar chart for a selected question, distinguishing by income."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    # Ensure the selected question and income column are in the data
    if selected_question not in df.columns or 'Q4_INCOME' not in df.columns:
        print(f"Error: The question {selected_question} or the column 'Q4_INCOME' is not found in the data.")
        return

    # Map the income using the `income` dictionary (assuming it's imported or defined somewhere)
    df['Q4_INCOME'] = df['Q4_INCOME'].map(
        income)  # You need to define or import the `income` dictionary

    # Ensure the 'Q4_INCOME' column is categorical and respects the order from the dictionary
    income_order = list(income.values())  # Use the ordered values from the `income` dictionary
    df['Q4_INCOME'] = pd.Categorical(df['Q4_INCOME'], categories=income_order, ordered=True)

    # Map the answers using the `answers` dictionary
    temp_df = pd.DataFrame({
        'Q4_INCOME': df['Q4_INCOME'],  # Income column after mapping
        selected_question: df[selected_question].map(answers)
    })

    # Define the order of the categories
    custom_order = ['Very disagree', 'Disagree', 'Normal', 'Agree', 'Very agree']

    # Count the number of answers for each category, grouped by income
    response_counts = temp_df.groupby(['Q4_INCOME', selected_question]).size().unstack(fill_value=0)
    response_counts = response_counts.reindex(columns=custom_order, fill_value=0)

    if response_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the chart
    fig, ax = plt.subplots(figsize=(12, 6))
    response_counts.T.plot(kind='bar', ax=ax, colormap='Set1', edgecolor='white')

    # Add values on top of the bars
    for p in ax.patches:
        height = int(p.get_height())
        if height > 0:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() - 0.1,
                    f'{height}', ha='center', va='bottom', color='black', fontsize=14, fontweight='bold')

    # Add the title and labels
    question_title = questions.get(selected_question, selected_question) + f" ({selected_question})"
    wrapped_title = textwrap.fill(question_title, width=40)

    plt.title(wrapped_title, fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Degree of agreement/disagreement', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Answers', fontsize=14, fontweight='bold')

    # Adjust the X-axis labels to be centered
    plt.xticks(rotation=30, ha='center', fontsize=12)

    # Adjust the Y-axis so that the ticks are every 25 units
    max_y = response_counts.values.max()
    plt.yticks(range(0, max_y + 25, 25))

    # Add grid lines to improve readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a border to the chart
    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)

    # Change the legend title
    ax.legend(title='Income')

    # Adjust space for the title
    plt.tight_layout()

    # Display the chart
    return fig


def pie_chart_by_school(df, selected_question):
    """Generate a pie chart for a selected question, distinguishing by school."""
    if df is None:
        print("Error: Data is not available to plot the question.")
        return

    if selected_question not in df.columns or 'Q3_SCHOOL' not in df.columns:
        print(
            f"Error: The question {selected_question} or the column 'Q3_SCHOOL' is not found in the data.")
        return


    # Map the answers using the `answers` dictionary
    temp_df = pd.DataFrame({
        'Q3_SCHOOL': df['Q3_SCHOOL'],  # School column after mapping
        selected_question: df[selected_question].map(answers)
    })

    # Count the number of answers for each category, grouped by school
    response_counts = temp_df.groupby(['Q3_SCHOOL', selected_question]).size().unstack(fill_value=0)

    # Check if the response_counts dataframe is empty
    if response_counts.empty:
        print(f"Error: No responses were found for the question {selected_question}.")
        return

    # Create the pie chart for each school
    fig, axes = plt.subplots(1, len(response_counts.index), figsize=(15, 7))

    if len(response_counts.index) == 1:
        axes = [axes]  # Make sure we always have an iterable for axes

    for i, school in enumerate(response_counts.index):
        # Get the data for each school
        school_data = response_counts.loc[school]

        # Generate the pie chart for the current school
        ax = axes[i]
        ax.pie(school_data, labels=school_data.index, autopct='%1.1f%%', startangle=90,
               colors=sns.color_palette('Set2', len(school_data)))

        # Add the title for each school
        ax.set_title(f'{school} Responses', fontsize=14, fontweight='bold')

    # Adjust space for the titles and labels
    plt.tight_layout()

    # Display the chart
    return fig


def question_plot(selected_question,
                  distinction_by_gender=False,
                  distinction_by_school=False,
                  distinction_by_income=False,
                  pie_chart=False
                  ):
    """Main function to generate the chart for a selected question."""
    df = load_data()  # Load the data
    if df is None:
        print(f"Error: Data loading failed for question {selected_question}")
        return None

    # Generate the chart with gender distinction
    if distinction_by_gender:
        return plot_question_data_by_gender(df, selected_question)

    # Generate the chart with school distinction
    elif distinction_by_school:
        return plot_question_data_by_school(df, selected_question)

    # Generate the chart with income distinction
    elif distinction_by_income:
        return plot_question_data_by_income(df, selected_question)

    # Generate a pie chart
    elif pie_chart:
        return pie_chart_by_school(df, selected_question)

    # Generate the chart without distinction
    else:
        return plot_question_data(df, selected_question)


def create_question_combobox(parent, callback):
    """Function to create a QComboBox for selecting a question."""
    try:
        # Create the QComboBox
        question_combobox = QComboBox(parent)

        # Add each question identifier and its corresponding description to the combobox
        for key, value in questions.items():
            question_combobox.addItem(value, key)

        # Connect the signal to the callback function to update the graph
        question_combobox.currentIndexChanged.connect(callback)

        return question_combobox
    except Exception as gen_err:
        print(f"Error creating question combobox: {gen_err}")
        return None