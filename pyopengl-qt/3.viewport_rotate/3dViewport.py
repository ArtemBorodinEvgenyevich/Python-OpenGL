import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
from PySide2 import QtGui, QtCore, QtWidgets


class GLSurfaceFormat(QtGui.QSurfaceFormat):
    """Setup OpenGL preferences."""
    def __init__(self):
        super(GLSurfaceFormat, self).__init__()
        self.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        self.setMinorVersion(3)
        self.setMajorVersion(4)
        self.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        # FIXME: Check for debug flag!
        self.setOption(QtGui.QSurfaceFormat.DebugContext)
        self.setColorSpace(QtGui.QSurfaceFormat.sRGBColorSpace)
        self.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)
        self.setSamples(4)


class ViewportWidget(QtWidgets.QOpenGLWidget):
    """Main 3D scene viewer."""

    def __init__(self):
        super(ViewportWidget, self).__init__(parent=None)

        # --- Setup widget attributes ---
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)

        # --- Setup View Projection matrices
        self.m_projectionMatrix = QtGui.QMatrix4x4()
        self.m_viewMatrix = QtGui.QMatrix4x4()

        self.m_mousePos = QtGui.QVector2D()
        self.m_viewRotation = QtGui.QQuaternion()

        # TODO: Should be abstracted. Initialized in paintGL for clarity.
        self.gr_vao = None
        self.gr_vbo = None
        self.gr_ebo = None
        self.gr_shaderProg = None

        self.mark_vao = None
        self.mark_vbo = None
        self.mark_ebo = None
        self.mark_shaderProg = None

    def initializeGL(self):
        gl.glEnable(gl.GL_DEPTH_TEST)

        gl.glClearColor(0.4, 0.4, 0.4, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT, gl.GL_DEPTH_BUFFER_BIT)

        # -- Grid object --
        with open("shaders/grid_fragment.glsl", 'r') as f:
            fragment = compileShader(f.read(), gl.GL_FRAGMENT_SHADER)
        with open("shaders/grid_vertex.glsl", "r") as f:
            vertex = compileShader(f.read(), gl.GL_VERTEX_SHADER)
        self.gr_shaderProg = compileProgram(vertex, fragment)

        grid_vertices = np.array(
            [
                 # Vertex positions     # UVs
                 0.5,  0.5, 0.0,        1.0, 1.0,
                 0.5, -0.5, 0.0,        1.0, 0.0,
                -0.5, -0.5, 0.0,        0.0, 0.0,
                -0.5,  0.5, 0.0,        0.0, 1.0
            ], dtype=ctypes.c_float
        )
        grid_indices = np.array(
            [
                0, 1, 3,
                1, 2, 3
            ], dtype=ctypes.c_uint
        )

        self.gr_vao = gl.glGenVertexArrays(1)
        self.gr_vbo = gl.glGenBuffers(1)
        self.gr_ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.gr_vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.gr_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, grid_vertices.nbytes, grid_vertices, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.gr_ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, grid_indices.nbytes, grid_indices, gl.GL_STATIC_DRAW)

        # Position attribute
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))

        # Texture coordinates attribute
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 5 * ctypes.sizeof(ctypes.c_float),
                                 ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        # --------------------------------------------------------------------------------------------------------

        # -- Center marker --
        with open("shaders/mark_fragment.glsl", 'r') as f:
            fragment = compileShader(f.read(), gl.GL_FRAGMENT_SHADER)
        with open("shaders/mark_vertex.glsl", "r") as f:
            vertex = compileShader(f.read(), gl.GL_VERTEX_SHADER)
        self.mark_shaderProg = compileProgram(vertex, fragment)

        grid_vertices = np.array(
            [
                 # Vertex positions
                 0.5,  0.5, 0.0,
                 0.5, -0.5, 0.0,
                -0.5, -0.5, 0.0,
                -0.5,  0.5, 0.0,
            ], dtype=ctypes.c_float
        )
        grid_indices = np.array(
            [
                0, 1, 3,
                1, 2, 3
            ], dtype=ctypes.c_uint
        )

        self.mark_vao = gl.glGenVertexArrays(1)
        self.mark_vbo = gl.glGenBuffers(1)
        self.mark_ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.mark_vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.mark_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, grid_vertices.nbytes, grid_vertices, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.mark_ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, grid_indices.nbytes, grid_indices, gl.GL_STATIC_DRAW)

        # Position attribute
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))

    def paintGL(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # TODO: Put model matrix into model entity
        # This is a *grid* model matrix
        gridModelMatrix = QtGui.QMatrix4x4()
        gridModelMatrix.rotate(90, QtGui.QVector3D(1.0, 0.0, 0.0))
        gridModelMatrix.scale(1000)

        markerModelMatrix = QtGui.QMatrix4x4()
        markerModelMatrix.rotate(90, QtGui.QVector3D(1.0, 0.0, 0.0))

        self.m_viewMatrix.setToIdentity()
        self.m_viewMatrix.lookAt(QtGui.QVector3D(0.0, 5.0, -10.0),
                                 QtGui.QVector3D(0.0, 0.0, 0.0),
                                 QtGui.QVector3D(0.0, 1.0, 0.0))
        self.m_viewMatrix.rotate(self.m_viewRotation)

        # -- Draw grid --
        gl.glUseProgram(self.gr_shaderProg)

        u_projection_loc = gl.glGetUniformLocation(self.gr_shaderProg, "u_projectionMatrix")
        gl.glUniformMatrix4fv(u_projection_loc, 1, gl.GL_FALSE, self.m_projectionMatrix.data())

        u_view_loc = gl.glGetUniformLocation(self.gr_shaderProg, "u_viewMatrix")
        gl.glUniformMatrix4fv(u_view_loc, 1, gl.GL_FALSE, self.m_viewMatrix.data())

        u_model_loc = gl.glGetUniformLocation(self.gr_shaderProg, "u_modelMatrix")
        gl.glUniformMatrix4fv(u_model_loc, 1, gl.GL_FALSE, gridModelMatrix.data())

        gl.glBindVertexArray(self.gr_vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # -- Draw marker --
        gl.glUseProgram(self.mark_shaderProg)

        u_projection_loc = gl.glGetUniformLocation(self.mark_shaderProg, "u_projectionMatrix")
        gl.glUniformMatrix4fv(u_projection_loc, 1, gl.GL_FALSE, self.m_projectionMatrix.data())

        u_view_loc = gl.glGetUniformLocation(self.mark_shaderProg, "u_viewMatrix")
        gl.glUniformMatrix4fv(u_view_loc, 1, gl.GL_FALSE, self.m_viewMatrix.data())

        u_model_loc = gl.glGetUniformLocation(self.mark_shaderProg, "u_modelMatrix")
        gl.glUniformMatrix4fv(u_model_loc, 1, gl.GL_FALSE, markerModelMatrix.data())

        gl.glBindVertexArray(self.mark_vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

    def resizeGL(self, w: int, h: int):
        aspect = w / h
        self.m_projectionMatrix.setToIdentity()
        self.m_projectionMatrix.perspective(45, aspect, 0.1, 1000.0)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            self.setFocus()
        elif event.type() == QtCore.QEvent:
            self.clearFocus()

        return super(ViewportWidget, self).eventFilter(watched, event)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.m_mousePos = QtGui.QVector2D(event.localPos())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            diff = QtGui.QVector2D(event.localPos()) - self.m_mousePos
            self.m_mousePos = QtGui.QVector2D(event.localPos())

            angle = diff.length() / 2.0
            axis = QtGui.QVector3D(diff.y(), diff.x(), 0.0)
            self.m_viewRotation = QtGui.QQuaternion.fromAxisAndAngle(axis, angle) * self.m_viewRotation

            self.update()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    surface = GLSurfaceFormat()
    QtGui.QSurfaceFormat.setDefaultFormat(surface)

    window = ViewportWidget()
    window.show()

    sys.exit(app.exec_())