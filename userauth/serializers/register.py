from rest_framework import serializers
from account.models import Account
from account.serializers import AccountSerializer


class RegisterSerializer(AccountSerializer):
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
            'address', 'city', 'state', 'date_of_birth', "password",
            'confirm_password'
        ]
    
    def validate(self, attrs):
        # return super().validate(attrs)
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {
                    'confirm_password': 'Passwords do not match.'
                }
            )
        return attrs
    
    def create(self, validated_data):
        print("VALIDATED DATA:", validated_data)
        validated_data.pop('confirm_password')
        return Account.objects.create_user(**validated_data)

