import json
import sys


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            pass
        cls = type(obj)
        result = {
            '__custom__': True,
            '__module__': cls.__module__,
            '__name__': cls.__name__,
            '__data__': obj.__dict__ if not hasattr(cls, 'to_representation') else obj.to_representation()
        }
        return result


class CustomJSONDecoder(json.JSONDecoder):
    def decode(self, text):
        result = super().decode(text)
        if not isinstance(result, dict) or not result.get('__custom__', False):
            return result
        module = result['__module__']
        if module not in sys.modules:
            __import__(module)
        cls = getattr(sys.modules[module], result['__name__'])
        if hasattr(cls, 'to_object'):
            return cls.to_object(result['data'])
        instance = cls.__new__(cls)
        instance.__dict__.update(result['data'])
        return instance


def dumps(obj):
    """
    Encoder function
    """
    return json.dumps(obj, cls=CustomJSONEncoder)


def loads(obj):
    """
    Decoder function
    """
    return json.loads(obj, cls=CustomJSONDecoder)
