"""
This module provides utility functions for sending emails,
specifically for sending email verification links to users.
"""

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_email(subject, message, recipient_email):
    """
    Sends an email with the specified subject and message to the recipient.
    Args:
        subject (str): The subject of the email.
        message (str): The body content of the email.
        recipient_email (list): The email address(es) of the recipient(s).
    Raises:
        Exception: If the email fails to send, an exception will be raised.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_email,
        fail_silently=False,
    )


def send_verification_email(user_email, token):
    """
    Sends an email verification link to the specified user.

    Args:
        user_email (str): The email address of the user to\
            send the verification link to.
        token (str): The unique token used for verifying the user's email.

    The email contains a link that the user can\
        click to verify their email address.
    """
    subject = 'Verify your email'
    verification_link = (
        f'http://localhost:5173/verify/?token={token}'
    )
    message = (
        f"Click the link to verify your email: {verification_link}"
    )
    logger.info(f'Token for {user_email}: {token}')
    send_email(subject, message, [user_email])


def send_password_reset_email(user_email, token):
    """
    Sends a password reset link to the user_email with a unique reset token.

    Args:
        user_email (str): The email address of the user requesting a password
            reset.
        token (str): The unique token to be included in the password reset
            link.

    Returns:
        None

    Side Effects:
        Sends an email to the user with a link to reset their password.
    """
    subject = 'Reset your password'
    reset_link = (
        f'http://localhost:8000/api/auth/reset-password/?token={token}'
    )
    message = (
        f"Click the link to reset your password: {reset_link}"
    )
    send_email(subject, message, [user_email])
