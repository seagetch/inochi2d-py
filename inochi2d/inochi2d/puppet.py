from ..api import *
from .node import *
from .param import *
from .texture import *

class Puppet:

    @classmethod
    def load(klass, path):
        return Puppet(inPuppetLoad(path))

    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        inPuppetDestroy(self.handle)
        self.handle = None

    def update(self):
        inPuppetUpdate(self.handle)

    def draw(self):
        inPuppetDraw(self.handle)

    @property
    def name(self):
        return inPuppetGetName(self.handle)
    
    @property
    def uuid(self):
        return inPuppetGetUUID(self.handle)

    @property
    def root(self):
        return Node(inPuppetGetRootNode(self.handle))
    
    @property
    def parameters(self):
        params = inPuppetGetParameters(self.handle)
        return [Parameter(handle) for handle in params]
    
    @property
    def enable_drivers(self):
        return inPuppetGetEnableDrivers(self.handle)
    
    @enable_drivers.setter
    def enable_drivers(self, value):
        inPuppetSetEnableDrivers(self.handle, value)

    def get_texture_from_id(self, id):
        return Texture(inPuppetGetTexture(self.handle, id))