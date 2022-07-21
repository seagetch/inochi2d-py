from ..api import *

class Viewport:
    @classmethod
    def set(klass, width, height):
        api.inViewportSet(width, height)
    
    @classmethod
    def get(klass):
        return api.inViewportGet()