from ..api import *

class Puppet:

    @classmethod
    def load(klass, path):
        return Puppet(inPuppetLoad(path))

    def __init__(self, handle):
        self.handle = handle
        
    def update(self):
        inPuppetUpdate(self.handle)

    def draw(self):
        inPuppetDraw(self.handle)
