import logging

from app.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError

logger = logging.getLogger('view')


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializers class for User model
    """
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "uuid",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer class to register new user
    """
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "uuid",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            'username': {'required': False},
        }

    def validate(self, attrs):
        password = attrs.get("password")

        # Define the desired combination of letters, special characters, and numbers
        has_special_character = False

        # Check each character in the password
        for char in password:
            if not char.isalpha() and not char.isdigit():
                has_special_character = True

        errors = dict()

        # Check the combination and length
        if not has_special_character:
            errors["password"] = [
                "The password must contain at least one special character"
            ]
            raise ValidationError(errors)

        if len(password) < 8:
            errors["password"] = [
                "The password must be at least 8 characters long"]
            raise ValidationError(errors)

        return super().validate(attrs)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializers class for updating user
    """
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "uuid",
            "created_at",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for user detail with minimal information
    """

    class Meta:
        model = User
        fields = (
            "id",
            "uuid",
            "email",
            "first_name",
            "last_name",
        )