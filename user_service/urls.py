"""
URL configuration for user_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView


from users.api import CreateUserView, AddMoneyView, RevokeAllTokensView, VersionTokenVerifyView, VersionTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/users/<int:user_id>/add_money/', AddMoneyView.as_view(), name='add-money'),
    path('api/v1/users/<int:user_id>/revoke_tokens/', RevokeAllTokensView.as_view(), name='revoke-tokens'),

    path('api/v1/register/', CreateUserView.as_view(), name='register'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/verify/', VersionTokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/token/refresh/', VersionTokenRefreshView.as_view(), name='token_refresh'),
]
