import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import pandas as pd
import os
from FinalProject.assets.impulse_buying_data.data_dictionary import questions, answers
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
    except Exception as gen_err:
        print(f"Error loading data: {gen_err}")
        return None

def plot_question_data(df, selected_question):
    """Generate the bar chart for a selected question."""
    if df is None:
        return  # If the DataFrame can't be loaded, don't generate the chart

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

def question_plot(selected_question):
    """Main function to generate the chart for a selected question."""
    df = load_data()  # Load the data
    if df is None:
        print(f"Error: Data loading failed for question {selected_question}")
        return None

    return plot_question_data(df, selected_question)  # Generate the chart


def create_question_combobox(parent, callback):
    """Function to create a QComboBox for selecting a question."""
    # Create the QComboBox
    question_combobox = QComboBox(parent)

    # Add each question identifier and its corresponding description to the combobox
    for key, value in questions.items():
        question_combobox.addItem(value, key)

    # Connect the signal to the callback function to update the graph
    question_combobox.currentIndexChanged.connect(callback)

    return question_combobox