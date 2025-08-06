"""
Serializer module for the Contact app.

Defines serializers for handling Contact model data,
including validation and transformation
for API requests and responses.
"""
from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.
    Serializes the following fields:
        - name: The name of the contact person.
        - email: The email address of the contact person.
        - phone_number: The phone number of the contact person.
        - subject: The subject of the contact message.
        - message: The content of the contact message.
    """
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone_number',
            'subject',
            'message'
        ]
