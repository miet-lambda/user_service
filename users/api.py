from decimal import Decimal
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from django.contrib.auth import get_user_model
from users import serializers



class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = serializers.RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        response_serializer = serializers.UserSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=HTTP_201_CREATED,
            headers=headers
        )




class AddMoneyView(APIView):
    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.AddMoneyInputSerializer

    def post(self, request: Request, user_id):
        cur_user = request.user
        if cur_user.id != user_id:
            return Response(
                {"error": "You can only add money to your own account"},
                status=HTTP_403_FORBIDDEN
            )

        serializer = serializers.AddMoneyInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cur_user.money_balance += Decimal(request.data['amount'])
        cur_user.save()

        response = serializers.UserSerializer(cur_user)
        return Response(response.data)


class RevokeAllTokensView(APIView):
    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request: Request, user_id):
        cur_user = request.user
        if cur_user.id != user_id:
            return Response(
                {"error": "You can only revoke tokens from your own account"},
                status=HTTP_403_FORBIDDEN
            )

        cur_user.token_version += 1
        cur_user.save()

        return Response(
            {"detail": "All tokens revoked successfully"},
            status=HTTP_200_OK
        )


class VersionTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.VersionTokenRefreshSerializer

class VersionTokenVerifyView(TokenVerifyView):
    serializer_class = serializers.VersionTokenVerifySerializer
