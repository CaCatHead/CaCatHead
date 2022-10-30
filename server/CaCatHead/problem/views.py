from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from CaCatHead.core.decorators import HasPolygonPermission


# Polygon
@api_view()
@permission_classes([HasPolygonPermission])
def create_problem(request):
    """
    创建题目
    """
    return Response({"status": "ok"})


@api_view()
@permission_classes([HasPolygonPermission])
def upload_problem(request):
    """
    创建题目
    """
    return Response({"status": "ok"})


@api_view()
@permission_classes([HasPolygonPermission])
def edit_problem(request):
    """
    编辑题目
    """
    return Response({"status": "ok"})


@api_view()
@permission_classes([HasPolygonPermission])
def list_created_problems(request):
    """
    列出自己创建的题目
    """
    return Response({"status": "ok"})


# 题库
@api_view()
def list_repos(request):
    """
    列出所有题库
    """
    return Response({"status": "ok"})


@api_view
def list_repo_problems(request):
    """
    列出题库中的所有题目
    """
    return Response({"status": "ok"})
