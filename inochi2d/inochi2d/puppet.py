from ..api import *
from .node import *
from .param import *

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

    def name(self):
        return inPuppetGetName(self.handle)
    
    def uuid(self):
        return inPuppetGetUUID(self.handle)

    def root(self):
        return Node(inPuppetGetRootNode(self.handle))
    
    def parameters(self):
        params = inPuppetGetParameters(self.handle)
        return [Parameter(handle) for handle in params]