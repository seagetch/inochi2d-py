from ctypes import *
import platform
import sys
import numpy as np

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
@i2d_decorate((c_void_p, POINTER(POINTER(c_void_p)), POINTER(c_uint)), None)
def inPuppetGetParameters(puppet):
    ptr = pointer(pointer(c_void_p(0)))
    length = pointer(c_uint(0));
    inochi2d.inPuppetGetParameters(puppet, ptr, length)
    arr = ptr.contents
    length = int.from_bytes(length.contents, sys.byteorder)
    result = []
    for i in range(length):
        result.append(arr[i])
    inFreeMem(arr)
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
@i2d_decorate((c_void_p, POINTER(POINTER(c_void_p)), POINTER(c_uint), POINTER(c_uint)), None)
def inParameterGetAxes(param):
    ptr = pointer(pointer(c_void_p(0)))
    xlength = pointer(c_uint(0));
    ylength = pointer(c_uint(0));
    inochi2d.inParameterGetAxes(param, ptr, xlength, ylength)
    arr = ptr.contents
    xlength = int.from_bytes(xlength.contents, sys.byteorder)
    ylength = int.from_bytes(ylength.contents, sys.byteorder)
    result = [[], []]

    result_type = c_float * xlength
    result[0] = cast(arr[0].contents, result_type).contents
    
    result_type = c_float * ylength
    result[1] = cast(arr[1].contents, result_type).contents

#    inFreeArray(arr)
    ifFreeMem(arr)
    return result

###################################################################################################
# Node
i2d_import("inPuppetGetRootNode", (c_void_p,), c_void_p)

@i2d_decorate((c_void_p, POINTER(POINTER(c_void_p)), POINTER(c_uint)), None)
def inNodeGetChildren(node):
    ptr = pointer(pointer(c_void_p(0)))
    length = pointer(c_uint(0));
    inochi2d.inNodeGetChildren(node, ptr, length)
    arr = ptr.contents
    length = int.from_bytes(length.contents, sys.byteorder)
    result = []
    for i in range(length):
        result.append(arr[i])
    inFreeMem(arr)
    return result

@i2d_decorate((c_void_p, ), c_char_p)
def inNodeGetName(node):
    name = inochi2d.inNodeGetName(node)
    result = name.decode("utf-8")
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
        result_type = c_float * length
        arr = cast(vertices.contents, result_type).value
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