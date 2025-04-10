from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api import (
    CreateUserView,
    AddMoneyView,
    RevokeAllTokensView,
    VersionTokenVerifyView,
    VersionTokenRefreshView,
)


urlpatterns = [
    path(
        "users/<int:user_id>/add_money/",
        AddMoneyView.as_view(),
        name="add-money",
    ),
    path(
        "users/<int:user_id>/revoke_tokens/",
        RevokeAllTokensView.as_view(),
        name="revoke-tokens",
    ),
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/verify/", VersionTokenVerifyView.as_view(), name="token_verify"),
    path(
        "token/refresh/", VersionTokenRefreshView.as_view(), name="token_refresh"
    ),
]
