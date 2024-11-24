class MountAgent:
    def __init__(self, client):
        self.client = client
        self.slew_speed = "0.5x"

    def get_ra_dec(self):
        """Fetch RA and DEC from INDIGO properties."""
        ra = self.client.get_property("Mount Agent.AGENT_MOUNT_DISPLAY_COORDINATES_PROPERTY.RA_JNOW")
        dec = self.client.get_property("Mount Agent.AGENT_MOUNT_DISPLAY_COORDINATES_PROPERTY.DEC_JNOW")
        return ra, dec

    def move(self, direction):
        """Move the mount in a specified direction."""
        directions = {
            "N": "Mount Agent.MOVE.NORTH",
            "S": "Mount Agent.MOVE.SOUTH",
            "E": "Mount Agent.MOVE.EAST",
            "W": "Mount Agent.MOVE.WEST",
        }
        self.client.set_property(directions[direction], True)

    def stop(self):
        """Stop the mount movement."""
        self.client.set_property("Mount Agent.MOVE.STOP", True)

    def set_speed(self, speed):
        """Set the slew speed of the mount."""
        self.slew_speed = speed
        speed_map = {
            "0.1x": 0.1,
            "0.5x": 0.5,
            "1x": 1.0,
            "2x": 2.0,
        }
        self.client.set_property("Mount Agent.SLEW_SPEED", speed_map[speed])

    def set_tracking(self, mode):
        """Set the tracking mode."""
        modes = {
            "Sidereal": "Mount Agent.TRACKING.SIDEREAL",
            "Solar": "Mount Agent.TRACKING.SOLAR",
        }
        self.client.set_property(modes[mode], True)
