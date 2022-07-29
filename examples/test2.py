import pyglfw.pyglfw as glfw
from pyglfw.libapi import *
import ctypes
from inochi2d import *
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

if not glfw.init():
    raise RuntimeError('Could not initialize GLFW3')

glfw.Window.hint(context_version_major = 3)
glfw.Window.hint(context_version_minor = 3)
glfw.Window.hint(forward_compat = True)
#glfw.Window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.Window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Aka', None, None)
if not window:
    glfw.terminate()
    raise RuntimeError('Could not create an window')

print("make_context_current")
window.make_current()
window.swap_interval(1)

@ctypes.CFUNCTYPE(ctypes.c_double)
def curr_time():
    return glfwGetTime() * 0.001

inInit(curr_time)

from OpenGL.GL import *

puppet = inPuppetLoad("./Aka-working.inx")

inochi2d.inViewportSet(WINDOW_WIDTH, WINDOW_HEIGHT)
camera = inochi2d.inCameraGetCurrent()
inochi2d.inCameraSetZoom(camera, 0.3)
inochi2d.inCameraSetPosition(camera, 0., 0.)

while not window.should_close:
#    glClearColor(0, 0, 0.5, 1.0)
#    glClear(GL_COLOR_BUFFER_BIT)
    
    inSceneBegin()
    inPuppetUpdate(puppet)
    inPuppetDraw(puppet)
    inSceneDraw(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    inSceneEnd()
    
    window.swap_buffers()
    glfw.poll_events()

glfw.terminate()