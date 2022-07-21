from sdl2 import *
from OpenGL import GL, GLU
from inochi2d import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

if SDL_Init(SDL_INIT_VIDEO) != 0:
    print(SDL_GetError())
    exit(-1)

# Set up OpenGL context
SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 2);

# Set up buffers + alpha channel
SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8);
SDL_GL_SetAttribute(SDL_GL_ALPHA_SIZE, 8);

## Linux>
# Don't disable compositing on Linux
SDL_SetHint(SDL_HINT_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR, b"0")

# We *always* want to use EGL, especially if we want to pass textures around via DMABUF.
#SDL_SetHint(SDL_HINT_VIDEO_X11_FORCE_EGL, b"1")
SDL_SetHint(SDL_HINT_VIDEO_EGL_ALLOW_TRANSPARENCY, b"1")
## <Linux

window = SDL_CreateWindow(
    b"Aka",
    SDL_WINDOWPOS_UNDEFINED,
    SDL_WINDOWPOS_UNDEFINED, WINDOW_WIDTH, WINDOW_HEIGHT,
    SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)

if not window:
    print(SDL_GetError())
    exit(-1)

ctx = SDL_GL_CreateContext(window)

SDL_GL_MakeCurrent(window, ctx);
SDL_GL_SetSwapInterval(1); # Enable VSync

print("Here")

inInit(SDL_GetTicks)
print("Here")
puppet = inPuppetLoad("./Aka-working.inx")

print("Here")
inViewportSet(WINDOW_WIDTH, WINDOW_HEIGHT)
camera = inCameraGetCurrent()
inCameraSetZoom(camera, 0.3)
inCameraSetPosition(camera, 0., 0.)

inSceneBegin()

print("Here")
ev = SDL_Event()
isrunning = True
while isrunning:
    while SDL_PollEvent(ctypes.byref(ev)) != 0:
        if ev.type == SDL_QUIT:
            isrunning = not isrunning

#        GL.glClearColor(0, 0, 0, 1)
#        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    inPuppetUpdate(puppet)
    inPuppetDraw(puppet)
    inSceneDraw(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    SDL_GL_SwapWindow(window)
    SDL_Delay(10)

inSceneEnd()
inCleanup()

SDL_GL_DeleteContext(ctx)
SDL_DestroyWindow(window)
SDL_Quit()