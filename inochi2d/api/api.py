from ctypes import *
import platform
import sys
import numpy as np
import copy

_CURRENT_MODULE_ = sys.modules[__name__]

if platform.uname()[0] == "Windows":
    inochi2d = CDLL("inochi2d-c.dll")
elif platform.uname()[0] == "Linux":
    inochi2d = CDLL("libinochi2d-c.so")
else:
    pass

def i2d_import(name : str, argtypes : tuple, restype, func = None):
    getattr(inochi2d, name).argtypes = argtypes
    getattr(inochi2d, name).restype  = restype
    if func is None:
        setattr(_CURRENT_MODULE_, name, getattr(inochi2d, name))

def i2d_decorate(argtypes : tuple, restype):
    def _decorator(func):
        name = func.__name__
        getattr(inochi2d, name).argtypes = argtypes
        getattr(inochi2d, name).restype  = restype
        return func
    return _decorator

###################################################################################################
# Basic Functions
i2d_import("inFreeMem", (c_void_p,), None)
i2d_import("inFreeArray", (POINTER(c_void_p), c_uint), None)
i2d_import("inInit", None, None)
i2d_import("inCleanup", None, None)
i2d_import("inUpdate", None, None)
i2d_import("inBlockProtected", None, None)

###################################################################################################
# Viewport
i2d_import("inViewportSet", (c_int, c_int), None)

@i2d_decorate((POINTER(c_int), POINTER(c_int)), None)
def inViewportGet():
    width = pointer(c_int(0))
    height = pointer(c_int(0))
    inochi2d.inViewportGet(width, height)
    return (width.contents.value, height.contents.value)

i2d_import("inSceneBegin", None, None)
i2d_import("inSceneEnd", None, None)
i2d_import("inSceneDraw", (c_float, c_float, c_float, c_float), None)

###################################################################################################
# Camera
i2d_import("inCameraGetCurrent", None, c_void_p)
i2d_import("inCameraDestroy", (c_void_p,), None)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float)), None)
def inCameraGetPosition(camera):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    inochi2d.inCameraGetPosition(camera, x, y)
    return (x.contents.value, y.contents.value)

i2d_import("inCameraSetPosition", (c_void_p, c_float, c_float), None)

@i2d_decorate((c_void_p, POINTER(c_float)), None)
def inCameraGetZoom(camera):
    zoom = pointer(c_float(0))
    inochi2d.inCameraGetZoom(camera, zoom)
    return zoom.contents.value

i2d_import("inCameraSetZoom", (c_void_p,c_float), None)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float)), None)
def inCameraGetCenterOffset(camera):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    inochi2d.inCameraGetCenterOffset(camera, x, y)
    return (x.contents.value, y.contents.value)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float)), None)
def inCameraGetRealSize(camera):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    inochi2d.inCameraGetRealSize(camera, x, y)
    return (x.contents.value, y.contents.value)

#void inCameraGetMatrix(InCamera* camera, float* mat4); // NOTE: mat4 array needs to be 16 elements long.

###################################################################################################
# Puppet
@i2d_decorate((c_char_p,), c_void_p)
def inPuppetLoad(name):
    name_bytes = name.encode('utf-8')
    puppet = inochi2d.inPuppetLoad(name_bytes)
    return puppet

#InPuppet* inPuppetLoadEx(const char *path, size_t length);
# Not required for python

#InPuppet* inPuppetLoadFromMemory(uint8_t* data, size_t length);

i2d_import("inPuppetDestroy", (c_void_p,), None)

@i2d_decorate((c_void_p, POINTER(c_char_p), POINTER(c_uint)), None)
def inPuppetGetName(puppet):
    length = pointer(c_uint(0))
    ptr    = pointer(c_char_p())
    inochi2d.inPuppetGetName(puppet, ptr, length)
    return ptr.contents
    # TBD: is this signature correct to return string value?

i2d_import("inPuppetUpdate", (c_void_p,), None)
i2d_import("inPuppetDraw", (c_void_p,), None)

