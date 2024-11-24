class ScriptingAgent:
    def __init__(self, client):
        self.client = client

    def list_scripts(self):
        """Fetch the list of available scripts."""
        try:
            scripts = self.client.get_property("Scripting Agent.SCRIPT_LIST")
            return scripts or []
        except Exception as e:
            print(f"Error fetching scripts: {e}")
            return []

    def run_script(self, script_name):
        """Run a script."""
        self.client.set_property("Scripting Agent.RUN_SCRIPT", script_name)

    def stop_script(self, script_name):
        """Stop a script."""
        self.client.set_property("Scripting Agent.STOP_SCRIPT", script_name)