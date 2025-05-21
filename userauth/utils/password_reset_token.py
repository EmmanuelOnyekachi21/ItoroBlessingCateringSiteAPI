"""
This module provides utility functions for generating and verifying 
time-limited tokens used in password reset functionality.
Functions:
    - generate_password_reset_token(email): Generates a secure token 
      associated with the provided email for password reset purposes.
    - verify_password_reset_token(token, max_age): Verifies the validity 
      of a password reset token within a specified time frame.
Dependencies:
    - generate_token: A function from the token_manager module used to 
      create secure tokens.
    - verify_token: A function from the token_manager module used to 
      validate tokens.
Usage:
    These functions are intended to be used as part of the user 
    authentication system to facilitate secure password reset operations.
"""

from .token_manager import generate_token, verify_token


def generate_password_reset_token(email):
    """
    Generates a time-limited token for password reset.
    """
    return generate_token(email)

def verify_password_reset_token(token, max_age=300):
    """
    Verifies a password reset token.
    
    Args:
        token (str): The signed token to verify.
        max_age (int): The maximum age of the token in seconds.
    """
    return verify_token(token, max_age)

