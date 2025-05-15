from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from account.serializers import AccountSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        
        if not self.user:
            raise serializers.ValidationError("No active account found with the given credentials")
        refresh = self.get_token(self.user) 
        
        # If using default username to login, just call super().validate
        data['user'] = AccountSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        
        return data
