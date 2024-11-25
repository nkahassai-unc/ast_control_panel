class ScriptingAgent:
    def __init__(self, client):
        self.client = client

    def list_scripts(self):
        """Fetch the list of available scripts."""
        try:
            scripts = []
            index = 0
            while True:
                # Dynamically fetch script details
                script_name = self.client.get_property(f"Scripting Agent.AGENT_SCRIPTING_SCRIPT_{index}.NAME")
                if not script_name:
                    break
                scripts.append(script_name)
                index += 1
            return scripts
        except Exception as e:
            print(f"Error fetching scripts: {e}")
            return []

    def run_script(self, script_name):
        """Run a script by name."""
        try:
            # Set the script name to be run
            self.client.set_property("Scripting Agent.AGENT_SCRIPTING_RUN_SCRIPT.SCRIPT", script_name)
            # Execute the script
            self.client.set_property("Scripting Agent.AGENT_SCRIPTING_EXECUTE_SCRIPT.AGENT_SCRIPTING_SCRIPT_0", True)
            print(f"Script '{script_name}' started.")
        except Exception as e:
            print(f"Error running script '{script_name}': {e}")

    def stop_script(self, script_name):
        """Stop a script by name."""
        try:
            # INDIGO scripting does not have a direct stop call; this is a placeholder.
            print(f"Stopping script '{script_name}' is not supported directly by the API.")
        except Exception as e:
            print(f"Error stopping script '{script_name}': {e}")