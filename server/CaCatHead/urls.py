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
from django.contrib import admin
from django.urls import path
from knox import views as knox_views

from CaCatHead.post import views as post_views
from CaCatHead.problem import views as problem_views
from CaCatHead.user import views as user_views

admin.site.site_header = "CaCatHead 管理后台"
admin.site.site_title = 'CaCatHead 管理后台'

urlpatterns = [
    # admin usage
    path('admin/', admin.site.urls),
    # test ping
    path('api/ping', user_views.ping),
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
    path('api/post', post_views.create_post),
    # polygon
    path('api/polygon/upload', problem_views.upload_problem),  # 上传题目
    path('api/polygon/create', problem_views.create_problem),  # 手动创建题目
    path('api/polygon/<int:problem_id>', problem_views.get_created_problems),  # 手动创建题目
    path('api/polygon/<int:problem_id>/edit', problem_views.edit_created_problem),  # 编辑题目
    path('api/polygon/<int:problem_id>/submit', problem_views.submit_created_problem),  # 提交题目代码
    # path('api/polygon/<int:problem_id>/permission'),  # 将创建的题目向他人授权
    path('api/polygon/own', problem_views.list_created_problems),  # 用户上传的题目列表
    path('api/polygon/submissions', problem_views.list_created_problem_submissions),  # 获取所有提交状态
    path('api/polygon/submission/<int:submission_id>', problem_views.get_created_problem_submission),  # 获取提交状态详情
    # problem
    path('api/repos', problem_views.list_repos),  # 列出所有公开的题库
    path('api/repo/<int:repo_id>/problems', problem_views.list_repo_problems),  # 查看题库中的题目列表
    # path('api/repo/<int:repo_id>/permission'),  # 将题库向他人授权
    # path('api/repo/<int:repo_id>/problems/edit'),  # 编辑题库中的题目列表
    # path('api/repo/<int:repo_id>/problem/<int:problem_id>'),  # 查看题目内容
    # path('api/repo/<int:repo_id>/problem/<int:problem_id>/submit'),  # 提交代码
    # path('api/repo/<int:repo_id>/problem/<int:problem_id>/edit'),  # 编辑题目
    # path('api/repo/<int:repo_id>/submissions'),  # 获取所有提交状态
    # path('api/repo/<int:repo_id>/submission/<int:submission_id>'),  # 获取提交状态详情
]

# if settings.DEBUG:
#     urlpatterns += [path('openapi/', get_schema_view(title="CaCatHead",
#                                                      description="API for all things …",
#                                                      version="1.0.0"), name='openapi-schema')]
