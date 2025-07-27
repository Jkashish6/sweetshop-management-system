from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from api.models import CustomUser  # ✅ FIXED: use your custom model

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser  # ✅ FIXED
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():  # ✅ FIXED
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():  # ✅ FIXED
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)  # ✅ FIXED


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )
        if not user:
            raise AuthenticationFailed("Invalid username or password")
        data["user"] = user
        return data
