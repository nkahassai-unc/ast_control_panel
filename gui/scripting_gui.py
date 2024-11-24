from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class ScriptingAgent:
    def __init__(self, client):
        self.client = client

    def list_scripts(self):
        """Fetch a list of available scripts from the server."""
        try:
            response = self.client.get_property("ScriptingAgent.SCRIPTS")
            return response if response else []
        except Exception as e:
            print(f"Error fetching scripts: {e}")
            return []

    def run_script(self, script_name):
        """Send a command to the server to run a script."""
        try:
            self.client.set_property(f"ScriptingAgent.RUN.{script_name}", True)
            print(f"Running {script_name}...")
        except Exception as e:
            print(f"Error running script {script_name}: {e}")

    def stop_script(self, script_name):
        """Send a command to the server to stop a script."""
        try:
            self.client.set_property(f"ScriptingAgent.STOP.{script_name}", True)
            print(f"Stopping {script_name}...")
        except Exception as e:
            print(f"Error stopping script {script_name}: {e}")


class ScriptingGUI(QWidget):
    def __init__(self, client):
        super().__init__()
        self.setWindowTitle("Scripting Module")
        self.setMinimumSize(400, 300)

        self.scripting_agent = ScriptingAgent(client)

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Fetch scripts and build UI
        self.scripts = self.scripting_agent.list_scripts()
        self.create_ui()

    def create_ui(self):
        """Create the GUI for scripting management."""
        for script in self.scripts:
            # Horizontal layout for each script
            script_layout = QHBoxLayout()

            # Script name label
            label = QLabel(script["name"])
            script_layout.addWidget(label)

            # Run button
            run_button = QPushButton("Run")
            run_button.clicked.connect(lambda _, s=script["name"]: self.run_script(s))
            script_layout.addWidget(run_button)

            # Stop button
            stop_button = QPushButton("Stop")
            stop_button.clicked.connect(lambda _, s=script["name"]: self.stop_script(s))
            script_layout.addWidget(stop_button)

            # Add script layout to main layout
            self.layout.addLayout(script_layout)

    def run_script(self, script_name):
        """Handle Run button click."""
        self.scripting_agent.run_script(script_name)

    def stop_script(self, script_name):
        """Handle Stop button click."""
        self.scripting_agent.stop_script(script_name)
