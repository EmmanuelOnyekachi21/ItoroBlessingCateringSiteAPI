"""
Custom serializer for user login using JWT authentication.

This serializer extends the `TokenObtainPairSerializer` from
`rest_framework_simplejwt` to provide additional validation and response
customization during user login.

Features:
- Validates user credentials and ensures the user account is active.
- Checks if the user's email is verified before allowing login.
- Returns JWT refresh and access tokens upon successful authentication.
- Serializes and includes user data in the response using
    `AccountSerializer`.
- Optionally updates the user's last login timestamp if configured.

Raises:
        serializers.ValidationError: If the user is not found or the email is
        not verified.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from account.serializers import AccountSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for handling user login and JWT token generation.

    Extends `TokenObtainPairSerializer` to authenticate users and provide
    JWT access and refresh tokens upon successful login. Performs
    additional checks to ensure the user exists and their email is
    verified before issuing tokens. On successful authentication, returns
    serialized user data along with the tokens. Optionally updates the
    user's last login timestamp if configured.

    Raises:
        serializers.ValidationError: If no active account is found with
        the provided credentials or if the user's email is not verified.
    
    """
    def validate(self, attrs):
        """
        Validates user login credentials and returns authentication tokens.
        This method checks if the user exists and is verified. If validation
        passes, it generates refresh and access tokens for the user, serialize
        the user data, and updates the last login timestamp if configured.
        Args:
            attrs (dict): The input data containing login credentials.
        Returns:
            dict: A dictionary containing serialized user data, refresh token,
            and access token.
        Raises:
            serializers.ValidationError: If the user does not exist or the
            email is not verified.
        """
        data = super().validate(attrs)

        
        if not self.user:
            raise serializers.ValidationError("No active account found with the given credentials")
        
        if not self.user.is_verified:
            raise serializers.ValidationError("Email is not verified.")

        refresh = self.get_token(self.user) 
        
        # If using default username to login, just call super().validate
        data['user'] = AccountSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        
        return data
