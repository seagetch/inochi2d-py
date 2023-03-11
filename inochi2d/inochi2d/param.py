from ..api import *

class Parameter:
    def __init__(self, handle):
        self.handle = handle
        self.is_vec2 = inParameterIsVec2(self.handle)
        
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