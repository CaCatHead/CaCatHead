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
from django.views.generic import RedirectView

from CaCatHead.contest import views as contest_views
from CaCatHead.judge import views as judge_views
from CaCatHead.post import views as post_views
from CaCatHead.problem import views as problem_views
from CaCatHead.user import views as user_views

admin.site.site_header = "CaCatHead 管理后台"
admin.site.site_title = 'CaCatHead 管理后台'

urlpatterns = [
    # admin usage
    path('admin/login/', RedirectView.as_view(url='/login', permanent=False), name='admin_login'),
    path('admin/logout/', RedirectView.as_view(url='/api/auth/logout', permanent=False), name='admin_logout'),
    path('admin/', admin.site.urls),
    # test ping
    path('api/ping', user_views.ping),
    path('api/home', user_views.get_home_info),
    path('api/prime/<str:text>', user_views.is_prime),
    path('api/sync', user_views.sync_timestamp),
    # user auth
    path('api/auth/register', user_views.user_register),
    path('api/auth/login', user_views.UserLoginView.as_view()),
    path('api/auth/logout', user_views.UserLogoutView.as_view()),
    # path('api/auth/logoutall', auth_views.LogoutAllView.as_view()),
    # user profile
    path('api/user/profile', user_views.current_user_profile),
    path('api/user/profile/<str:username>', user_views.get_user_info),
    # judge node
    path('api/judge/node', judge_views.list_judge_nodes),
    path('api/judge/nodes', judge_views.list_judge_nodes),
    # post
    path('api/posts', post_views.list_post),
    path('api/posts/home', post_views.list_public_home_post),
    path('api/posts/public', post_views.list_public_post),
    path('api/post/<int:post_id>', post_views.get_post_content),
    path('api/post/<int:post_id>/edit', post_views.edit_post),
    # path('api/post/<int:post_id>/permission'),
    path('api/post', post_views.create_post),
    # polygon
    path('api/polygon/upload', problem_views.upload_problem),  # 上传题目
    path('api/polygon/create', problem_views.create_problem),  # 手动创建题目
    path('api/polygon/<int:problem_id>', problem_views.get_polygon_problem),  # 手动创建题目
    path('api/polygon/<int:problem_id>/edit', problem_views.edit_polygon_problem),  # 编辑题目
    path('api/polygon/<int:problem_id>/export', problem_views.export_polygon_problem_zip),  # 导出题目 zip
    path('api/polygon/<int:problem_id>/upload', problem_views.edit_polygon_problem_by_upload),  # 上压缩包编辑题目
    path('api/polygon/<int:problem_id>/submit', problem_views.submit_polygon_problem),  # 提交题目代码
    path('api/polygon/<int:problem_id>/submissions', problem_views.list_polygon_problem_submissions),  # 提交题目代码
    path('api/polygon/<int:problem_id>/checker', problem_views.upload_polygon_problem_checker),  # 更新题目 checker
    path('api/polygon/<int:problem_id>/permission', problem_views.PolygonPermission.as_view()),  # 将创建的题目向他人授权
    path('api/polygon/own', problem_views.list_polygon_problems),  # 用户上传的题目列表
    path('api/polygon/submissions', problem_views.list_polygon_submissions),  # 获取所有提交状态
    path('api/polygon/submission/<int:submission_id>', problem_views.get_polygon_submission),  # 获取提交状态详情
    path('api/polygon/submission/<int:submission_id>/rejudge', problem_views.rejudge_polygon_problem),  # 重测提交
    # problem
    path('api/repos', problem_views.list_repos),  # 列出所有公开的题库
    path('api/repo/<int:repo_id>', problem_views.list_repo_problems),  # 获取题库信息
    path('api/repo/<int:repo_id>/permission', problem_views.RepoPermission.as_view()),  # 将题库向他人授权
    path('api/repo/<int:repo_id>/problems', problem_views.list_repo_problems),  # 查看题库中的题目列表
    path('api/repo/<int:repo_id>/problems/add/<int:problem_id>', problem_views.add_repo_problem),  # 编辑题库中的题目列表
    path('api/repo/<int:repo_id>/problems/delete/<int:problem_id>', problem_views.delete_repo_problem),  # 编辑题库中的题目列表
    path('api/repo/<int:repo_id>/problem/<int:problem_id>', problem_views.get_repo_problem_content),  # 查看题目内容
    path('api/repo/<int:repo_id>/problem/<int:problem_id>/submit', problem_views.submit_repo_problem_code),  # 提交代码
    path('api/repo/<int:repo_id>/problem/<int:problem_id>/edit', problem_views.edit_repo_problem),  # 编辑题目
    path('api/repo/<int:repo_id>/submissions', problem_views.list_repo_submissions),  # 获取所有提交状态
    path('api/repo/<int:repo_id>/submission/<int:submission_id>', problem_views.get_repo_submission),  # 获取提交状态详情
    # contest
    path('api/contests', contest_views.list_contests),  # 列出所有比赛
    path('api/contest', contest_views.create_contest),  # 创建比赛
    path('api/contest/<int:contest_id>/edit', contest_views.edit_contest),  # 编辑比赛信息
    path('api/contest/<int:contest_id>/registrations', contest_views.ContestRegistrationView.as_view()),  # 编辑比赛人员列表
    path('api/contest/<int:contest_id>/registrations/import', contest_views.import_registrations),  # 生成比赛账号密码
    # path('api/contest/<int:contest_id>/permission'),  # 将比赛向他人授权
    path('api/contest/<int:contest_id>/register', contest_views.user_register_contest),  # 参加比赛
    path('api/contest/<int:contest_id>/unregister', contest_views.user_unregister_contest),  # 取消注册比赛
    path('api/contest/<int:contest_id>/public', contest_views.get_contest_public),  # 查看比赛详情, 包括题目内容
    path('api/contest/<int:contest_id>/content', contest_views.get_contest),  # 查看比赛详情, 包括题目内容
    path('api/contest/<int:contest_id>/problem/<int:problem_id>/submit', contest_views.user_submit_code),  # 提交代码
    path('api/contest/<int:contest_id>/problem/<int:problem_id>/prepare', contest_views.prepare_problem),  # 预热题目
    path('api/contest/<int:contest_id>/status', contest_views.user_list_own_submissions),  # 查看比赛个人提交
    path('api/contest/<int:contest_id>/submission/<int:submission_id>',
         contest_views.user_view_submission),  # 获取比赛提交状态详情
    path('api/contest/<int:contest_id>/submission/<int:submission_id>/rejudge',
         contest_views.rejudge_contest_submission),  # 重测某个提交
    path('api/contest/<int:contest_id>/submission/<int:submission_id>/delete',
         contest_views.delete_contest_submission),  # 删除某个提交
    path('api/contest/<int:contest_id>/submissions', contest_views.user_view_all_submissions),  # 查看比赛所有提交
    path('api/contest/<int:contest_id>/standings', contest_views.user_view_standings),  # 查看比赛排行榜
    path('api/contest/<int:contest_id>/rating', contest_views.RatingView.as_view()),  # 更新比赛 Rating
    path('api/contest/<int:contest_id>/standings/export', contest_views.admin_export_standings),  # 导出比赛数据
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
