from utilities.exception_dialog import ExceptionDialog
import sys

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

try:
    from PySide2 import QtOpenGL, QtWidgets, QtCore, QtGui
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import PySide2\n"
                             "Run:\npip3 install PySide2")

try:
    from OpenGL.GL import *
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import PySide2\n"
                             "Run:\npip3 install PySide2")


class GLSurfaceFormat(QtGui.QSurfaceFormat):
    def __init__(self, major: int = 4, minor: int = 3,
                 profile: QtGui.QSurfaceFormat.OpenGLContextProfile = QtGui.QSurfaceFormat.CoreProfile,
                 color_space: QtGui.QSurfaceFormat.ColorSpace = QtGui.QSurfaceFormat.sRGBColorSpace):
        """
        Class to specify settings for OpenGL.
        :param major: Set major OpenGL version.
        :param minor: Set minor OpenGL version.
        :param profile: Set OpenGL to work in Core/Legacy(compatibility) profile.
        :param color_space: Set Qt which color profile to use.
        """
        super().__init__()
        self.gl_major = major
        self.gl_minor = minor
        self.gl_profile = profile
        self.color_space = color_space

        self.__initSurface()

    def __initSurface(self):
        """
        Initiallize OpenGL settings.
        :return:
        """
        self.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        self.setMajorVersion(self.gl_major)
        self.setMinorVersion(self.gl_minor)
        self.setProfile(self.gl_profile)
        self.setColorSpace(self.color_space)
        # You can change it to TripleBuffer if your platform supports it
        self.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)

    def printDebugInfo(self):
        """
        Print set settings to console/terminal
        :return:
        """
        print(f"QT_SURFACE_FORMAT::{self.__class__.__name__}")
        print("------------------------------>")
        print(f"INFO::GL_MAJOR_VERSION::{self.majorVersion()}")
        print(f"INFO::GL_MINOR_VERSION::{self.minorVersion()}")
        print(f"INFO::GL_PROFILE::{str(self.profile()).split('.')[4]}")
        print(f"INFO::GL_SWAP_BEAHAVIOR::{str(self.swapBehavior()).split('.')[4]}")
        print(f"INFO::QT_RENDERABLE_TYPE::{str(self.renderableType()).split('.')[4]}")
        print(f"INFO::QT_COLOR_SPACE::{str(self.colorSpace()).split('.')[4]}")
        print("------------------------------>\n")


class Viewport(QtWidgets.QOpenGLWidget):
    def __init__(self, width: int, height: int, title :str="Qt OpenGl Window",
                 r: int=0.2, g: int=0.3, b: int=0.3, a: int=1.0):
        """
        Creates OpenGl widget with a 2d specified primitive
        :param width: Set widget width
        :param height: Set widget height
        :param title: Set window title
        :param r: Set red value for background
        :param g: Set green value for background
        :param b: Set blue value for background
        :param a: Set alpha value for background
        """
        super().__init__()
        self.width = width
        self.height = height
        self.bg_color = (r, g, b, a)

        self.setWindowTitle(title)
        self.resize(self.width, self.height)

        self.vertices = np.array([], dtype=np.float32)

        # Should be OpenGL.GL.shaders.ShaderProgram
        self.shader_program = None
        # Should be int to be used in "layout (location = attr_position)..."
        self.attr_position = None

    def initializeGL(self):
        """
        Initialize OpenGL context, Vertex buffer, Vertex array, shader and its attributes
        Calls paintGL after
        :return:
        """
        VBO = self.__createVBO(self.vertices)

        # Create and bind here once because we have only one VAO that there's no need to bind every time
        VAO = self.__createVAO()

        self.shader_program = self.__compileShaders(path_vertex="shaders/triangle.vs",
                                                    path_fragment="shaders/triangle.fs")
        self.attr_position = self.createAttribute(self.shader_program, "a_position", 0)

    def paintGL(self):
        """
        OpenGl main loop.
        :return:
        """
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(self.bg_color[0], self.bg_color[1],
                     self.bg_color[2], self.bg_color[3])
        glUseProgram(self.shader_program)
        glDrawArrays(GL_TRIANGLES, 0, 3)

    def resizeGL(self, w: int, h: int):
        """
        Resize OpenGL viewport. Calls paintGL after.
        :param w: Set new viewport width
        :param h: Set new viewport height
        :return:
        """
        glViewport(0, 0, w, h)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """
        Process events from keyboard.
        :param event: Event signal
        :return:
        """
        if event.key() == QtCore.Qt.Key_Escape:
            app.exit()
        event.accept()

    def printDebugInfo(self):
        """
        Print current OpenGL version
        :return:
        """
        print(f"QT_OPENGL_WIDGET::{self.__class__.__name__}")
        print("------------------------------>")
        print(f"INFO::GL_VERSION::{glGetString(GL_VERSION)}")
        print("------------------------------>\n")

    def __createVBO(self, vertices :np.ndarray):
        """
        Generate and bind Vertex buffer.
        :param vertices: Primitive vertices
        :return:
        """
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        return VBO

    def __createVAO(self):
        """
        Generate and bind Vertex array
        :return:
        """
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        return VAO

    def __compileShaders(self, path_vertex: str, path_fragment: str):
        """
        Read and compile .glsl shaders into a shader program
        :param path_vertex: Path to vertex shader
        :param path_fragment: Path to fragment shader
        :return:
        """
        with open(path_vertex, "r") as source:
            vertex = compileShader(source.read(), GL_VERTEX_SHADER)

        with open(path_fragment, "r") as source:
            fragment = compileShader(source.read(), GL_FRAGMENT_SHADER)

        shader_program = compileProgram(vertex, fragment)

        return shader_program

    def createAttribute(self, shader, attrib_name: str, stride: int):
        """
        Define and pass attribute that will be used in a shader
        :param shader: Shader to pass an attribute
        :param attrib_name: Attribute name. Should be similar as in shader.
        :param stride: Attribute position offset
        :return:
        """
        attribute = glGetAttribLocation(shader, attrib_name)
        glEnableVertexAttribArray(attribute)
        glVertexAttribPointer(attribute, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        return attribute

    def setVertices(self, vertex_list: list):
        """
        Set vertices to be used to draw a primitive.
        :param vertex_list: Array of points.
        :return:
        """
        vertices = np.array(vertex_list, dtype=np.float32)
        self.vertices = vertices



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    surface = GLSurfaceFormat()
    QtGui.QSurfaceFormat.setDefaultFormat(surface)
    surface.printDebugInfo()

    window = Viewport(1280, 720)

    vertices = [-0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0, 0.5, 0.0]
    window.setVertices(vertices)

    window.show()
    window.printDebugInfo()

    sys.exit(app.exec_())
