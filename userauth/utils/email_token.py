"""
This module provides utility functions for generating and verifying email\
    tokens
The tokens are used for email verification purposes.
"""

from .token_manager import *


def generate_email_token(email):
    """
    Generates a time-limited token for email verification.
    """
    email_token = generate_token(email)
    return email_token

def verify_email_token(token, max_age=300):
    """
    Verifies an email veriification token.
    Args:
        token (str): The signed token to verify.
        max_age (int): The maximum age of the token in seconds.
    Returns:
        str or None: The original email if the token is valid, otherwise None.
    """
    return verify_token(token, max_age)


