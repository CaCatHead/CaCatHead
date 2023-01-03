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

from CaCatHead.contest import views as contest_views
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
    # path('api/post/<int:post_id>/edit'),
    # path('api/post/<int:post_id>/permission'),
    path('api/post', post_views.create_post),
    # polygon
    path('api/polygon/upload', problem_views.upload_problem),  # 上传题目
    path('api/polygon/create', problem_views.create_problem),  # 手动创建题目
    path('api/polygon/<int:problem_id>', problem_views.get_polygon_problem),  # 手动创建题目
    path('api/polygon/<int:problem_id>/edit', problem_views.edit_polygon_problem),  # 编辑题目
    path('api/polygon/<int:problem_id>/upload', problem_views.edit_polygon_problem_by_upload),  # 上压缩包编辑题目
    path('api/polygon/<int:problem_id>/submit', problem_views.submit_polygon_problem),  # 提交题目代码
    path('api/polygon/<int:problem_id>/submissions', problem_views.list_polygon_problem_submissions),  # 提交题目代码
    path('api/polygon/<int:problem_id>/permission', problem_views.PolygonPermission.as_view()),  # 将创建的题目向他人授权
    path('api/polygon/own', problem_views.list_polygon_problems),  # 用户上传的题目列表
    path('api/polygon/submissions', problem_views.list_polygon_submissions),  # 获取所有提交状态
    path('api/polygon/submission/<int:submission_id>', problem_views.get_polygon_submission),  # 获取提交状态详情
    # problem
    path('api/repos', problem_views.list_repos),  # 列出所有公开的题库
    path('api/repo/<int:repo_id>/problems', problem_views.list_repo_problems),  # 查看题库中的题目列表
    path('api/repo/<int:repo_id>/permission', problem_views.RepoPermission.as_view()),  # 将题库向他人授权
    path('api/repo/<int:repo_id>/add/<int:problem_id>', problem_views.add_repo_problem),  # 编辑题库中的题目列表
    path('api/repo/<int:repo_id>/delete/<int:problem_id>', problem_views.delete_repo_problem),  # 编辑题库中的题目列表
    path('api/repo/<int:repo_id>/problem/<int:problem_id>', problem_views.get_repo_problem_content),  # 查看题目内容
    path('api/repo/<int:repo_id>/problem/<int:problem_id>/submit', problem_views.submit_repo_problem_code),  # 提交代码
    # path('api/repo/<int:repo_id>/problem/<int:problem_id>/edit'),  # 编辑题目
    path('api/repo/<int:repo_id>/submissions', problem_views.list_repo_submissions),  # 获取所有提交状态
    path('api/repo/<int:repo_id>/submission/<int:submission_id>', problem_views.get_repo_submission),  # 获取提交状态详情
    # contest
    path('api/contests', contest_views.list_contests),  # 列出所有比赛
    path('api/contest', contest_views.create_contest),  # 创建比赛
    path('api/contest/<int:contest_id>/edit', contest_views.edit_contest),  # 编辑比赛信息
    # path('api/contest/<int:contest_id>/problems/edit'),  # 编辑比赛题目列表
    # path('api/contest/<int:contest_id>/contestants/edit'),  # 编辑比赛人员列表
    # path('api/contest/<int:contest_id>/permission'),  # 将比赛向他人授权
    # path('api/contest/<int:contest_id>/register'),  # 参加比赛
    path('api/contest/<int:contest_id>/content', contest_views.get_contest),  # 查看比赛详情, 包括题目内容
    # path('api/contest/<int:contest_id>/problem/<int:problem_id>/submit'),  # 提交代码
    # path('api/contest/<int:contest_id>/submissions'),  # 查看比赛所有提交
    # path('api/contest/<int:contest_id>/submission/<int:submission_id>'),  # 获取比赛提交状态详情
    # path('api/contest/<int:contest_id>/standings'),  # 查看比赛排行榜
    # path('api/contest/<int:contest_id>/export'),  # 导出比赛数据
    # team
    # path('api/teams'),  # 列出自己参加的团队
    # path('api/team'),  # 创建团队
    # path('api/team/<int:team_id>'),  # 查看团队
    # path('api/team/<int:team_id>/edit'),  # 编辑团队信息
]

# if settings.DEBUG:
#     urlpatterns += [path('openapi/', get_schema_view(title="CaCatHead",
#                                                      description="API for all things …",
#                                                      version="1.0.0"), name='openapi-schema')]
