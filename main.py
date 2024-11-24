from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea
from indigo.client import INDIGOClient
from indigo.mount_agent import MountAgent
from indigo.scripting_agent import ScriptingAgent

from gui.mount_gui import MountControlWidget
from gui.server_control import ServerControlWidget
from gui.nstep_gui import nSTEPControlWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automated Solar Telescope Control Panel")
        self.setGeometry(100, 100, 1200, 800)

        # Multi-document interface
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        # INDIGO Client (not connected by default)
        self.client = INDIGOClient(host="raspberrypi.local", port=7624)

        # Mount Agent
        self.mount_agent = MountAgent(self.client)

        # Scripting Agent
        self.scripting_agent = ScriptingAgent(self.client)

        # Add GUI Modules
        self.add_module(ServerControlWidget(self.client), "Server Control")
        self.add_module(nSTEPControlWidget(self.client), "nSTEP Focuser")
        self.add_module(MountControlWidget(self.mount_agent), "Mount Control")
        

    def add_module(self, module_widget, title):
        """Add a GUI module as a subwindow."""
        sub_window = self.mdi_area.addSubWindow(module_widget)
        sub_window.setWindowTitle(title)
        sub_window.resize(400, 300)
        sub_window.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
