from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from CaCatHead.permission.constants import PostPermissions
from CaCatHead.post.models import Post
from CaCatHead.post.serializers import PostSerializer, PostContentSerializer
from CaCatHead.utils import make_response


@api_view()
def list_post(request: Request):
    """
    列出用户可见的所有公告
    """
    posts = Post.objects.filter_user_public(user=request.user, permission=PostPermissions.Read)
    return make_response(posts=PostSerializer(posts, many=True).data)


@api_view()
def list_public_post():
    """
    列出公开的公告
    """
    posts = Post.objects.filter_public()
    return make_response(posts=PostSerializer(posts, many=True).data)


@api_view()
def get_post_content(request: Request, post_id):
    """
    查看公告内容
    """
    post = Post.objects.filter_user_public(user=request.user, id=post_id, permission=PostPermissions.Read).first()
    return make_response(post=PostContentSerializer(post).get_or_raise())


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_post(request: Request):
    """
    创建公告
    """
    return make_response()
