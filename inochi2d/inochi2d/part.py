from ..api import *
from .texture import *
from .node import *
from .drawable import *
import json


class InvalidCast(RuntimeError):
    def __init__(self, obj):
        super(InvalidCast, self).__init__("src must be Node object, but get object of type %s"%type(obj))

class Part(Drawable):
    def __init__(self, src):
        super(Part, self).__init__(src)
        
    def __del__(self):
        pass

    @property
    def textures(self):
        result = inPartGetTextures(self.handle)
        if result is not None:
            return [Texture(tex) for tex in result]
        else:
            return None