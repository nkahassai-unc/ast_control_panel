from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame
from PyQt5.QtGui import QFont, QPixmap

from indigo.client import INDIGOClient
from indigo.mount_agent import MountAgent
from indigo.scripting_agent import ScriptingAgent

from gui.mount_gui import MountControlWidget
from gui.server_gui import ServerControlWidget
from gui.nstep_gui import nSTEPControlWidget
from gui.scripting_gui import ScriptingWidget
from gui.weather_gui import WeatherWidget
from gui.calculations_gui import CalculationsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automated Solar Telescope Control Panel")
        self.setGeometry(100, 100, 800, 1000)

        # INDIGO Client
        self.client = INDIGOClient(host="raspberrypi.local", port=7624)

        # Agents
        self.mount_agent = MountAgent(self.client)
        self.scripting_agent = ScriptingAgent(self.client)

        # Arduino Etalons
        #self.dome_etalon = xxxxx

        # Arduino Dome
        #self.dome_etalon = xxxxxx

        # File Transfer
        #self.file_transfer = xxxxx

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QVBoxLayout(self.central_widget)

        # Add Banner
        self.add_banner(main_layout)

        # Add Grid Layout for Modules
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        # First Column (4 rows)
        self.add_module_to_grid(grid_layout, ServerControlWidget(self.client), "Server Control", 0, 0)
        self.add_module_to_grid(grid_layout, MountControlWidget(self.mount_agent), "Mount Control", 1, 0)
        self.add_module_to_grid(grid_layout, CalculationsWidget(), "Calculations", 2, 0)
        self.add_module_to_grid(grid_layout, WeatherWidget(api_key="10b2f1d4a200b534bb2d4bf69bddcace", latitude=35.9132, longitude=-79.0558), "Weather Monitor", 3, 0)

        # Second Column (3 rows)
        self.add_module_to_grid(grid_layout, QLabel("!!Dome Camera Placeholder"), "Dome Cam", 0, 1)
        self.add_module_to_grid(grid_layout, QLabel("#Dome Control Placeholder"), "Dome Control", 1, 1)
        self.add_module_to_grid(grid_layout, QLabel("#Etalon Control Placeholder"), "Etalon Control", 2, 1)

        # Third Column (3 rows)
        self.add_module_to_grid(grid_layout, QLabel("!!Science Camera Placeholder"), "Science Cam", 0, 2)
        self.add_module_to_grid(grid_layout, nSTEPControlWidget(self.client), "nSTEP Focuser", 1, 2)
        self.add_module_to_grid(grid_layout, ScriptingWidget(self.scripting_agent), "Scripting Module", 2, 2)

    def add_banner(self, layout):
        """Add a banner to the top of the control panel."""
        banner_frame = QFrame()
        banner_frame.setFrameShape(QFrame.StyledPanel)
        banner_layout = QVBoxLayout(banner_frame)

        # Remove extra margins and spacing
        banner_layout.setContentsMargins(0, 0, 0, 0)  # Top, left, right, bottom margins
        banner_layout.setSpacing(0)  # Space between widgets in the layout

        # Banner Logo
        logo = QLabel()
        pixmap = QPixmap('ast_panel_logo.png')  # Replace with the correct relative or absolute path
        logo.setPixmap(pixmap.scaled(800, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignLeft)

        # Add to Banner Layout
        banner_layout.addWidget(logo)
        layout.addWidget(banner_frame)

    def add_module_to_grid(self, grid_layout, module_widget, title, row, col):
        """Add a module widget to the grid layout."""
        module_frame = QFrame()
        module_frame.setFrameShape(QFrame.StyledPanel)
        module_frame.setLayout(QVBoxLayout())

        # Add Title
        module_title = QLabel(title)
        module_title.setFont(QFont("Arial", 14, QFont.Bold))
        module_title.setAlignment(Qt.AlignCenter)
        module_frame.layout().addWidget(module_title)

        # Add Module Widget
        module_frame.layout().addWidget(module_widget)
        grid_layout.addWidget(module_frame, row, col)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()