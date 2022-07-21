from ..api import *

class Camera:
    @classmethod
    def get_current(klass):
        return Camera(api.inCameraGetCurrent())
    
    def __init__(self, handle):
        self.handle = handle
    
    def set_position(self, x, y):
        api.inCameraSetPosition(self.handle, x, y)
    
    def set_zoom(self, zoom):
        api.inCameraSetZoom(self.handle, zoom)