# TODO: put code inside a class


from utilities.exception_dialog import ExceptionDialog

try:
    import glfw
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import GLFW\n"
                             "Run:\npip3 install glfw")

try:
    from OpenGL.GL import *
    from OpenGL.GL.shaders import compileProgram, compileShader
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import PyOpenGL\n"
                             "Run:\npip3 install PyOpenGL")

try:
    import numpy as np
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import NumPy\n"
                             "Run:\npip3 install numpy")


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
             0.5,  0.5, 0.0, 1.0, 1.0, 1.0,
             0.0, 0.75, 0.0, 1.0, 1.0, 0.0]

indices = [0, 1, 2,
           1, 2, 3,
           2, 3, 4]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

with open("shaders/index_drawing.vs", "r") as source:
    vertex_src = source.read()

with open("shaders/index_drawing.fs", "r") as source:
    fragment_src = source.read()

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Element Buffer Object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()