# This file contains the GUI for the mount control.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QComboBox, QHBoxLayout
from PyQt5.QtCore import QTimer

class MountControlWidget(QWidget):
    def __init__(self, mount_agent):
        super().__init__()
        self.mount_agent = mount_agent

        # Layout
        self.setWindowTitle("Mount Control")
        layout = QVBoxLayout()

        # RA/DEC Display
        self.ra_dec_label = QLabel("RA: 0.0, DEC: 0.0")
        layout.addWidget(self.ra_dec_label)

        # D-Pad for Movement
        dpad_layout = QGridLayout()

        # Create buttons
        self.north_button = QPushButton("N")
        self.south_button = QPushButton("S")
        self.east_button = QPushButton("E")
        self.west_button = QPushButton("W")
        self.stop_button = QPushButton("Stop")

        # Set square dimensions for buttons
        button_size = 60
        for button in [self.north_button, self.south_button, self.east_button, self.west_button, self.stop_button]:
            button.setFixedSize(button_size, button_size)

        # Add buttons to the grid layout
        dpad_layout.addWidget(self.north_button, 0, 1)
        dpad_layout.addWidget(self.south_button, 2, 1)
        dpad_layout.addWidget(self.east_button, 1, 2)
        dpad_layout.addWidget(self.west_button, 1, 0)
        dpad_layout.addWidget(self.stop_button, 1, 1)

        layout.addLayout(dpad_layout)

        # Connect Buttons
        self.north_button.clicked.connect(lambda: self.mount_agent.move("N"))
        self.south_button.clicked.connect(lambda: self.mount_agent.move("S"))
        self.east_button.clicked.connect(lambda: self.mount_agent.move("E"))
        self.west_button.clicked.connect(lambda: self.mount_agent.move("W"))
        self.stop_button.clicked.connect(self.mount_agent.stop)

        # Speed Selector
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Slew Speed:")
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.1x", "0.5x", "1x", "2x"])
        self.speed_combo.currentIndexChanged.connect(
            lambda: self.mount_agent.set_speed(self.speed_combo.currentText())
        )
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_combo)
        layout.addLayout(speed_layout)

        # Tracking Mode
        tracking_layout = QHBoxLayout()
        self.sidereal_button = QPushButton("Sidereal")
        self.solar_button = QPushButton("Solar")
        tracking_layout.addWidget(self.sidereal_button)
        tracking_layout.addWidget(self.solar_button)
        self.sidereal_button.clicked.connect(lambda: self.mount_agent.set_tracking("Sidereal"))
        self.solar_button.clicked.connect(lambda: self.mount_agent.set_tracking("Solar"))
        layout.addLayout(tracking_layout)

        # Timer for RA/DEC
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ra_dec)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_ra_dec(self):
        """Update RA/DEC labels."""
        try:
            ra, dec = self.mount_agent.get_ra_dec()
            self.ra_dec_label.setText(f"RA: {ra:.2f}, DEC: {dec:.2f}")
        except Exception as e:
            self.ra_dec_label.setText("Error fetching RA/DEC")
