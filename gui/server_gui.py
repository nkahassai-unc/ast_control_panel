# This file contains the GUI for connecting to the server control.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

class ServerControlWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setWindowTitle("Server Control")
        self.setMinimumSize(300, 100)

        # Layout
        layout = QVBoxLayout()

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        layout.addWidget(self.connect_button)

        # Disconnect Button
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        layout.addWidget(self.disconnect_button)

        # Log Area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def connect_to_server(self):
        """Connect to the INDIGO server."""
        try:
            self.client.connect()
            self.log_area.append("Connected to INDIGO server.")
        except Exception as e:
            self.log_area.append(f"Failed to connect: {e}")

    def disconnect_from_server(self):
        """Disconnect from the INDIGO server."""
        try:
            self.client.disconnect()
            self.log_area.append("Disconnected from INDIGO server.")
        except Exception as e:
            self.log_area.append(f"Failed to disconnect: {e}")
