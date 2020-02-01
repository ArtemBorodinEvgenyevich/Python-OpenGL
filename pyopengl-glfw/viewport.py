from utilities.exception_dialog import ExceptionDialog

try:
    import glfw
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import GLFW\n"
                             "Run:\npip3 install glfw")

try:
    from OpenGL.GL import *
except ImportError:
    dialog = ExceptionDialog("ImportError::Cannot import PyOpenGL\n"
                             "Run:\npip3 install PyOpenGL")



class Viewport(object):
    def __init__(self, widht, height, title="OpenGL Window", r=0.2, g=0.3, b=0.3, a=1.0):
        super().__init__()
        self.widht = widht
        self.height = height
        self.window_title = title
        self.bg_color = (r, g, b, a)

        self.__check_glfw()
        self.window = self.__create_window()


    def main_loop(self):
        while not glfw.window_should_close(self.window):
            self.processEvents(self.window)

            glClearColor(self.bg_color[0], self.bg_color[1],
                         self.bg_color[2], self.bg_color[3])
            glClear(GL_COLOR_BUFFER_BIT)

            # DO STUFF HERE
            #--------------

            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def processEvents(self, window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) is glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def __create_window(self):
        window = glfw.create_window(self.widht, self.height, self.window_title, None, None)
        # check if window was created
        if not window:
            glfw.terminate()
            dialog = ExceptionDialog("GLWFError::Cannot initialize window")

        glfw.set_window_pos(window, 400, 200)
        glfw.make_context_current(window)

        return window

    def __check_glfw(self):
        # Initiallize gflw
        if not glfw.init():
            dialog = ExceptionDialog("GLFWError::The GLFW lib cannot initialized")


if __name__ == '__main__':
    window = Viewport(1280, 720, "Test window ")
    window.main_loop()
