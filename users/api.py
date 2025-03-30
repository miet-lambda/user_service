from decimal import Decimal
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from .serializers import UserSerializer
from users import serializers


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = UserSerializer


class AddMoneyView(APIView):
    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, user_id):
        cur_user = request.user
        if cur_user.id != user_id and not cur_user.is_staff:
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