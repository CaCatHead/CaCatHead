import platform
import subprocess

from django.utils import timezone

from CaCatHead.config import cacathead_config
from CaCatHead.judge.models import JudgeNode


def get_judge_node(name: str):
    node = JudgeNode.objects.filter(name=name).first()
    if node is not None:
        return node
    else:
        node = JudgeNode(name=name, updated=timezone.now())
        node.save()
        return node


def get_system_info():
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'architecture': platform.architecture(),
        'processor': platform.processor()
    }


def get_compiler_version():
    gcc = subprocess.check_output(['gcc', '--version'], encoding='UTF-8')
    gpp = subprocess.check_output(['g++', '--version'], encoding='UTF-8')
    java = subprocess.check_output(['java', '-version'], encoding='UTF-8', stderr=subprocess.STDOUT)
    return {
        'gcc': gcc,
        'g++': gpp,
        'java': java
    }


def handle_ping():
    node_name = cacathead_config.judge.name
    node = get_judge_node(node_name)
    node.active = True
    node.information = {
        'platform': get_system_info(),
        'compiler': get_compiler_version()
    }
    node.updated = timezone.now()
    node.save()
