"""
This module defines the Contact model for storing contact form submissions.

Classes:
    Contact: Represents a contact form entry with fields for name,
            email, phone number, subject, message, and timestamp.
"""
from django.db import models


class Contact(models.Model):
    """
    Represents a contact message submitted by a user.
    Fields:
        name (CharField): The name of the person submitting the contact form.
        email (EmailField): The email address of the contact.
        phone_number (CharField): The phone number of the contact.
        subject (CharField): The subject of the message (optional).
        message (TextField): The content of the contact message.
        created_at (DateTimeField): The timestamp when the contact was created.
    Methods:
        __str__: Returns a string representation of the contact, including the
                name and subject.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(blank=True, null=True, max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the contact instance,
        combining the name and subject.
        Returns:
            str: A formatted string in the form 'name - subject'.
        """
        return f"{self.name} - {self.subject}"
