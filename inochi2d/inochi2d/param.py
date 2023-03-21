from ..api import *
from .binding import *

class Parameter:
    def __init__(self, handle):
        self.handle = handle
        self.is_vec2 = inParameterIsVec2(self.handle)

    def __del__(self):
        inParameterDestroy(self.handle)
        self.handle = None

    @property
    def uuid(self):
        return inParameterGetUUID(self.handle)
    
    @property
    def name(self):
        return inParameterGetName(self.handle)
    
    @property
    def value(self):
        values = inParameterGetValue(self.handle)
        return values

    @value.setter
    def value(self, values):
        inParameterSetValue(self.handle, *values)
    
    @property
    def min(self):
        return inParameterGetMin(self.handle)
    
    @property
    def max(self):
        return inParameterGetMax(self.handle)
    
    @property
    def axes(self):
        return inParameterGetAxes(self.handle)
    
    def find_closest_keypoint(self, x = None, y = None):
        if x is None or y is None:
            return inParameterFindClosestKeypointAtCurrent(self.handle)
        else:
            return inParameterFindClosestKeypoint(self.handle, x, y)
    
    @property
    def bindings(self):
        return [ParameterBinding(b) for b in inParameterGetBindings(self.handle)]
    
    def get_binding(self, node, name):
        return ParameterBinding(inParameterGetBinding(self.handle, node.handle, name))
    
    def get_or_add_binding(self, node, name):
        return ParameterBinding(inParameterGetOrAddBinding(self.handle, node.handle, name))
    
    def create_binding(self, node, name):
        return ParameterBinding(inParameterCreateBinding(self.handle, node.handle, name))
    
    def add_binding(self, binding):
        inParameterAddBinding(self.handle, binding)

    def remove_binding(self, binding):
        inParameterRemoveBinding(self.handle, binding)

    def reset(self):
        inParameterReset(self.handle)