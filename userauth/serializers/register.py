"""
Serializers for user registration in the user authentication module.
This module defines the RegisterSerializer class,\
    which extends the AccountSerializer
to handle user registration, including password validation and confirmation.
Classes:
    RegisterSerializer: Serializer for registering new users, ensuring password
    confirmation and validation according to Django's password policies.
"""
from rest_framework import serializers
from account.models import Account
from account.serializers import AccountSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegisterSerializer(AccountSerializer):
    """
    Serializer for registering a new user account.
    Inherits from AccountSerializer and adds password and confirm_password
    fields with validation. Ensures that the password and confirm_password
    fields match and that the password meets Django's password validation
    requirements. The password fields are write-only and must be between 8
    and 128 characters. On successful validation, creates a new Account
    instance using the provided data.
    """
    # Making sure that the password is at least 8 characters long,
    # and no longer than 128 and can't be read by user.
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True,
        required=True
    )
    confirm_password = serializers.CharField(
        max_length=128, min_length=8, write_only=True,
        required=True
    )

    class Meta:
        model = Account
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'address', 'city', 'state', 'date_of_birth', 'is_verified',
            "password",
            'confirm_password'
        ]

    def validate(self, attrs):
        """
        Validates the provided password and confirm_password fields.
        Ensures that the password and confirm_password fields match.
        If they do not,
        raises a ValidationError with an appropriate message.
        Also validates the
        password using Django's password validators,
        raising a ValidationError if
        the password does not meet the required criteria.
        Args:
            attrs (dict): The input data containing at least\
                'password' and 'confirm_password' keys.
        Returns:
            dict: The validated attributes if all checks pass.
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {
                    'confirm_password': 'Passwords do not match.'
                }
            )
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError(
                {
                    'password': list(e.messages)
                }
            )
        return attrs

    def create(self, validated_data):
        """
        Creates a new user account using the validated registration data.

        Args:
            validated_data (dict): The validated data from the
                registration serializer, including user credentials.

        Returns:
            Account: The newly created user account instance.

        Side Effects:
            Removes the 'confirm_password' field from the validated data
            before creating the user.

        Prints:
            The validated data to the console for debugging purposes.
        """
        print("VALIDATED DATA:", validated_data)
        validated_data.pop('confirm_password')
        return Account.objects.create_user(**validated_data)
