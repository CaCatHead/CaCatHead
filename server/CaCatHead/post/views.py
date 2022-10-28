from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from CaCatHead.post.models import Post
from CaCatHead.post.serializers import PostSerializer, PostContentSerializer


@api_view()
def list_post(request: Request):
    posts = Post.objects.filter_user(user=request.user)
    return Response({'status': 'ok', 'posts': PostSerializer(posts, many=True).data})


@api_view()
def get_post(request: Request, post_id):
    post = Post.objects.filter_user(user=request.user, id=post_id).first()
    if post is not None:
        return Response({'status': 'ok', 'post': PostContentSerializer(post).data})
    else:
        return Response({'status': 'error', 'detail': f'未找到编号为 {post_id} 的公告'})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_post(request: Request):
    return Response({'status': 'ok'})
