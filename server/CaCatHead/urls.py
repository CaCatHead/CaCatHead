"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.contrib import admin

from rest_framework.schemas import get_schema_view
from knox import views as knox_views

from CaCatHead.users import views as users_views

urlpatterns = [
    # admin usage
    path('admin/', admin.site.urls),
    # test ping
    path('hello/', users_views.hello_world),
    # user auth
    path('auth/register', users_views.user_register),
    path('auth/login', users_views.UserLoginView.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view()),
    path('auth/logoutall', knox_views.LogoutAllView.as_view()),
    # user profile
    path('user/profile', users_views.current_user_profile)
]

# if settings.DEBUG:
#     urlpatterns += [path('openapi/', get_schema_view(title="CaCatHead",
#                                                      description="API for all things …",
#                                                      version="1.0.0"), name='openapi-schema')]
