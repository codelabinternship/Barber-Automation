"""
URL configuration for barber project.

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
from django.urls import path
from django.http import JsonResponse

from barber_app.views import (
    RegisterView,
    LoginView,
    ResetPasswordView,
    MeView,
    DevPasswordResetView,
    ProfileView,
    CreateAdminBySuperadminView,
)


def home_view(request):
    return JsonResponse({'message': 'Welcome to Barber API'})

from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from barber_app.views import CreateAdminBySuperadminView
from barber_app.views import ProfileView
from barber_app.views import GetMeView

from barber_app.views import MyView






schema_view = get_schema_view(
    openapi.Info(
        title="Barber API",
        default_version='v1',
        description="API documentation for Barber app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@friends.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('home/', home_view, name='home-url'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my-view/', MyView.as_view(), name='my-view'),
    path('get-me/', GetMeView.as_view(), name='get-me'),


    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='auth-reset-password'),
    path('auth/get-me/', MeView.as_view(), name='auth-get-me'),
    path('auth/dev/reset-password/<int:user_id>/', DevPasswordResetView.as_view(), name='dev-reset-password'),
    path('auth/profile/', ProfileView.as_view(), name='auth-profile'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

