# Impulse Buying Factors on TikTok Shop
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-DavidCruzGomez-blue?logo=github&logoColor=white)](https://github.com/DavidCruzGomez)


## Table of Contents
1. [Introduction](#introduction)
2. [Project Features](#project-features)
3. [Technologies Used](#technologies-used)
4. [Windows](#windows)
5. [Directory Structure](#directory-structure)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Testing](#testing)
9. [Owner](#owner)

## Introduction
This is a Final Project created by David Cruz Gómez.
Project Description: This project, is an application that simulates
a login system, user registration, and password recovery for a data
analysis platform like TikTok Shop. In addition to user management,
it provides tools to upload, preprocess, and analyze data related
to impulse buying factors. The interface is developed using PySide6,
ensuring an interactive and functional graphical experience.

## Project Features:

### User Management:
- 💼**Registration**: Allows users to create an account by providing basic information.
- 🔒**Login**: Secure access to the system using credentials.
- 🔑**Password Recovery**: Offers a process to recover passwords in case of loss.

### Data Analysis Interface:
- 📊**Data Preview**: Displays a quick preview of the DataFrame related to impulse buying factors.
- 📈**Descriptive Statistics**: Provides a statistical summary (mean, median, standard deviation, etc.).
- 📥**Data Download**: Users can download the data file if it's not already available.
- 🛠️**Data Preprocessing**: Tools for cleaning the DataFrame (handling missing values, removing duplicates, etc.).

### Graph Visualization:
- 📉**Customizable Graphs**: Create customizable graphs based on the DataFrame.
- 🖼️**Graph Exporting**: Users can save the generated graphs in formats like PNG or JPG.

## Technologies Used:
- **PySide6**: For creating the graphical user interface (GUI).
- **JSON**: To store the user database and configurations.
- **bcrypt**: For hashing and verifying user passwords.
- **smtplib**: To send password recovery emails.
- **pandas**: For data manipulation and analysis.
- **matplotlib**: For generating customizable visualizations (graphs).
- **seaborn**: For enhanced data visualization and statistical graphics.
- **PyQt6**: Alternative Qt framework used in conjunction with PySide6 for GUI elements.
- **openpyxl**: To read and write Excel files, enabling data import/export functionality.
- **selenium**: For automating web browser interactions (e.g., scraping data for analysis).

## Windows:
### Login Window
![python login](https://github.com/user-attachments/assets/7f21f0b5-a119-4057-96d1-a067db98698e)

### Registration Window
![registration window](https://github.com/user-attachments/assets/1e792be2-cec7-4c2d-b4f3-d25853c679a6)

### Recovery Window
![recovery window](https://github.com/user-attachments/assets/c918e023-2434-4cb8-b8b7-8e0956fd621c)

### Dashboard Window Home
![Home](https://github.com/user-attachments/assets/076fe810-7585-4447-9ffd-98deaa76928a)

### Dashboard Window Graphs
![graphs](https://github.com/user-attachments/assets/822e0938-b1ba-45e4-90f7-6d0e9d63f311)


## Directory Structure

```plaintext
.
├── src/
│   ├── assets/
│   │   ├── exported_graphs/                # Directory for exported graphs
│   │   ├── impulse_buying_data/
│   │   │   ├── cleaned_data.csv            # Cleaned data CSV file
│   │   │   ├── data_dictionary.py          # Data dictionary script
│   │   │   ├── processed_data.csv          # Processed data CSV file
│   │   │   ├── Questionnaire.pdf           # Questionnaire in PDF format
│   │   │   └── Raw_data.xlsx               # Raw data in Excel format
│   │   ├── custom_errors.py                # Custom error classes
│   │   ├── dashboard_window_setup.py       # Dashboard window setup script
│   │   ├── download_files.py               # Script for downloading files
│   │   ├── email_config.json               # Email configuration (SMTP)
│   │   ├── graph_widget.py                 # Graph widget script
│   │   ├── graphics.py                     # Graphics related functions
│   │   ├── preprocess.py                   # Data preprocessing script                    
│   │   ├── regex.py                        # Regular expressions (e.g., for validating emails)
│   │   ├── users_db.json                   # User database
│   │   ├── users_db.py                     # User database functions
│   │   ├── utils.py                        # Utility functions (e.g., displaying messages)
│   │   └── __init__.py                     # Empty file to import the assets module
│   ├── styles/
│   │   ├── styles.py                       # Styles for the GUI (buttons, text fields, etc.)
│   │   └── __init__.py                     # Empty file to import the styles module
│   ├── visualization/
│   │   ├── charts/
│   │   │   ├── __init__.py                 # Empty file to import the charts module
│   │   │   ├── bar_charts.py               # Functions to create bar charts
│   │   │   ├── base.py                     # Base functions for charts visualization
│   │   │   └── pie_charts.py               # Functions to create pie charts
│   │   └── __init__.py                     # Empty file to import the visualization module
│   ├── windows/
│   │   ├── main_window.py                  # Main window for login
│   │   ├── dashboard_window.py             # User dashboard window
│   │   ├── registration_window.py          # User registration window
│   │   ├── recovery_window.py              # Password recovery window
│   │   └── __init__.py                     # Empty file to import the windows module
│   ├── main.py                             # Main file to run the application
│   └── __init__.py                         # Empty file to import the main package
├── tests/
│   ├── tests_assets/
│   │   ├── test_custom_errors.py           # Tests for custom errors
│   │   ├── test_dashboard_window_setup.py  # Tests for dashboard window setup      
│   │   ├── test_download_files.py          # Tests for file download functionality
│   │   ├── test_email_config.py            # Tests for email configuration
│   │   ├── test_graph_widget.py            # Tests for graph widget functionality
│   │   ├── test_preprocess.py              # Tests for data preprocessing
│   │   ├── test_regex.py                   # Tests for regular expressions
│   │   ├── test_users_db.py                # Tests for user database functions
│   │   ├── test_utils.py                   # Tests for utility functions
│   │   └── __init__.py                     # Empty file to import the tests_assets module
│   ├── tests_styles/
│   │   ├── test_styles.py                  # Tests for the styles in `styles.py`
│   │   └── __init__.py                     # Empty file to import the tests_styles module
│   ├── tests_visualization/
│   │   ├── tests_charts/
│   │   │   ├── __init__.py                 # Empty file to import the tests_charts module
│   │   │   ├── test_bar_charts.py          # Tests for bar charts
│   │   │   ├── test_base.py                # Tests for base visualization charts
│   │   │   └── test_pie_charts.py          # Tests for pie charts 
│   │   └── __init__.py                     # Empty file to import the tests_visualization module
│   ├── tests_windows/
│   │   ├── test_dashboard_window.py        # Tests for the `dashboard_window.py`     
│   │   ├── test_main_window.py             # Tests for the `main_window.py` (login window)
│   │   ├── test_recovery_window.py         # Tests for the `recovery_window.py` (password recovery window)
│   │   ├── test_registration_window.py     # Tests for the `registration_window.py` (user registration window)         
│   │   └── __init__.py                     # Empty file to import the tests_windows module
│   └── __init__.py                         # Empty file to import the tests package
├── docs/
│   └── UMLDiagram.xml                      # UML Diagram in XML format
│ 
├── CHANGELOG.md                            # Project change log
├── LICENSE.md                              # License for the project
├── README.md                               # This file
├── requirements.txt                        # Project dependencies
├── requirements_dev.txt                    # Development dependencies
├── setup.cfg                               # Configuration for packaging the project
├── setup.py                                # Script to install the project
├── VERSION.txt                             # Current version of the project
└── Dockerfile                              # Docker configuration for the project
```

## Installation
To install the project, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/DavidCruzGomez/PythonFinalProject.git
   
2. Navigate to the project directory:
    ```bash
    cd src
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

## Usage
To run the application, use the following command:
```bash
  python FinalProject/main.py
```
## Testing
To run the tests, use the following command:
```bash
  python -m unittest discover -s tests
```
<div style="border-left: 4px solid #8a2be2; padding: 1em; background: #f3f6fc;">
  <strong>⚠️ Important:</strong> You must disable manual login so that all tests work correctly.
</div>

### Owner
- David Cruz Gómez <david97torrejon@alumnos.cei.es>
