# Description: INDIGO client implementation in Python.

import socket
import json

class INDIGOClient:
    def __init__(self, host="localhost", port=7624):
        """Initialize INDIGO client with host and port."""
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """Establish connection to the INDIGO server."""
        try:
            self.connection = socket.create_connection((self.host, self.port))
            print(f"Connected to INDIGO server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to INDIGO server: {e}")
            self.connection = None

    def disconnect(self):
        """Close the connection to the INDIGO server."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_property(self, property_name):
        """Fetch the value of a property with error handling."""
        try:
            if not self.connection:
                raise ConnectionError("Client is not connected to the INDIGO server.")
            
            # Prepare the request
            request = {"action": "get", "property": property_name}
            self._send_request(request)
            
            # Get the response
            response = self._receive_response()
            return response.get("value")
        
        except ConnectionError as ce:
            print(f"Connection Error: {ce}")
            return None  # Return a default value (e.g., None or a mock value)
        
        except Exception as e:
            print(f"Error fetching property '{property_name}': {e}")
            return None
        
    def set_property(self, property_name, value):
        """Set the value of a property."""
        request = {"action": "set", "property": property_name, "value": value}
        self._send_request(request)

    def _send_request(self, request):
        """Send a request to the INDIGO server."""
        self.connection.sendall((json.dumps(request) + "\n").encode("utf-8"))

    def _receive_response(self):
        """Receive and parse a response from the INDIGO server."""
        response = self.connection.recv(4096).decode("utf-8")
        return json.loads(response)
