from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from CaCatHead.post.models import Post
from CaCatHead.post.serializers import PostSerializer, PostContentSerializer


@api_view()
def list_post(request: Request):
    posts = Post.objects.filter(isPublic=True)
    return Response({'status': 'ok', 'posts': PostSerializer(posts, many=True).data})


@api_view()
def get_post(request: Request, post_id):
    posts = Post.objects.filter(isPublic=True, id=post_id).first()
    return Response({'status': 'ok', 'post': PostContentSerializer(posts).data})
