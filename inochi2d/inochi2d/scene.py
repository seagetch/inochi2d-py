from ..api import *

class Scene:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def __enter__(self):
        api.inSceneBegin()
        
    def __exit__(self, exc_type, exc_value, traceback):
        api.inSceneEnd()
        api.inSceneDraw(self.x, self.y, self.w, self.h)