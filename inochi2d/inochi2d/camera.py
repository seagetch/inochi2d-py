from ..api import *

class Camera:
    @classmethod
    def get_current(klass):
        return Camera(api.inCameraGetCurrent())
    
    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        inCameraDestroy(self.handle)
        self.handle = None

    @property
    def position(self):
        return api.inCameraGetPosition(self.handle)

    @position.setter
    def position(self, pos):
        api.inCameraSetPosition(self.handle, pos[0], pos[1])

    @property    
    def zoom(self):
        return api.inCameraGetZoom(self.handle)
    
    @zoom.setter
    def zoom(self, zoom):
        api.inCameraSetZoom(self.handle, zoom)

    @property    
    def matrix(self):
        return inCameraGetMatrix(self.handle)
    
    @property
    def screen_to_global(self):
        return inCameraGetScreenToGlobalMatrix(self.handle)