###################################################################################################
# Parameter
@i2d_decorate((c_void_p, c_void_p, POINTER(c_uint)), None)
def inPuppetGetParameters(puppet):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    inochi2d.inPuppetGetParameters(puppet, ptr, length)
    buffer = pointer(cast((c_void_p * length.contents.value)(), POINTER(c_void_p)))
    inochi2d.inPuppetGetParameters(puppet, buffer, length)
    length = length.contents.value
    result = buffer.contents[0:length]

#    arr = ptr.contents
#    length = int.from_bytes(length.contents, sys.byteorder)
#    result = arr[0:length]
#    inFreeMem(arr)
    return result

@i2d_decorate((c_void_p,),c_char_p)
def inParameterGetName(param):
    ptr = inochi2d.inParameterGetName(param)
    result = ptr.decode("utf-8")
#    inFreeMem(ptr)
    return result

i2d_import("inParameterGetUUID", (c_void_p,), c_uint)

@i2d_decorate((c_void_p,POINTER(c_float), POINTER(c_float)), None)
def inParameterGetValue(param):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    ptr = inochi2d.inParameterGetValue(param, x, y)
    return (x.contents.value, y.contents.value)

i2d_import("inParameterSetValue", (c_void_p, c_float, c_float), None)
i2d_import("inParameterIsVec2", (c_void_p,), c_bool)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float)), None,)
def inParameterGetMin(param):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    inochi2d.inParameterGetMin(param, x, y)
    return (x.contents.value, y.contents.value)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float)), None,)
def inParameterGetMax(param):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    inochi2d.inParameterGetMax(param, x, y)
    return (x.contents.value, y.contents.value)

#void inParameterGetAxes(InParameter* param, float*** axes, size_t* xLength, size_t* yLength) {
@i2d_decorate((c_void_p, POINTER(POINTER(c_float)), POINTER(c_uint), POINTER(c_uint)), None)
def inParameterGetAxes(param):
    ptr = pointer(pointer(c_void_p(0)))
    xlength = pointer(c_uint(0));
    ylength = pointer(c_uint(0));
    inochi2d.inParameterGetAxes(param, ptr, xlength, ylength)
    arr = ptr.contents
    xlength = int.from_bytes(xlength.contents, sys.byteorder)
    ylength = int.from_bytes(ylength.contents, sys.byteorder)
    result = [[], []]

    result[0] = arr[0][0:xlength]
    result[1] = arr[1][0:ylength]

    ifFreeMem(arr)
    return result

@i2d_decorate((c_void_p, c_float, c_float, POINTER(c_uint), POINTER(c_uint)), None)
def inParameterFindClosestKeypoint(param, x, y):
    index_x = pointer(c_uint(0))
    index_y = pointer(c_uint(0))
    result = inochi2d.inParameterFindClosestKeypoint(param, x, y, index_x, index_y)
    return (index_x.contents.value, index_y.contents.value)

i2d_import("inParameterDestroy", (c_void_p,), None)

###################################################################################################
# Node
i2d_import("inPuppetGetRootNode", (c_void_p,), c_void_p)

@i2d_decorate((c_void_p, c_void_p, POINTER(c_uint)), None)
def inNodeGetChildren(node):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    inochi2d.inNodeGetChildren(node, ptr, length)
    buffer = pointer(cast((c_void_p * length.contents.value)(), POINTER(c_void_p)))
    inochi2d.inNodeGetChildren(node, buffer, length)
    length = length.contents.value
    result = buffer.contents[0:length]
    return result

@i2d_decorate((c_void_p, ), POINTER(c_char))
def inNodeGetName(node):
    name = inochi2d.inNodeGetName(node)
    result = c_char_p.from_buffer_copy(name).value.decode("utf-8")
    inFreeMem(name)
    return result

i2d_import("inNodeGetUUID", (c_void_p,), c_uint)
i2d_import("inNodeGetParent", (c_void_p,), c_void_p)
i2d_import("inNodeGetZSort", (c_void_p,), c_float)
i2d_import("inNodeGetLockToRoot", (c_void_p,), c_bool)
i2d_import("inNodeGetEnabled", (c_void_p,), c_bool)

