"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from interview import views as interview_views
from users import views as user_views
from users.views import CustomLogoutView
from interview.views import main_page
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from users.views import RegisterView, register_page
from django.contrib.auth import views as auth_views
from users.views import CustomLogoutView, logout_confirm_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', interview_views.home_page, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("register/", user_views.register_page, name="register"),
    path('mainpage/', interview_views.main_page, name='mainpage'),
    path('interview/', include('interview.urls')),
    path('api/interview/', include('interview.urls')),
    path('api/users/', include('users.urls')),
    path('api/resume/', include('resume.urls')),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html',success_url='/mainpage/'), name='password_change'),
    path('logout/', CustomLogoutView.as_view(next_page="login"), name='logout'),
    path('logout/confirm/', logout_confirm_view, name='logout_confirm'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('interview.urls')),
]
