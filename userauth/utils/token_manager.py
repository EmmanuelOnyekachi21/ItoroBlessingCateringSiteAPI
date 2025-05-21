"""
token_manager.py

This module provides utility functions for generating and verifying time-limited tokens 
using Django's signing framework. It leverages the `TimestampSigner` class to create 
secure, signed tokens that can expire after a specified duration.

Functions:
    - generate_token(data): Generates a signed token for the given data.
    - verify_token(token, max_age): Verifies the validity of a signed token and extracts 
      the original data if the token is valid and within the specified time limit.

Dependencies:
    - django.core.signing.TimestampSigner
    - django.core.signing.SignatureExpired
    - django.core.signing.BadSignature
Using Django signing system to create a time-limited token
"""
from django.core.signing import (
    SignatureExpired, TimestampSigner, BadSignature
)


signer = TimestampSigner()

def generate_token(data):
    """
    Generates a time-limited token for the given data.
    Args:
        data (str): The data to be signed.
    Returns:
        str: The signed token.
    """
    return signer.sign(data)

def verify_token(token, max_age):
    """
    Verifies a time-limited token and extracts the original data.

    Args:
        token (str): The signed token to verify.
        max_age (int): The maximum age of the token in seconds.

    Returns:
        str or None: The original data if the token is valid, otherwise None.
    """
    try:
        return signer.unsign(token, max_age=max_age)
        return email
    except (SignatureExpired, BadSignature):
        return None


