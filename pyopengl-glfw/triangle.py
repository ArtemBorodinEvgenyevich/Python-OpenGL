import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Viewport(object):
    def __init__(self, width, height, title="OpenGL Window", r=0.2, g=0.3, b=0.3, a=1.0):
        super().__init__()
        self.width = width
        self.height = height
        self.window_title = title
        self.bg_color = (r, g, b, a)

        # !!! MUST BE SET AS NDARRAY FROM NUMPY !!!
        self.vertices = np.array([], dtype=np.float32)

        self.__check_glfw()
        self.__setup_glfw()
        self.window = self.__create_window()

    def main_loop(self):
        self.__check_vertices(self.vertices, True)

        self.VBO = self.__createVBO(self.vertices)
        self.VAO = self.__createVAO()

        self.shaderProgram = self.__compile_shaders(path_vertex="shaders/triangle.vs",
                                                    path_fragment="shaders/triangle.fs")
        self.attr_position = self.create_attribute(self.shaderProgram, "a_position", 0)

        # MAIN LOOP
        # ---------
        while not glfw.window_should_close(self.window):
            self.__process_events(self.window)

            glClearColor(self.bg_color[0], self.bg_color[1],
                         self.bg_color[2], self.bg_color[3])
            glClear(GL_COLOR_BUFFER_BIT)

            # DO STUFF HERE
            # -------------
            glUseProgram(self.shaderProgram)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            # -------------

            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def create_attribute(self, shader, attrib_name: str, stride: int):
        attribute = glGetAttribLocation(shader, attrib_name)
        glEnableVertexAttribArray(attribute)
        glVertexAttribPointer(attribute, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        return attribute

    def set_vertices(self, vertex_list: list):
        vertices = np.array(vertex_list, dtype=np.float32)
        self.vertices = vertices

    def __createVAO(self):
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        return VAO

    def __createVBO(self, vertices):
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        return VBO

    def __compile_shaders(self, path_vertex: str, path_fragment: str):
        with open(path_vertex, "r") as source:
            vertex = compileShader(source.read(), GL_VERTEX_SHADER)

        with open(path_fragment, "r") as source:
            fragment = compileShader(source.read(), GL_FRAGMENT_SHADER)

        shader_program = compileProgram(vertex, fragment)

        return shader_program

    def __create_window(self):
        window = glfw.create_window(self.width, self.height, self.window_title, None, None)

        glfw.set_window_pos(window, 400, 200)
        glfw.set_window_size_callback(window, self.__resize_window)
        glfw.make_context_current(window)

        return window

    def __resize_window(self, window, width: int, height: int):
        glViewport(0, 0, width, height)

    @staticmethod
    def __process_events(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) is glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if glfw.get_key(window, glfw.KEY_F) == glfw.PRESS:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)

    @staticmethod
    def __check_glfw():
        # Initiallize gflw
        if not glfw.init():
            raise RuntimeError("GLFW initialization error")

    @staticmethod
    def __check_vertices(vertices: np.ndarray, show_coordinates: bool):
        if vertices.nbytes is 0:
            print("DEBUG::NO_VERTICES_ARE_SPECIFIED")

            return
        print("DEBUG::VERTICES_ARE_SPECIFIED")

        if show_coordinates is True:
            print("DEBUG::PRINT_VERTICES_COORDINATES")
            print("----------------------------------->")
            print(vertices)
            print("----------------------------------->")

    @staticmethod
    def __setup_glfw():
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


if __name__ == '__main__':
    window = Viewport(1280, 720, "Test window ")

    vertices = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0,  0.5, 0.0]
    window.set_vertices(vertices)

    window.main_loop()
