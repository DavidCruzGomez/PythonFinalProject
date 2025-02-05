"""
Regular expressions for validating email addresses, passwords, and usernames.

This module contains a set of regular expressions designed to validate user input
for email addresses, passwords, and usernames. Each regular expression ensures
that the input conforms to specific format requirements, such as proper structure,
length constraints, and allowed characters.

Key validations include:

- `EMAIL_REGEX`: Validates the format of email addresses,
ensuring proper structure with an optional subdomain, domain, and extension.

- `PASSWORD_REGEX`: Defines a set of regular expressions for
validating passwords based on specific criteria, including the presence of
uppercase and lowercase letters, digits, special characters, and length constraints.

- `USERNAME_REGEX`: Validates usernames to ensure they consist of alphanumeric
characters, underscores, hyphens, and periods, with length and format rules
to ensure they meet specific requirements.

Each regular expression is customizable for different validation requirements
and is used to ensure that input data conforms to expected patterns before being
processed in the application.
"""

EMAIL_REGEX: str = (
    r"^"                        # Start of the string
    r"[a-zA-Z0-9._%+-]+"        # Username part (allowed alphanumeric and special characters)
    r"@"                        # The "@" symbol is mandatory
    r"[a-zA-Z0-9-]+"            # Domain (must have at least one alphanumeric character or hyphen)
    r"(\.[a-zA-Z0-9-]+)*"       # There can be additional subdomains
                                # (letters, numbers, and hyphens are allowed)
    r"\."                       # A literal dot (.) separating the domain from the extension
    r"[a-zA-Z]{2,}$"            # Domain extension (must be at least 2 letters)
)

PASSWORD_REGEX: dict[str, str] = {
    'upper': r'[A-Z]',               # At least one uppercase letter
    'lower': r'[a-z]',               # At least one lowercase letter
    'number': r'\d',                 # At least one number
    'special': r'[@$!%*?&]',         # At least one special character
    'length': r'^.{8,16}$',          # Length between 8 and 16 characters
    'all': (
        r"^(?=.*[a-z])"              # At least one lowercase letter
        r"(?=.*[A-Z])"               # At least one uppercase letter
        r"(?=.*\d)"                  # At least one number
        r"(?=.*[@$!%*?&])"           # At least one special character from the allowed set
        r"[A-Za-z\d@$!%*?&]{8,16}$"  # Only letters, numbers, and allowed special characters,
                                     # with a length between 8 and 16 characters
    )
}

USERNAME_REGEX: dict[str, str] = {
    'length': r'.{3,18}',                   # Length between 3 and 18 characters
    'valid_chars': r'^[A-Za-z0-9._-]+$',    # Only alphanumeric characters, dots, hyphens,
                                            # and underscores
    'start_alnum': r'^[A-Za-z0-9]',         # Starts with alphanumeric
    'end_alnum': r'[A-Za-z0-9]$',           # Ends with alphanumeric
    'all': (
        r"^[A-Za-z0-9]"              # Start with an alphanumeric character
        r"[A-Za-z0-9._-]{2,16}"      # Allows alphanumeric, dot, dash, and underscore
                                     # (2 to 16 characters)
        r"[A-Za-z0-9]$"              # End with an alphanumeric character
    )
}
