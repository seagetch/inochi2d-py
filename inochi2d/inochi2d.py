import ctypes
import platform

if platform.uname()[0] == "Windows":
    inochi2d = ctypes.CDLL("libinochi2d-c.dll")
elif platform.uname()[0] == "Linux":
    inochi2d = ctypes.CDLL("libinochi2d-c.so")
else:
    pass

inochi2d.inInit.restype = None
inInit = inochi2d.inInit

inochi2d.inPuppetLoad.argtypes = [ctypes.c_char_p]
inochi2d.inPuppetLoad.restype = ctypes.c_void_p
def inPuppetLoad(name):
    name_bytes = name.encode('utf-8')
    puppet = inochi2d.inPuppetLoad(name_bytes)
    return puppet

inochi2d.inViewportSet.argtypes = (ctypes.c_int, ctypes.c_int)
inViewportSet = inochi2d.inViewportSet

inochi2d.inCameraSetZoom.argtypes = [ctypes.c_void_p, ctypes.c_float]
inochi2d.inCameraGetCurrent.restype = ctypes.c_void_p
inCameraGetCurrent = inochi2d.inCameraGetCurrent

inochi2d.inCameraSetPosition.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
inCameraSetPosition = inochi2d.inCameraSetPosition

inochi2d.inCameraSetZoom.argtypes = [ctypes.c_void_p, ctypes.c_float]
inCameraSetZoom = inochi2d.inCameraSetZoom

inochi2d.inPuppetUpdate.argtypes = (ctypes.c_void_p,)
inPuppetUpdate = inochi2d.inPuppetUpdate

inochi2d.inPuppetDraw.argtypes = (ctypes.c_void_p,)
inPuppetDraw = inochi2d.inPuppetDraw

inochi2d.inSceneDraw.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)
inSceneDraw = inochi2d.inSceneDraw

inSceneBegin = inochi2d.inSceneBegin
inSceneEnd = inochi2d.inSceneEnd
inCleanup = inochi2d.inCleanup