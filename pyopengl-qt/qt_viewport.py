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
        super().__init__()
        self.gl_major = major
        self.gl_minor = minor
        self.gl_profile = profile
        self.color_space = color_space

        self.__initSurface()

    def __initSurface(self):
        self.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        self.setMajorVersion(self.gl_major)
        self.setMinorVersion(self.gl_minor)
        self.setProfile(self.gl_profile)
        self.setColorSpace(self.color_space)
        # You can change it to TripleBuffer if your platform supports it
        self.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)

    def printDebugInfo(self):
        print(f"QT_SURFACE_FORMAT::{self.__class__.__name__}")
        print("------------------------------>")
        print(f"INFO::GL_MAJOR_VERSION::{self.majorVersion()}")
        print(f"INFO::GL_MINOR_VERSION::{self.minorVersion()}")
        print(f"INFO::GL_PROFILE::{str(self.profile()).split('.')[4]}")
        print(f"INFO::GL_SWAP_BEAHAVIOR::{str(self.swapBehavior()).split('.')[4]}")
        print(f"INFO::QT_RENDERABLE_TYPE::{str(self.renderableType()).split('.')[4]}")
        print(f"INFO::QT_COLOR_SPACE::{str(self.colorSpace()).split('.')[4]}")
        print("------------------------------>\n")


class nViewport(QtWidgets.QOpenGLWidget):
    def __init__(self, width, height, title="Qt OpenGl Window", r=0.2, g=0.3, b=0.3, a=1.0):
        super().__init__()
        self.widht = width
        self.height = height
        self.bg_color = (r, g, b, a)

        self.setWindowTitle(title)
        self.resize(self.widht, self.height)

    def initializeGL(self):
        pass

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(self.bg_color[0], self.bg_color[1],
                     self.bg_color[2], self.bg_color[3])

    def resizeGL(self, w:int, h:int):
        glViewport(0, 0, w, h)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            app.exit()
        event.accept()

    def printDebugInfo(self):
        print(f"QT_OPENGL_WIDGET::{self.__class__.__name__}")
        print("------------------------------>")
        print(f"INFO::GL_VERSION::{glGetString(GL_VERSION)}")
        print("------------------------------>\n")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    surface = GLSurfaceFormat()
    QtGui.QSurfaceFormat.setDefaultFormat(surface)
    surface.printDebugInfo()

    window = nViewport(1280, 720)
    window.show()
    window.printDebugInfo()

    sys.exit(app.exec_())
