# This file contains the GUI for the Scripting module.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class ScriptingWidget(QWidget):
    def __init__(self, scripting_agent):
        super().__init__()  # Properly call the QWidget constructor
        self.scripting_agent = scripting_agent
        self.setWindowTitle("Scripting Module")

        # Layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add a title label
        title_label = QLabel("Available Scripts")
        self.layout.addWidget(title_label)

        # Dynamically populate the UI with script controls
        self.scripts = self.scripting_agent.list_scripts()
        self.create_ui()

    def create_ui(self):
        """Create a UI for managing scripts."""
        for script in self.scripts:
            script_layout = QHBoxLayout()

            # Script name label
            script_name_label = QLabel(script["name"])
            script_layout.addWidget(script_name_label)

            # Run button
            run_button = QPushButton("Run")
            run_button.clicked.connect(lambda _, s=script["name"]: self.scripting_agent.run_script(s))
            script_layout.addWidget(run_button)

            # Stop button
            stop_button = QPushButton("Stop")
            stop_button.clicked.connect(lambda _, s=script["name"]: self.scripting_agent.stop_script(s))
            script_layout.addWidget(stop_button)

            self.layout.addLayout(script_layout)