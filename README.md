# Impulse Buying Factors on TikTok Shop

Este es un proyecto de **Final Project** creado por **David Cruz Gómez**.
La aplicación es una simulación de un sistema de inicio de sesión, registro de usuario y recuperación de contraseñas para una plataforma de compras en línea, como **TikTok Shop**.
La interfaz está desarrollada con **PySide6** (una interfaz de Python para Qt), que es una biblioteca para la creación de interfaces gráficas de usuario (GUI).

### Main Features:
- **Login**: Users can log in with a username and password.
- **User Registration**: Users can register by creating a new account.
- **Password Recovery**: Users can recover their password via email.
- **Dashboard**: After logging in, users are redirected to a welcome dashboard.

## Technologies Used:
- **PySide6**: For creating the graphical user interface (GUI).
- **JSON**: To store the user database and configurations.
- **bcrypt**: For hashing and verifying user passwords.
- **smtplib**: To send password recovery emails.



FinalProject/
│
├── assets/
│   ├── users_db.json             # User database
│   ├── email_config.json         # Email configuration (SMTP)
│   ├── regex.py                  # Regular expressions (e.g., for validating emails)
│   └── utils.py                  # Utility functions (e.g., displaying messages)
│
├── styles/
│   ├── styles.py                 # Styles for the GUI (buttons, text fields, etc.)
│   └── __init__.py               # Empty file to import the styles module
│
├── windows/
│   ├── main_window.py            # Main window for login
│   ├── dashboard_window.py       # User dashboard window
│   ├── registration_window.py    # User registration window
│   ├── recovery_window.py        # Password recovery window
│   └── __init__.py               # Empty file to import the windows module
│
├── requirements.txt              # Project dependencies
├── main.py                       # Main file to run the application
└── README.md                     # This file
