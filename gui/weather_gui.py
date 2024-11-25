import requests
import json
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt

class WeatherMonitor:
    def __init__(self, api_key, latitude, longitude, output_callback=None):
        """Initialize the WeatherMonitor."""
        self.weather_api_url = 'http://api.openweathermap.org/data/2.5/weather'
        self.weather_api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.output_callback = output_callback

    def log(self, message):
        """Log output through the callback."""
        if self.output_callback:
            self.output_callback(message)

    def check_weather(self):
        """Fetch current weather data."""
        try:
            response = requests.get(
                self.weather_api_url,
                params={
                    'lat': self.latitude,
                    'lon': self.longitude,
                    'appid': self.weather_api_key,
                    'units': 'metric'
                }
            )
            response.raise_for_status()
            data = response.json()

            weather_conditions = [condition['main'].lower() for condition in data['weather']]
            temperature = data['main']['temp']
            rain_chance = data.get('rain', {}).get('1h', 0)
            sky_conditions = 'clear' if 'clear' in weather_conditions else 'not clear'

            return {
                'temperature': temperature,
                'rain_chance': rain_chance,
                'sky_conditions': sky_conditions,
                'last_checked': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except requests.RequestException as e:
            self.log(f"Error fetching weather data: {str(e)}")
            return None


class WeatherWidget(QWidget):
    def __init__(self, api_key, latitude, longitude):
        super().__init__()
        self.setWindowTitle("Weather Monitor")
        self.setMinimumSize(300, 200)

        # WeatherMonitor instance
        self.weather_monitor = WeatherMonitor(api_key, latitude, longitude, self.log_message)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Weather data labels
        self.temperature_label = QLabel("Temperature: -- °C")
        self.rain_label = QLabel("Rain Chance: -- %")
        self.sky_label = QLabel("Sky Conditions: --")
        self.last_checked_label = QLabel("Last Checked: --")

        self.layout.addWidget(self.temperature_label)
        self.layout.addWidget(self.rain_label)
        self.layout.addWidget(self.sky_label)
        self.layout.addWidget(self.last_checked_label)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh Weather")
        self.refresh_button.clicked.connect(self.update_weather)
        self.layout.addWidget(self.refresh_button)

        # Auto-refresh timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(900000)  # 15 minutes in milliseconds

        # Fetch initial weather data
        self.update_weather()

    def update_weather(self):
        """Update the weather data."""
        weather_data = self.weather_monitor.check_weather()
        if weather_data:
            self.temperature_label.setText(f"Temperature: {weather_data['temperature']} °C")
            self.rain_label.setText(f"Rain Chance: {weather_data['rain_chance']} mm")
            self.sky_label.setText(f"Sky Conditions: {weather_data['sky_conditions']}")
            self.last_checked_label.setText(f"Last Checked: {weather_data['last_checked']}")

    def log_message(self, message):
        """Log weather messages (for debugging or logging)."""
        print(message)