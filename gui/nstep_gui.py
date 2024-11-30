# This file contains the GUI for the nSTEP focuser control.

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider)
from PyQt5.QtCore import Qt, QTimer


class nSTEPControlWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client

        # Main Layout
        self.setWindowTitle("nSTEP Focuser Control")
        main_layout = QVBoxLayout()
        self.setMinimumSize(300, 100)


        # Temperature Display
        self.temperature_label = QLabel("Temperature: -- °C")
        main_layout.addWidget(self.temperature_label)

        # Position Display
        self.position_label = QLabel("Position: --")
        main_layout.addWidget(self.position_label)

        # Speed Display
        self.speed_label = QLabel("Speed: --")
        main_layout.addWidget(self.speed_label)

        # Direction Control
        direction_layout = QHBoxLayout()
        self.inward_button = QPushButton("Move Inward")
        self.outward_button = QPushButton("Move Outward")
        self.stop_button = QPushButton("Stop")
        direction_layout.addWidget(self.inward_button)
        direction_layout.addWidget(self.stop_button)
        direction_layout.addWidget(self.outward_button)
        main_layout.addLayout(direction_layout)

        # Connect Direction Buttons to Properties
        self.inward_button.clicked.connect(lambda: self.set_property("nSTEP.FOCUSER_DIRECTION.MOVE_INWARD", True))
        self.outward_button.clicked.connect(lambda: self.set_property("nSTEP.FOCUSER_DIRECTION.MOVE_OUTWARD", True))
        self.stop_button.clicked.connect(lambda: self.set_property("nSTEP.FOCUSER_ABORT_MOTION.ABORT_MOTION", True))

        # Speed Control
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Speed Control")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 100)  # Speed range: 1% to 100%
        self.speed_slider.setValue(50)  # Default speed: 50%
        self.speed_slider.valueChanged.connect(self.update_speed)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        main_layout.addLayout(speed_layout)

        # Timer for Live Updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # Update every second

        self.setLayout(main_layout)

    def set_property(self, property_name, value):
        """Set an nSTEP property using the client."""
        try:
            self.client.set_property(property_name, value)
        except Exception as e:
            print(f"Error setting property {property_name}: {e}")

    def get_property(self, property_name):
        """Get an nSTEP property using the client."""
        try:
            return self.client.get_property(property_name)
        except Exception as e:
            print(f"Error getting property {property_name}: {e}")
            return None

    def update_speed(self):
        """Update speed when slider value changes."""
        speed = self.speed_slider.value()
        self.set_property("nSTEP.FOCUSER_SPEED.SPEED", speed)
        self.speed_label.setText(f"Speed: {speed}")

    def update_status(self):
        """Update the GUI with current focuser status."""
        temp = self.get_property("nSTEP.FOCUSER_TEMPERATURE.TEMPERATURE") or "--"
        position = self.get_property("nSTEP.FOCUSER_POSITION.POSITION") or "--"

        self.temperature_label.setText(f"Temperature: {temp} °C")
        self.position_label.setText(f"Position: {position}")