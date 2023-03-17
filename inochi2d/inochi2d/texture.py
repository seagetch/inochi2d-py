from ..api import *
from .binding import *

class Texture:
    def __init__(self, texture):
        self.handle = texture
    
    def __del__(self):
        inTextureDestroy(self.handle)
        self.handle = None

    def size(self):
        return inTextureGetSize(self.handle)
    
    def center(self):
        return inTextureGetCenter(self.handle)
    
    def width(self):
        return inTextureGetWidth(self.hendle)
    
    def height(self):
        return inTextureGetHeight(self.handle)
    
    def channels(self):
        return inTextureGetChannels(self.handle)

    def set_data(self, buffer):
        inTextureSetData(self.handle, buffer, len(buffer))
    
    def get_data(self, unmultiply = False):
        buffer, length = inTextureGetTextureData(self.handle, unmultiply)
        return buffer, length

    def bind(self):
        inTextureBind(self.handle)

    def dispose(self):
        inTextureDispose(self.handle)