@i2d_decorate((c_void_p,), c_char_p)
def inNodeGetPath(node):
    name = inochi2d.inNodeGetPath(node)
    result = name.contents.value
    return result

@i2d_decorate((c_void_p,), c_char_p)
def inNodeGetTypeId(node):
    name = inochi2d.inNodeGetTypeId(node)
    result = name.decode("utf-8")
    return result

i2d_import("inNodeHasParam", (c_void_p,), c_bool)
i2d_import("inNodeGetValue", (c_void_p, c_char_p), c_float)
i2d_import("inNodeSetValue", (c_void_p, c_char_p, c_float), None)
i2d_import("inNodeDraw", (c_void_p,), None)
i2d_import("inNodeDrawOne", (c_void_p,), None)
i2d_import("inNodeUpdate", (c_void_p,), None)
i2d_import("inNodeBeginUpdate", (c_void_p,), None)
i2d_import("inNodeTransformChanged", (c_void_p,), None)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)), None)
def inNodeGetCombinedBounds(node):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    z = pointer(c_float(0))
    w = pointer(c_float(0))
    inochi2d.inNodeGetCombinedBounds(node, x, y, z, w)
    return (x, y, z, w)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)), None)
def inNodeGetCombinedBoundsWithUpdate(node):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    z = pointer(c_float(0))
    w = pointer(c_float(0))
    inochi2d.inNodeGetCombinedBounds(node, x, y, z, w)
    return (x, y, z, w)

@i2d_decorate((c_void_p, c_char_p), None)
def inNodeLoadJson(node, text):
    inochi2d.inNodeLoadJson(node, text)

@i2d_decorate((c_void_p,), c_char_p)
def inNodeDumpJson(node):
    json_text = inochi2d.inNodeDumpJson(node)
    result    = json_text.decode("utf-8")
    return result

i2d_import("inNodeDestroy", (c_void_p,), None)

###################################################################################################
# Drawable
@i2d_decorate((c_void_p, POINTER(POINTER(c_float)), POINTER(c_uint)), c_bool)
def inDrawableGetVertices(node):
    vertices = pointer(pointer(c_float))
    length   = pointer(c_uint)
    result = inochi2d.inDrawableGetVertices(node, vertices, length)
    if not result:
        return None
    else:
        length = length.contents.value
        arr = vertices.contents[0:length]
        #inFreeMem(vertices)
        return arr

@i2d_decorate((c_void_p, POINTER(c_float), c_uint), c_bool)
def inDrawableSetVertices(node, vertices):
    arg_type = POINTER(c_float)
    length   = len(vertices)
    vert_arr = cast(vertices, arg_type)
    return inochi2d.inDrawableSetVertices(node, vert_arr, length)

i2d_import("inDrawableRefresh", (c_void_p,), c_bool)
i2d_import("inDrawableRefreshDeform", (c_void_p,), c_bool)
i2d_import("inDrawableReset", (c_void_p,), c_bool)

###################################################################################################
# Binding
#void inParameterGetBindings(InParameter* param, InParameterBinding*** arr, size_t* length) {
@i2d_decorate((c_void_p, c_void_p, POINTER(c_uint)), None)
def inParameterGetBindings(param):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    inochi2d.inParameterGetBindings(param, ptr, length)
    buffer = pointer(cast((c_void_p * length.contents.value)(), POINTER(c_void_p)))
    inochi2d.inParameterGetBindings(param, buffer, length)
    length = length.contents.value
    result = buffer.contents[0:length]
    return result

@i2d_decorate((c_void_p, c_void_p, c_char_p), c_void_p)
def inParameterGetBinding(param, node, name):
    return inochi2d.inParameterGetBinding(param, node, name.encode("utf-8"))
