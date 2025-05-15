from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        source="public_id",
        read_only=True,
        format="hex"
    )
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'address', 'city', 'state', 'date_of_birth', 'is_active',
            'is_superuser', 'is_staff', 'date_joined', 'last_login'
        ]
        read_only_field = ['is_active', 'is_superuser', 'is_staff']
