from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from CaCatHead.core.decorators import func_validate_request
from CaCatHead.permission.constants import PostPermissions
from CaCatHead.post.models import Post, PostContent
from CaCatHead.post.serializers import PostSerializer, PostContentSerializer, CreatePostPayloadSerializer
from CaCatHead.utils import make_response


@api_view()
def list_post(request: Request):
    """
    列出用户可见的所有公告
    """
    posts = Post.objects.filter_user_public(user=request.user, permission=PostPermissions.Read)
    return make_response(posts=PostSerializer(posts, many=True).data)


@api_view()
def list_public_post(request: Request):
    """
    列出公开的公告
    """
    posts = Post.objects.filter_public()
    return make_response(posts=PostContentSerializer(posts, many=True).data)


@api_view()
def list_public_home_post(request: Request):
    """
    列出首页的公告
    """
    posts = Post.objects.filter_public().filter(is_home=True)
    return make_response(posts=PostContentSerializer(posts, many=True).data)


@api_view()
def get_post_content(request: Request, post_id):
    """
    查看公告内容
    """
    post = Post.objects.filter_user_public(user=request.user, id=post_id, permission=PostPermissions.Read).first()
    return make_response(post=PostContentSerializer(post).get_or_raise())


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required('post.add_post', raise_exception=True)
@func_validate_request(CreatePostPayloadSerializer)
def edit_post(request: Request, post_id: int):
    """
    编辑公告
    """
    post: Post = Post.objects.filter_user_permission(user=request.user, permission=PostPermissions.Edit).filter(
        id=post_id).first()
    if post is not None:
        post.title = request.data['title']
        post.content.content = request.data['content']
        if request.user.is_superuser:
            if 'is_public' in request.data:
                post.is_public = request.data['is_public']
            if 'is_home' in request.data:
                post.is_home = request.data['is_home']
        post.save()
        post.content.save()
        return make_response(post=PostContentSerializer(post).get_or_raise())
    else:
        raise NotFound(detail='未找到公告')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required('post.add_post', raise_exception=True)
@func_validate_request(CreatePostPayloadSerializer)
def create_post(request: Request):
    """
    创建公告
    """
    post = Post(title=request.data['title'], sort_time=timezone.now(), is_public=False, owner=request.user)
    if request.user.is_superuser:
        if 'is_public' in request.data:
            post.is_public = request.data['is_public']
        if 'is_home' in request.data:
            post.is_home = request.data['is_home']
    post.save()
    post_content = PostContent(post=post, content=request.data['content'])
    post_content.save()
    return make_response(post=PostContentSerializer(post).get_or_raise())
