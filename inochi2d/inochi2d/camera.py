from ..api import *

class Camera:
    @classmethod
    def get_current(klass):
        return Camera(api.inCameraGetCurrent())
    
    def __init__(self, handle):
        self.handle = handle
    
    def set_position(self, x, y):
        api.inCameraSetPosition(self.handle, x, y)
    
    def get_position(self):
        return api.inCameraGetPosition(self.handle)
    
    def set_zoom(self, zoom):
        api.inCameraSetZoom(self.handle, zoom)
        
    def get_zoom(self):
        return api.inCameraGetZoom(self.handle)