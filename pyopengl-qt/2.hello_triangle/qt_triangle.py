import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from PySide2 import QtWidgets, QtCore, QtGui


class GLSurfaceFormat(QtGui.QSurfaceFormat):
    """Setup OpenGL preferences."""
    def __init__(self):
        super(GLSurfaceFormat, self).__init__()
        self.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        self.setMinorVersion(3)
        self.setMajorVersion(4)
        self.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        # FIXME: only for debug!
        self.setOption(QtGui.QSurfaceFormat.DebugContext)
        self.setColorSpace(QtGui.QSurfaceFormat.sRGBColorSpace)
        self.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)
        self.setSamples(4)

    def printSurfaceInfo(self):
        """Get renderer info."""
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

        self.polygon_mode = GL_FILL

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
        glPolygonMode(GL_FRONT_AND_BACK, self.polygon_mode)

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
        glPolygonMode(GL_FRONT_AND_BACK, self.polygon_mode)

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
        W - for wireframe, P - for point, F - for full fill
        :param event: Event signal
        :return:
        """
        if event.key() == QtCore.Qt.Key_Escape:
            app.exit()

        if event.key() == QtCore.Qt.Key_W:
            self.polygon_mode = GL_LINE
            self.update()

        if event.key() == QtCore.Qt.Key_F:
            self.polygon_mode = GL_FILL
            self.update()

        if event.key() == QtCore.Qt.Key_P:
            self.polygon_mode = GL_POINT
            self.update()

        event.accept()

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

    window = Viewport(1280, 720)

    vertices = [-0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0, 0.5, 0.0]
    window.setVertices(vertices)
    window.show()

    sys.exit(app.exec_())
