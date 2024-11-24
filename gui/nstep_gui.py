from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider)
from PyQt5.QtCore import Qt, QTimer

class nSTEPControlWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client

        # Main Layout
        self.setWindowTitle("nSTEP Focuser Control")
        main_layout = QVBoxLayout()

        # Temperature Display
        self.temp_label = QLabel("Temperature: --°C")
        main_layout.addWidget(self.temp_label)

        # Position Display
        self.position_label = QLabel("Position: --")
        main_layout.addWidget(self.position_label)

        # Direction Control
        direction_layout = QHBoxLayout()
        self.inward_button = QPushButton("Move Inward")
        self.outward_button = QPushButton("Move Outward")
        self.stop_button = QPushButton("Stop")
        direction_layout.addWidget(self.inward_button)
        direction_layout.addWidget(self.stop_button)
        direction_layout.addWidget(self.outward_button)
        main_layout.addLayout(direction_layout)

        # Connect direction buttons to nSTEP bindings
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

        # Timer for live updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # Update every second

        self.setLayout(main_layout)

    def set_property(self, property_name, value):
        """Set an nSTEP property using the client."""
        self.client.set_property(property_name, value)

    def get_property(self, property_name):
        """Get an nSTEP property using the client."""
        return self.client.get_property(property_name)

    def update_speed(self):
        """Update speed when slider value changes."""
        speed = self.speed_slider.value()
        self.set_property("nSTEP.FOCUSER_SPEED.SPEED", speed)

    def update_status(self):
        """Update temperature and position readings."""
        temp = self.get_property("nSTEP.FOCUSER_TEMPERATURE.TEMPERATURE")
        position = self.get_property("nSTEP.FOCUSER_POSITION.POSITION")
        self.temp_label.setText(f"Temperature: {temp:.2f}°C" if temp else "Temperature: --°C")
        self.position_label.setText(f"Position: {position:.0f}" if position else "Position: --")

'''
nSTEP.X_FOCUSER_STEPPING_MODE.WAVE = OFF
nSTEP.X_FOCUSER_STEPPING_MODE.HALF = OFF
nSTEP.X_FOCUSER_STEPPING_MODE.FULL = ON
nSTEP.X_FOCUSER_PHASE_WIRING.0 = ON
nSTEP.X_FOCUSER_PHASE_WIRING.1 = OFF
nSTEP.X_FOCUSER_PHASE_WIRING.2 = OFF
nSTEP.FOCUSER_SPEED.SPEED = 59.000000
nSTEP.FOCUSER_DIRECTION.MOVE_INWARD = ON
nSTEP.FOCUSER_DIRECTION.MOVE_OUTWARD = OFF
nSTEP.FOCUSER_STEPS.STEPS = 0.000000
nSTEP.FOCUSER_ABORT_MOTION.ABORT_MOTION = OFF
nSTEP.FOCUSER_BACKLASH.BACKLASH = 0.000000
nSTEP.FOCUSER_POSITION.POSITION = 1003.000000
nSTEP.FOCUSER_TEMPERATURE.TEMPERATURE = 11.000000
nSTEP.FOCUSER_COMPENSATION.COMPENSATION = -0.000000
nSTEP.FOCUSER_MODE.MANUAL = ON
nSTEP.FOCUSER_MODE.AUTOMATIC = OFF
nSTEP.INFO.DEVICE_NAME = "nSTEP"
nSTEP.INFO.DEVICE_DRIVER = "indigo_focuser_nstep"
nSTEP.INFO.DEVICE_VERSION = "2.0.0.6"
nSTEP.INFO.DEVICE_INTERFACE = "8"
nSTEP.CONFIG.LOAD = OFF
nSTEP.CONFIG.SAVE = OFF
nSTEP.CONFIG.REMOVE = OFF
nSTEP.PROFILE_NAME.NAME_0 = "Profile #0"
nSTEP.PROFILE_NAME.NAME_1 = "Profile #1"
nSTEP.PROFILE_NAME.NAME_2 = "Profile #2"
nSTEP.PROFILE_NAME.NAME_3 = "Profile #3"
nSTEP.PROFILE_NAME.NAME_4 = "Profile #4"
Configuration Agent.AGENT_CONFIG_PROFILES.Mount PMC Eight = "PROFILE_0"
Configuration Agent.AGENT_CONFIG_PROFILES.Mount PMC Eight (guider) = "PROFILE_0"
Configuration Agent.AGENT_CONFIG_PROFILES.nSTEP = "PROFILE_0"
nSTEP.PROFILE.PROFILE_0 = ON
nSTEP.PROFILE.PROFILE_1 = OFF
nSTEP.PROFILE.PROFILE_2 = OFF
nSTEP.PROFILE.PROFILE_3 = OFF
nSTEP.PROFILE.PROFILE_4 = OFF
nSTEP.DEVICE_PORT.PORT = "/dev/ttyACM0"
nSTEP.DEVICE_PORTS.REFRESH = OFF
nSTEP.DEVICE_PORTS./dev/ttyACM0 = OFF
nSTEP.DEVICE_PORTS./dev/ttyUSB0 = OFF
nSTEP.ADDITIONAL_INSTANCES.COUNT = 0.000000
nSTEP.CONNECTION.CONNECTED = ON
nSTEP.CONNECTION.DISCONNECTED = OFF
'''