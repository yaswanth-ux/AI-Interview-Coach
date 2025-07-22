# users/urls.py
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import dashboard_view
from .views import register_page
from .views import CustomLogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('delete/', views.delete_account, name='account_delete'),
]

