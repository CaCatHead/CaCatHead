import json
import logging
import sys

logger = logging.getLogger(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            logger.info('call default')
            logger.info(obj)
            return super().default(obj)
        except TypeError:
            logger.info('type error')
            pass
        cls = type(obj)
        return {
            '__custom__': True,
            '__module__': cls.__module__,
            '__name__': cls.__name__,
            '__data__': obj.__dict__ if not hasattr(cls, 'to_representation') else obj.to_representation()
        }


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if not isinstance(obj, dict) or not obj.get('__custom__', False):
            return obj
        module = obj['__module__']
        if module not in sys.modules:
            __import__(module)
        cls = getattr(sys.modules[module], obj['__name__'])
        if hasattr(cls, 'to_object'):
            return cls.to_object(obj['__data__'])
        else:
            instance = cls.__new__(cls)
            instance.__dict__.update(obj['__data__'])
            return instance


def dumps(obj):
    """
    Custom JSON encoder function
    """
    try:
        text = json.dumps(obj, cls=CustomJSONEncoder)
        return text
    except Exception as ex:
        logger.exception(ex)
        raise ex


def loads(s, decode_bytes=True):
    """
    Custom JSON decoder function
    """
    if isinstance(s, memoryview):
        s = s.tobytes().decode('utf-8')
    elif isinstance(s, bytearray):
        s = s.decode('utf-8')
    elif decode_bytes and isinstance(s, bytes):
        s = s.decode('utf-8')
    try:
        return json.loads(s, cls=CustomJSONDecoder)
    except Exception as ex:
        logger.exception(ex)
        raise ex