i2d_import("inParameterBindingApply", (c_void_p, c_uint, c_uint, c_float, c_float), None)
i2d_import("inParameterBindingClear", (c_void_p,), None)
i2d_import("inParameterBindingSetCurrent", (c_void_p, c_int, c_int), None)
i2d_import("inParameterBindingUnset", (c_void_p, c_uint, c_uint), None)
i2d_import("inParameterBindingReset", (c_void_p, c_uint, c_uint), None)
i2d_import("inParameterBindingIsSet", (c_void_p, c_uint, c_uint), c_bool)
i2d_import("inParameterBindingScaleValueAt", (c_void_p, c_uint, c_uint, c_uint, c_float), None)
i2d_import("inParameterBindingExtrapolateValueAt", (c_void_p, c_uint, c_uint, c_uint), None)
i2d_import("inParameterBindingCopyKeypointToBinding", (c_void_p, c_uint, c_uint, c_void_p, c_uint, c_uint), None)
i2d_import("inParameterBindingSwapKeypointWithBinding", (c_void_p, c_uint, c_uint, c_void_p, c_uint, c_uint), None)
i2d_import("inParameterBindingReverseAxis", (c_void_p, c_uint), None)
i2d_import("inParameterBindingReInterpolate", (c_void_p,), None)
i2d_import("inParameterBindingMoveKeypoints", (c_void_p, c_uint, c_uint, c_uint), None)
i2d_import("inParameterBindingInsertKeypoints", (c_void_p, c_uint, c_uint), None)
i2d_import("inParameterBindingDeleteKeypoints", (c_void_p, c_uint, c_uint), None)
@i2d_decorate((c_void_p,), POINTER(c_char))
def inParameterBindingGetName(binding):
    name = inochi2d.inParameterBindingGetName(binding)
    result = c_char_p.from_buffer_copy(name).value.decode("utf-8")
    inFreeMem(name)
    return result
i2d_import("inParameterBindingGetNode", (c_void_p,), c_void_p)
i2d_import("inParameterBindingGetNodeUUID", (c_void_p,), c_uint)
i2d_import("inParameterBindingIsCompatibleWithNode", (c_void_p, c_void_p), c_bool)
i2d_import("inParameterBindingGetInterpolateMode", (c_void_p,), c_uint)
i2d_import("inParameterBindingSetInterpolateMode", (c_void_p, c_uint), None)

i2d_import("inParameterBindingDestroy", (c_void_p,), None)

###################################################################################################
# Deformation
i2d_import("inParameterBindingGetType", (c_void_p, ), c_uint)
@i2d_decorate((c_void_p, c_uint, c_uint, POINTER(c_float)), c_uint)
def inParameterBindingGetFloat(binding, x, y):
    ptr =pointer(c_float(0));
    inochi2d.inParameterBindingGetFloat(binding, x, y, ptr)
    return ptr.contents.value

#BindingType inParameterBindingGetValue(InParameterBinding* binding, uint x, uint y, float** values, size_t* length) {
@i2d_decorate((c_void_p, c_uint, c_uint, c_void_p, POINTER(c_uint)), c_uint)
def inParameterBindingGetValue(binding, x, y):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    type = inochi2d.inParameterBindingGetValue(binding, x, y, ptr, length)

    type = inochi2d.inParameterBindingGetValue(binding, x, y, ptr, length)
    if type == 0:
        return inParameterBindingGetFloat(binding, x, y)
    elif type == 1:
        buffer = pointer(cast((c_float * length.contents.value)(), POINTER(c_float)))
        inochi2d.inParameterBindingGetValue(binding, x, y, buffer, length)
        length = length.contents.value
        return (buffer.contents, length)
    else:
        return None

#BindingType inParameterBindingGetValue(InParameterBinding* binding, uint x, uint y, float** values, size_t* length) {
def inParameterBindingGetValueUpdate(binding, x, y, buffer, length):
    buffer = pointer(buffer)
    length = pointer(c_uint(length))
    inochi2d.inParameterBindingGetValue(binding, x, y, buffer, length)

#BindingType inParameterBindingSetValue(InParameterBinding* binding, uint x, uint y, float* values, size_t length) {
@i2d_decorate((c_void_p, c_uint, c_uint, POINTER(c_float), c_uint), c_uint)
def inParameterBindingSetValue(binding, x, y, value):
    if isinstance(value, list):
        len = len(value)
        return inochi2d.inParameterBindingSetValue(binding, x, y, value, len)
    else:
        return inochi2d.inParameterBindingSetValue(binding, x, y, [value], 1)