from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea
from gui.mount_control import MountControl
from gui.scripting import ScriptingModule

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AST Control Panel")
        self.setGeometry(100, 100, 1200, 800)

        # Multi-document interface for modular windows
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        # Add Mount Control Module
        mount_control = MountControl()
        self.mdi_area.addSubWindow(mount_control)

        # Add Scripting Module
        scripting_module = ScriptingModule()
        self.mdi_area.addSubWindow(scripting_module)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()