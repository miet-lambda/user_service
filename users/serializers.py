from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)



UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("id", "login", "money_balance")

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            **validated_data
        )
        return user

    class Meta:
        model = UserModel
        fields = ("login", "password")


class AddMoneyInputSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=1000,decimal_places=100)
    def validate_amount(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError("The value must be positive")
        return value


class VersionTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["version"] = user.token_version
        return token


class VersionTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.token_class(attrs["refresh"])
        user_id = refresh.payload.get("user_id")
        try:
            user = UserModel.objects.get(id=user_id)
            if refresh.payload.get("version") != user.token_version:
                raise exceptions.AuthenticationFailed("Token revoked")
        except UserModel.DoesNotExist as e:
            raise exceptions.AuthenticationFailed(f"User not found: {e}")

        return data


class VersionTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        user_id = token.payload.get("user_id")
        if user_id:
            try:
                user = UserModel.objects.get(id=user_id)
                if token.payload.get("version") != user.token_version:
                    raise exceptions.AuthenticationFailed("Token revoked")
            except UserModel.DoesNotExist as e:
                raise exceptions.AuthenticationFailed(f"User not found: {e}")

        return {}
