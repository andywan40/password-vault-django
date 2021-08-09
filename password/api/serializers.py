from rest_framework import serializers
from password.models import Password

class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Password
        fields = ['id', 'account', 'name', 'email','website', 'username', 'password', 'description', 'notes', 'is_favorite', 'date_added', 'updated_at']