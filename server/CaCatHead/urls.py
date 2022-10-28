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
from django.contrib import admin

from knox import views as knox_views

from CaCatHead.user import views as user_views
from CaCatHead.post import views as post_views

urlpatterns = [
    # admin usage
    path('admin/', admin.site.urls),
    # test ping
    path('api/hello/', user_views.hello_world),
    # user auth
    path('api/auth/register', user_views.user_register),
    path('api/auth/login', user_views.UserLoginView.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view()),
    path('api/auth/logoutall', knox_views.LogoutAllView.as_view()),
    # user profile
    path('api/user/profile', user_views.current_user_profile),
    # post
    path('api/posts', post_views.list_post),
    path('api/posts/public', post_views.list_public_post),
    path('api/post/<int:post_id>', post_views.get_post_content),
    path('api/post', post_views.create_post)
]

# if settings.DEBUG:
#     urlpatterns += [path('openapi/', get_schema_view(title="CaCatHead",
#                                                      description="API for all things …",
#                                                      version="1.0.0"), name='openapi-schema')]
