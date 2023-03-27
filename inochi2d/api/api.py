from ctypes import *
import platform
import sys
import numpy as np
import copy
import functools

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

def shape_len(arr):
    return functools.reduce(lambda x, y: x * y, arr.shape, 1)

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
@i2d_decorate((c_void_p, POINTER(c_float)), None)
def inCameraGetMatrix(camera):
    mem = (c_float * 16)()
    buffer = cast(mem, POINTER(c_float))
    inochi2d.inCameraGetMatrix(camera, buffer)
    return np.frombuffer(mem, c_float).reshape((4, 4))

@i2d_decorate((c_void_p, POINTER(c_float)), None)
def inCameraGetScreenToGlobalMatrix(camera):
    mem = (c_float * 16)()
    buffer = cast(mem, POINTER(c_float))
    inochi2d.inCameraGetScreenToGlobalMatrix(camera, buffer)
    return np.frombuffer(mem, c_float).reshape((4, 4))

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
i2d_import("inPuppetGetEnableDrivers", (c_void_p,), c_bool)
i2d_import("inPuppetSetEnableDrivers", (c_void_p, c_bool), None)

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
    inochi2d.inParameterFindClosestKeypoint(param, x, y, index_x, index_y)
    return (index_x.contents.value, index_y.contents.value)

@i2d_decorate((c_void_p, POINTER(c_uint), POINTER(c_uint)), None)
def inParameterFindClosestKeypointAtCurrent(param):
    index_x = pointer(c_uint(0))
    index_y = pointer(c_uint(0))
    inochi2d.inParameterFindClosestKeypointAtCurrent(param, index_x, index_y)
    return (index_x.contents.value, index_y.contents.value)

i2d_import("inParameterDestroy", (c_void_p,), None)

@i2d_decorate((c_void_p, c_void_p, c_char_p), c_void_p)
def inParameterGetBinding(param, node, name):
    return inochi2d.inParameterGetBinding(param, node, name.encode("utf-8"))

@i2d_decorate((c_void_p, c_void_p, c_char_p), c_void_p)
def inParameterGetOrAddBinding(param, node, name):
    return inochi2d.inParameterGetOrAddBinding(param, node, name.encode("utf-8"))

@i2d_decorate((c_void_p, c_void_p, c_char_p), c_void_p)
def inParameterCreateBinding(param, node, name):
    return inochi2d.inParameterCreateBinding(param, node, name.encode("utf-8"))

@i2d_decorate((c_void_p, c_void_p), c_void_p)
def inParameterAddBinding(param, binding):
    return inochi2d.inParameterAddBinding(param, binding)

@i2d_decorate((c_void_p, c_void_p), c_void_p)
def inParameterRemoveBinding(param, binding):
    return inochi2d.inParameterRemoveBinding(param, binding)

i2d_import("inParameterReset", (c_void_p,), None)

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

@i2d_decorate((c_void_p, c_char_p), c_float)
def inNodeGetValue(node, name):
    return inochi2d.inNodeGetValue(node, name.encode("utf-8"))

@i2d_decorate((c_void_p, c_char_p, c_float), None)
def inNodeSetValue(node, name, value):
    inochi2d.inNodeSetValue(node, name.encode("utf-8"), value)

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
    return (x.contents.value, y.contents.value, z.contents.value, w.contents.value)

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)), None)
def inNodeGetCombinedBoundsWithUpdate(node):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    z = pointer(c_float(0))
    w = pointer(c_float(0))
    inochi2d.inNodeGetCombinedBounds(node, x, y, z, w)
    return (x.contents.value, y.contents.value, z.contents.value, w.contents.value)

@i2d_decorate((c_void_p, c_char_p), None)
def inNodeLoadJson(node, data):
    inochi2d.inNodeLoadJson(node, text)

