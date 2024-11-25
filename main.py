# Main entry point for the AST Control Panel application.

from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea
from indigo.client import INDIGOClient
from indigo.mount_agent import MountAgent
from indigo.scripting_agent import ScriptingAgent

from gui.mount_gui import MountControlWidget
from gui.server_gui import ServerControlWidget
from gui.nstep_gui import nSTEPControlWidget
from gui.scripting_gui import ScriptingWidget
from gui.weather_gui import WeatherWidget



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


        # Add Server Control Modules
        self.add_module(ServerControlWidget(self.client), "Server Control")
        # Add nSTEP Focuser Module
        self.add_module(nSTEPControlWidget(self.client), "nSTEP Focuser")
        # Add Mount Control Module
        self.add_module(MountControlWidget(self.mount_agent), "Mount Control")
        
        # Add Weather Module
        self.add_module(WeatherWidget(api_key="10b2f1d4a200b534bb2d4bf69bddcace", latitude=35.9132, longitude=-79.0558), "Weather Monitor")
        # Add Scripting Module
        self.add_module(ScriptingWidget(self.scripting_agent), "Scripting Module")


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
