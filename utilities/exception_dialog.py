from PySide2 import QtWidgets
import sys

class ExceptionDialog(object):
    def __init__(self, exception_name="exception"):
        super().__init__()

        self.exception = exception_name
        self.__init_dialog()

    def __init_dialog(self):
        app = QtWidgets.QApplication()
        message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "OpenGL sample",
                                           "Error has been occured at start!",
                                           QtWidgets.QMessageBox.Close)
        message_box.setDetailedText(f"{self.exception}")
        message_box.exec_()
        sys.exit(1)