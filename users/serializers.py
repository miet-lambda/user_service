from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework import exceptions

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            login=validated_data["login"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "login", "password", "money_balance")


class AddMoneyInputSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


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
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

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
            except UserModel.DoesNotExist:
                raise exceptions.AuthenticationFailed("User not found")

        return {}
