
import sys
from OpenGL.GL import *
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


class nViewport(QtWidgets.QOpenGLWidget):
    def __init__(self, width, height, title="Qt OpenGl Window", r=0.2, g=0.3, b=0.3, a=1.0):
        super().__init__()
        self.width = width
        self.height = height
        self.bg_color = (r, g, b, a)

        self.setWindowTitle(title)
        self.resize(self.width, self.height)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    surface = GLSurfaceFormat()
    QtGui.QSurfaceFormat.setDefaultFormat(surface)
    surface.printSurfaceInfo()

    window = nViewport(1280, 720)
    window.show()

    sys.exit(app.exec_())
