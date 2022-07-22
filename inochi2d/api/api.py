import ctypes
import platform

if platform.uname()[0] == "Windows":
    inochi2d = ctypes.CDLL("inochi2d-c.dll")
elif platform.uname()[0] == "Linux":
    inochi2d = ctypes.CDLL("libinochi2d-c.so")
else:
    pass

#void inInit(double (*timingFunc)());
inochi2d.inInit.restype = None
inInit = inochi2d.inInit

#void inCleanup();
inochi2d.inCleanup.restype  = None
inCleanup = inochi2d.inCleanup

#void inUpdate();
inochi2d.inUpdate.restype  = None
inUpdate = inochi2d.inUpdate

#void inBlockProtected(void (*func)());
inochi2d.inBlockProtected.restype = None
inBlockProtected = inochi2d.inBlockProtected

#void inViewportSet(float width, float height);
inochi2d.inViewportSet.argtypes = (ctypes.c_int, ctypes.c_int)
inochi2d.inViewportSet.restype  = None
inViewportSet = inochi2d.inViewportSet

#void inViewportGet(float* width, float* height);
inochi2d.inViewportGet.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
inochi2d.inViewportGet.restype  = None
def inViewportGet():
    width = ctypes.pointer(ctypes.c_int(0))
    height = ctypes.pointer(ctypes.c_int(0))
    inochi2d.inViewportGet(width, height)
    return (width.contents.value, height.contents.value)


#void inSceneBegin();
inochi2d.inSceneBegin.restype = None
inSceneBegin = inochi2d.inSceneBegin

#void inSceneEnd();
inochi2d.inSceneEnd.restype = None
inSceneEnd = inochi2d.inSceneEnd

#void inSceneDraw(float x, float y, float width, float height);
inochi2d.inSceneDraw.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)
inochi2d.inSceneDraw.restype  = None
inSceneDraw = inochi2d.inSceneDraw


#InCamera* inCameraGetCurrent();
inochi2d.inCameraGetCurrent.restype = ctypes.c_void_p
inCameraGetCurrent = inochi2d.inCameraGetCurrent

#void inCameraDestroy(InCamera* camera);
inochi2d.inCameraDestroy.argtypes = (ctypes.c_void_p,)
inochi2d.inCameraDestroy.restype  = None
inCameraDestroy = inochi2d.inCameraDestroy

#void inCameraGetPosition(InCamera* camera, int* x, int* y);
inochi2d.inCameraGetPosition.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
inochi2d.inCameraGetPosition.restype  = None
def inCameraGetPosition(camera):
    x = ctypes.pointer(ctypes.c_float(0))
    y = ctypes.pointer(ctypes.c_float(0))
    inochi2d.inCameraGetPosition(camera, x, y)
    return (x.contents.value, y.contents.value)

#void inCameraSetPosition(InCamera* camera, float x, float y);
inochi2d.inCameraSetPosition.argtypes = (ctypes.c_void_p, ctypes.c_float, ctypes.c_float)
inochi2d.inCameraSetPosition.restype  = None
inCameraSetPosition = inochi2d.inCameraSetPosition

#void inCameraGetZoom(InCamera* camera, float* zoom);
inochi2d.inCameraGetZoom.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_float))
inochi2d.inCameraGetZoom.restype  = None
def inCameraGetZoom(camera):
    zoom = ctypes.pointer(ctypes.c_float(0))
    inochi2d.inCameraGetZoom(camera, zoom)
    return zoom.contents.value

#void inCameraSetZoom(InCamera* camera, float zoom);
inochi2d.inCameraSetZoom.argtypes = (ctypes.c_void_p, ctypes.c_float)
inochi2d.inCameraSetZoom.restype  = None
inCameraSetZoom = inochi2d.inCameraSetZoom

#void inCameraGetCenterOffset(InCamera* camera, float* x, float* y);
inochi2d.inCameraGetCenterOffset.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
inochi2d.inCameraGetCenterOffset.restype  = None
def inCameraGetCenterOffset(camera):
    x = ctypes.pointer(ctypes.c_float(0))
    y = ctypes.pointer(ctypes.c_float(0))
    inochi2d.inCameraGetCenterOffset(camera, x, y)
    return (x.contents.value, y.contents.value)

#void inCameraGetRealSize(InCamera* camera, float* x, float* y);
inochi2d.inCameraGetRealSize.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float))
inochi2d.inCameraGetRealSize.restype  = None
def inCameraGetRealSize(camera):
    x = ctypes.pointer(ctypes.c_float(0))
    y = ctypes.pointer(ctypes.c_float(0))
    inochi2d.inCameraGetRealSize(camera, x, y)
    return (x.contents.value, y.contents.value)

#void inCameraGetMatrix(InCamera* camera, float* mat4); // NOTE: mat4 array needs to be 16 elements long.


#InPuppet* inPuppetLoad(const char *path);
inochi2d.inPuppetLoad.argtypes = [ctypes.c_char_p]
inochi2d.inPuppetLoad.restype = ctypes.c_void_p
def inPuppetLoad(name):
    name_bytes = name.encode('utf-8')
    puppet = inochi2d.inPuppetLoad(name_bytes)
    return puppet

#InPuppet* inPuppetLoadEx(const char *path, size_t length);
# Not required for python

#InPuppet* inPuppetLoadFromMemory(uint8_t* data, size_t length);

#void inPuppetDestroy(InPuppet* puppet);
inochi2d.inPuppetDestroy.argtypes = (ctypes.c_void_p,)
inochi2d.inPuppetDestroy.restype  = None
inPuppetDestroy = inochi2d.inPuppetDestroy

#void inPuppetGetName(InPuppet* puppet, const char *text, size_t *len);
inochi2d.inPuppetGetName.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint))
inochi2d.inPuppetGetName.restype  = None
def inPuppetGetName(puppet):
    length = ctypes.pointer(ctypes.c_unit(0))
    ptr    = ctypes.c_char_p("")
    inochi2d.inPuppetGetName(puppet, ptr, length)
    # TBD: is this signature correct to return string value?

#void inPuppetUpdate(InPuppet* puppet);
inochi2d.inPuppetUpdate.argtypes = (ctypes.c_void_p,)
inochi2d.inPuppetUpdate.restype  = None
inPuppetUpdate = inochi2d.inPuppetUpdate

#void inPuppetDraw(InPuppet* puppet);
inochi2d.inPuppetDraw.argtypes = (ctypes.c_void_p,)
inochi2d.inPuppetDraw.restype  = None
inPuppetDraw = inochi2d.inPuppetDraw