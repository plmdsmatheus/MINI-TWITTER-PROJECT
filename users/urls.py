from django.urls import path
from rest_framework.simplejwt import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, UserDetailView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("me/", UserDetailView.as_view(), name="user-profile"),
]