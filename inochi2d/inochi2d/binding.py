from ..api import *
from .node import *

from typing import *

class Deformation:
    def __init__(self, offsets, binding, x, y):
        self.binding = binding
        self.x = x
        self.y = y
        self.vertex_offsets = offsets

    def pull(self, x = None, y = None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        inParameterBindingGetValueUpdate(self.binding, x, y, self.vertex_offsets)

class ParameterBinding:

    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        inParameterBindingDestroy(self.handle)
        self.handle = None

    @property
    def name(self):
        return inParameterBindingGetName(self.handle)
    
    @property
    def node(self):
        return Node(inParameterBindingGetNode(self.handle))
    
    def apply(self, x, y, ofsx, ofsy):
        inParameterBindingApply(self.handle, x, y, ofsx, ofsy)

    def clear(self):
        inParameterBindingClear(self.handle)

    def set_current(self, x, y):
        inParameterBindingSetCurrent(self.handle, x, y)
    
    def unset(self, x, y):
        inParameterBindingUnset(self.handle, x, y)
    
    def reset(self, x, y):
        inParameterBindingReset(self.handle, x, y)

    def is_set(self, x, y):
        return inParameterBindingIsSet(self.handle, x, y)
    
    def scale_value_at(self, x, y, axis, scale):
        inParameterBindingScaleValueAt(self.handle, x, y, axis, scale)

    def copy_keypoint_to_binding(self, src_x: int, src_y: int, other, dest_x: int, dest_y: int):
        inParameterBindingCopyKeypointToBinding(self.handle, src_x, src_y, other.handle, dest_x, dest_y)

    def swap_keypoint_with_binding(self, src_x, src_y, other, dest_x, dest_y):
        inParameterBindingSwapKeypointWithBinding(self.handle, src_x, src_y, other.handle, dest_x, dest_y)

    def reverse_axis(self, axis):
        inParameterBindingReverseAxis(self.handle, axis)

    def reinterpolate(self):
        inParameterBindingReInterpolate(self.handle)

    def move_keypoints(self, axis, old, new):
        inParameterBindingMoveKeypoints(self.handle, axis, old, new)

    def insert_keypoints(self, axis, index):
        inParameterBindingInsertKeypoints(self.handle, axis, index)

    def delete_keypoints(self, axis, index):
        inParameterBindingDeleteKeypoints(self.handle, axis, index)

    @property
    def node_uuid(self):
        return inParameterBindingGetNodeUUID(self.handle)

    def is_compatible(self, node):
        return inParameterBindingIsCompatibleWithNode(self.handle, node.handle)

    @property
    def interpolate_mode(self):
        return inParameterBindingGetInterpolateMode(self.handle)
    
    @interpolate_mode.setter
    def set_interpolate_mode(self, mode):
        inParameterBindingSetInterpolateMode(self.handle, mode)
    
    class Value:
        def __init__(self, binding):
            self.handle = binding.handle

        def __getitem__(self, key):
            x, y = key
            result = inParameterBindingGetValue(self.handle, x, y)
            if isinstance(result, float):
                return result
            else:
                return result
#                return Deformation(result, self.handle, x, y)

        def __setitem__(self, key, value):
            x, y = key
            if isinstance(value, Deformation):
                return inParameterBindingSetValue(self.handle, x, y, value.vertex_offsets)
            else:
                return inParameterBindingSetValue(self.handle, x, y, value)
        
    @property
    def value(self):
        return self.Value(self)