@i2d_decorate((c_void_p, c_bool), POINTER(c_char))
def inNodeDumpJson(node, recursive):
    json_text = inochi2d.inNodeDumpJson(node, recursive)
    result = c_char_p.from_buffer_copy(json_text).value.decode("utf-8")
    inFreeMem(json_text)
    return result

i2d_import("inNodeDestroy", (c_void_p,), None)

@i2d_decorate((c_void_p, POINTER(c_float)), None)
def inNodeGetTransformMatrix(camera):
    mem = (c_float * 16)()
    buffer = cast(mem, POINTER(c_float))
    inochi2d.inNodeGetTransformMatrix(camera, buffer)
    return np.frombuffer(mem, c_float).reshape((4, 4))

@i2d_decorate((c_void_p, POINTER(c_float)), None)
def inNodeGetLocalTransformMatrix(camera):
    mem = (c_float * 16)()
    buffer = cast(mem, POINTER(c_float))
    inochi2d.inNodeGetLocalTransformMatrix(camera, buffer)
    return np.frombuffer(mem, c_float).reshape((4, 4))

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float)), None)
def inNodeGetTranslation(node):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    z = pointer(c_float(0))
    inochi2d.inNodeGetTranslation(node, x, y, z)
    return np.array((x.contents.value, y.contents.value, z.contents.value))

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float)), None)
def inNodeGetRotation(node):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    z = pointer(c_float(0))
    inochi2d.inNodeGetRotation(node, x, y, z)
    return np.array((x.contents.value, y.contents.value, z.contents.value))

@i2d_decorate((c_void_p, POINTER(c_float), POINTER(c_float)), None)
def inNodeGetScale(node):
    x = pointer(c_float(0))
    y = pointer(c_float(0))
    inochi2d.inNodeGetScale(node, x, y)
    return np.array((x.contents.value, y.contents.value))

i2d_import("inNodeSetTranslation", (c_void_p, c_float, c_float, c_float), None)
i2d_import("inNodeSetRotation", (c_void_p, c_float, c_float, c_float), None)
i2d_import("inNodeSetScale", (c_void_p, c_float, c_float), None)

###################################################################################################
# Drawable
i2d_import("inSetUpdateBounds", (c_bool,), None)

@i2d_decorate((c_void_p, c_void_p, POINTER(c_uint)), c_bool)
def inDrawableGetVertices(node):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    result = inochi2d.inDrawableGetVertices(node, ptr, length)
    if not result:
        return None
    mem = (c_float * length.contents.value)()
    buffer = pointer(cast(mem, POINTER(c_float)))
    inochi2d.inDrawableGetVertices(node, buffer, length)
    length = length.contents.value
    data = np.frombuffer(mem, c_float).reshape((int(length / 2), 2))
    return data

@i2d_decorate((c_void_p, POINTER(c_float), c_uint), c_bool)
def inDrawableSetVertices(node, vertices):
    buffer = vertices.ctypes.data_as(POINTER(c_float))
    length = shape_len(vertices)
    inochi2d.inDrawableSetVertices(node, buffer, length)

@i2d_decorate((c_void_p, c_void_p, POINTER(c_uint)), c_bool)
def inDrawableGetDeformation(node):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    result = inochi2d.inDrawableGetDeformation(node, ptr, length)
    if not result:
        return None
    mem = (c_float * length.contents.value)()
    buffer = pointer(cast(mem, POINTER(c_float)))
    inochi2d.inDrawableGetDeformation(node, buffer, length)
    length = length.contents.value
    data = np.frombuffer(mem, c_float, length).reshape((int(length / 2), 2))
    return data

i2d_import("inDrawableRefresh", (c_void_p,), c_bool)
i2d_import("inDrawableRefreshDeform", (c_void_p,), c_bool)
i2d_import("inDrawableReset", (c_void_p,), c_bool)
i2d_import("inDrawableDrawBounds", (c_void_p,), c_bool)
i2d_import("inDrawableDrawMeshLines", (c_void_p,), c_bool)
i2d_import("inDrawableDrawMeshPoints", (c_void_p,), c_bool)

