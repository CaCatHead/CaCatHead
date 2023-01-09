from rest_framework.decorators import api_view
from rest_framework.request import Request

from CaCatHead.judge.models import JudgeNode
from CaCatHead.judge.serializers import JudgeNodeSerializer
from CaCatHead.utils import make_response


@api_view()
def list_judge_nodes(request: Request):
    judge_nodes = JudgeNode.objects.all()
    return make_response(nodes=JudgeNodeSerializer(judge_nodes, many=True).data)
