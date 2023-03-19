from ..api import *
from .binding import *

class Texture:
    def __init__(self, texture):
        self.handle = texture
    
    def __del__(self):
        inTextureDestroy(self.handle)
        self.handle = None

    @property
    def size(self):
        return inTextureGetSize(self.handle)
    
    @property
    def center(self):
        return inTextureGetCenter(self.handle)
    
    @property
    def width(self):
        return inTextureGetWidth(self.hendle)
    
    @property
    def height(self):
        return inTextureGetHeight(self.handle)
    
    @property
    def channels(self):
        return inTextureGetChannels(self.handle)

    def get_data(self, unmultiply = False):
        return inTextureGetTextureData(self.handle, unmultiply)

    @property
    def data(self):
        return self.get_data()

    @data.setter
    def data(self, buffer):
        inTextureSetData(self.handle, buffer)
    
    def bind(self):
        inTextureBind(self.handle)

    def dispose(self):
        inTextureDispose(self.handle)