@i2d_decorate((c_void_p, POINTER(c_float)), c_bool)
def inDrawableGetDynamicMatrix(node):
    mem = (c_float * 16)()
    buffer = cast(mem, POINTER(c_float))
    inochi2d.inDrawableGetDynamicMatrix(node, buffer)
    return np.frombuffer(mem, c_float).reshape((4, 4))

###################################################################################################
# MeshData

@i2d_decorate((c_void_p, c_void_p, POINTER(c_uint),
               c_void_p, POINTER(c_uint), c_void_p, POINTER(c_uint),
               c_void_p, POINTER(c_uint), POINTER(c_uint),
               POINTER(c_float), POINTER(c_float)), c_bool)
def inDrawableGetMeshData(node):
    ptr_verts  = c_void_p(0)
    len_verts  = pointer(c_uint(0))
    ptr_uvs    = c_void_p(0)
    len_uvs    = pointer(c_uint(0))
    ptr_ind    = c_void_p(0)
    len_ind    = pointer(c_uint(0))
    ptr_axes   = c_void_p(0)
    len_axes_x = pointer(c_uint(0))
    len_axes_y = pointer(c_uint(0))
    origin_x   = pointer(c_float(0))
    origin_y   = pointer(c_float(0))
    succeeded  = inochi2d.inDrawableGetMeshData(node, ptr_verts, len_verts, ptr_uvs, len_uvs, ptr_ind, len_ind, ptr_axes, len_axes_x, len_axes_y, origin_x, origin_y)
    if not succeeded:
        return [None, None, None, None, (None, None)]
    mem_verts  = (c_float  * len_verts.contents.value)()
    buf_verts  = pointer(cast(mem_verts, POINTER(c_float)))
    mem_uvs    = (c_float  * len_uvs.contents.value)()
    buf_uvs    = pointer(cast(mem_uvs, POINTER(c_float)))
    mem_ind    = (c_ushort * len_ind.contents.value)()
    buf_ind    = pointer(cast(mem_ind, POINTER(c_ushort)))
    mem_axes   = (c_void_p * 2)()
    buf_axes   = pointer(cast(mem_axes, POINTER(c_void_p)))
    mem_axis_y = (c_float  * len_axes_y.contents.value)()    
    mem_axis_x = (c_float  * len_axes_x.contents.value)()    
    buf_axes.contents[0]= cast(mem_axis_y, c_void_p)
    buf_axes.contents[1]= cast(mem_axis_x, c_void_p)
    inochi2d.inDrawableGetMeshData(node, buf_verts, len_verts, buf_uvs, len_uvs, buf_ind, len_ind, buf_axes, len_axes_x, len_axes_y, origin_x, origin_y)
    ret_verts  = np.ctypeslib.as_array(mem_verts).reshape((len_verts.contents.value // 2, 2))
    ret_uvs    = np.ctypeslib.as_array(mem_uvs).reshape((len_uvs.contents.value // 2, 2))
    ret_ind    = np.ctypeslib.as_array(mem_ind).reshape((int(len_ind.contents.value // 3), 3))
    ret_axes   = [np.ctypeslib.as_array(mem_axis_y), 
                  np.ctypeslib.as_array(mem_axis_x)]
    return [ret_verts, ret_uvs, ret_ind, ret_axes, (origin_x, origin_y)]

@i2d_decorate((c_void_p, c_void_p, c_uint,
               c_void_p, c_uint, c_void_p, c_uint,
               c_void_p, c_uint, c_uint,
               POINTER(c_float), POINTER(c_float)), c_bool)
def inDrawableSetMeshData(node, verts, uvs, ind, axes, origin):
    if verts is not None:
        buf_verts  = verts.ctypes.data_as(POINTER(c_float))
        len_verts  = shape_len(verts)
    else:
        buf_verts  = c_void_p(0)
        len_verts  = 0
    if uvs:
        buf_uvs    = uvs.ctypes.data_as(POINTER(c_float))
        len_uvs    = shape_len(uvs)
    else:
        buf_uvs    = c_void_p(0)
        len_uvs    = 0
    if ind:
        buf_ind    = ind.ctypes.data_as(POINTER(c_ushort))
        len_ind    = shape_len(ind)
    else:
        buf_ind    = c_void_p(0)
        len_ind    = 0
    if axes:
        buf_axes   = pointer(cast((c_void_p * 2)(), POINTER(c_void_p)))
        buf_axes.contents[0]= axes[0].ctypes.data_as(POINTER(c_float))
        buf_axes.contents[1]= axes[1].ctypes.data_as(POINTER(c_float))
        len_axes_x = shape_len(buf_axes[1])
        len_axes_y = shape_len(buf_axes[0])
    if origin:
        origin_x   = pointer(c_float(origin[0]))
        origin_y   = pointer(c_float(origin[1]))
    else:
        origin_x   = pointer(c_float(0))
        origin_y   = pointer(c_float(0))
    inochi2d.inDrawableSetMeshData(node, buf_verts, len_verts, buf_uvs, len_uvs, buf_ind, len_ind, buf_axes, len_axes_x, len_axes_y, origin_x, origin_y)

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

i2d_import("inParameterBindingSetFloat", (c_void_p, c_uint, c_uint, c_float), None)

@i2d_decorate((c_void_p, c_uint, c_uint, c_void_p, POINTER(c_uint)), c_uint)
def inParameterBindingGetValue(binding, x, y):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    type = inochi2d.inParameterBindingGetValue(binding, x, y, ptr, length)
    if type == 0:
        return inParameterBindingGetFloat(binding, x, y)
    elif type == 1:
        mem = (c_float * length.contents.value)()
        buffer = pointer(cast(mem, POINTER(c_float)))
        inochi2d.inParameterBindingGetValue(binding, x, y, buffer, length)
        length = length.contents.value
        data = np.frombuffer(mem, c_float).reshape((int(length / 2), 2))
        return data
    else:
        return None

def inParameterBindingGetValueUpdate(binding, x, y, data):
    length = shape_len(data)
    buffer = pointer(np.ctypes.data_as(data, POINTER(c_float)))
    length = pointer(c_uint(length))
    inochi2d.inParameterBindingGetValue(binding, x, y, buffer, length)

@i2d_decorate((c_void_p, c_uint, c_uint, POINTER(c_float), c_uint), c_uint)
def inParameterBindingSetValue(binding, x, y, value):
    if isinstance(value, np.ndarray):
        buffer = value.ctypes.data_as(POINTER(c_float))
        len = shape_len(value)
        return inochi2d.inParameterBindingSetValue(binding, x, y, buffer, len)
    else:
        return inochi2d.inParameterBindingSetFloat(binding, x, y, value)

i2d_import("inParameterBindingClearValue", (c_void_p, c_uint, c_uint), None)

###################################################################################################
# Texture
i2d_import("inPuppetGetTexture", (c_void_p, c_uint), c_void_p)
i2d_import("inTextureGetWidth", (c_void_p,), c_uint)
i2d_import("inTextureGetHeight", (c_void_p,), c_uint)
i2d_import("inTextureGetColorMode", (c_void_p,), c_uint)
i2d_import("inTextureGetChannels", (c_void_p,), c_int)

@i2d_decorate((c_void_p, POINTER(c_int), POINTER(c_int)), None)
def inTextureGetCenter(texture):
    x = pointer(c_int(0))
    y = pointer(c_int(0))
    inochi2d.inTextureGetCenter(texture, x, y)
    return (x.contents.value, y.contents.value)

@i2d_decorate((c_void_p, POINTER(c_int), POINTER(c_int)), None)
def inTextureGetSize(texture):
    x = pointer(c_int(0))
    y = pointer(c_int(0))
    inochi2d.inTextureGetSize(texture, x, y)
    return (x.contents.value, y.contents.value)

i2d_import("inTextureBind", (c_void_p, c_uint), None)
i2d_import("inTextureGetTextureId", (c_void_p,), c_uint)
i2d_import("inTextureDispose", (c_void_p,), None)

@i2d_decorate((c_void_p, POINTER(c_ubyte), c_uint), None)
def inTextureSetData(texture, data):
    buffer = data.ctypes.data_as(POINTER(c_ubyte))
    length = shape_len(data)
    inochi2d.inTextureSetData(texture, buffer, length)

@i2d_decorate((c_void_p, c_bool, c_void_p, POINTER(c_uint)), None)
def inTextureGetTextureData(texture, unmultiply):
    ptr = c_void_p(0)
    length = pointer(c_uint(0));
    inochi2d.inTextureGetTextureData(texture, unmultiply, ptr, length)
    mem = (c_ubyte * length.contents.value)()
    buffer = pointer(cast(mem, POINTER(c_ubyte)))
    inochi2d.inTextureGetTextureData(texture, unmultiply, buffer, length)
    length = length.contents.value
    data = np.frombuffer(mem, c_ubyte)
    return data

i2d_import("inTextureDestroy", (c_void_p, ), None)

###################################################################################################
# Dbg
i2d_import("inGetDbgDrawMeshOutlines", None, c_bool)
i2d_import("inSetDbgDrawMeshOutlines", (c_bool,), None)
i2d_import("inGetDbgDrawMeshVertexPoints", None, c_bool)
i2d_import("inSetDbgDrawMeshVertexPoints", (c_bool,), None)
i2d_import("inGetDbgDrawMeshOrientation", None, c_bool)
i2d_import("inSetDbgDrawMeshOrientation", (c_bool,), None)
i2d_import("inDbgPointsSize", (c_float,), None)
i2d_import("inDbgLineWidth", (c_float,), None)
@i2d_decorate((POINTER(c_float), c_uint), None)
def inDbgSetBuffer(_points):
    points = _points.ctypes.data_as(POINTER(c_float))    
    length = shape_len(_points)
    inochi2d.inDbgSetBuffer(points, length)

#void inDbgSetBuffer(float* _points, size_t point_length, ushort* _indices, size_t ind_len) {
@i2d_decorate((POINTER(c_float), c_uint, POINTER(c_float), c_uint), None)
def inDbgSetBufferWithIndices(_points, _indices):
    points  = _points.ctypes.data_as(POINTER(c_float))
    indices = _indices.ctypes.data_as(POINTER(c_ushort))

    ptlen  = shape_len(_points)
    indlen = shape_len(_indices)
    inochi2d.inDbgSetBufferWithIndices(points, ptlen, indices, indlen)

#void inDbgDrawPoints(float[4] _color, float* _mat4) {
@i2d_decorate((POINTER(c_float), c_void_p), None)
def inDbgDrawPoints(_color, _matrix):
    color = _color.ctypes.data_as(POINTER(c_float))
    if _matrix is None:
        inochi2d.inDbgDrawPoints(color, c_void_p(0))
    else:
        matrix = _matrix.ctypes.data_as(POINTER(c_float))
        inochi2d.inDbgDrawPoints(color, matrix)

#void inDbgDrawLines(float[4] _color, float* _mat4) {
@i2d_decorate((POINTER(c_float), c_void_p), None)
def inDbgDrawLines(_color, _matrix):
    color = _color.ctypes.data_as(POINTER(c_float))
    if _matrix is None:
        inochi2d.inDbgDrawLines(color, c_void_p(0))
    else:
        matrix = _matrix.ctypes.data_as(POINTER(c_float))
        inochi2d.inDbgDrawLines(color, matrix)
