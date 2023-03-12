from ..api import *
from .binding import *

class Parameter:
    def __init__(self, handle):
        self.handle = handle
        self.is_vec2 = inParameterIsVec2(self.handle)

    def __del__(self):
        inParameterDestroy(self.handle)
        self.handle = None

    def uuid(self):
        return inParameterGetUUID(self.handle)
    
    def name(self):
        return inParameterGetName(self.handle)
    
    def get_value(self):
        values = inParameterGetValue(self.handle)
        return values

    def set_value(self, *values):
        inParameterSetValue(self.handle, *values)
    
    def min(self):
        return inParameterGetMin(self.handle)
    
    def max(self):
        return inParameterGetMax(self.handle)
    
    def get_axes(self):
        return inParameterGetAxes(self.handle)
    
    def find_closest_keypoint(self, x, y):
        return inParameterFindClosestKeypoint(self.handle, x, y)
    
    def get_bindings(self):
        return [ParameterBinding(b) for b in inParameterGetBindings(self.handle)]
    
    def get_binding(self, node, name):
        return ParameterBinding(inParameterGetBinding(self.handle, node.handle, name))