from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, ICRS, get_sun
import astropy.units as u

class CalculationsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculations Module")
        self.setMinimumSize(200, 200)

        # Observer's location (e.g., Chapel Hill, NC)
        self.location = EarthLocation(lat=35.9132 * u.deg, lon=-79.0558 * u.deg, height=80 * u.m)

        # Layout
        layout = QVBoxLayout()
        self.setMinimumSize(300, 100)


        # Labels for displaying data
        self.lst_label = QLabel("Local Sidereal Time: --")
        self.sun_ra_dec_label = QLabel("Sun RA/DEC: -- / --")
        self.sun_alt_az_label = QLabel("Sun Alt/Az: -- / --")

        # Add labels to layout
        layout.addWidget(self.lst_label)
        layout.addWidget(self.sun_ra_dec_label)
        layout.addWidget(self.sun_alt_az_label)

        # Refresh button
        refresh_button = QPushButton("Refresh Calculations")
        refresh_button.clicked.connect(self.update_calculations)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.update_calculations()  # Initial update

    def update_calculations(self):
        """Update all calculated values and display them."""
        now = Time.now()
        altaz_frame = AltAz(obstime=now, location=self.location)

        # Calculate Local Sidereal Time (LST)
        lst = now.sidereal_time('apparent', longitude=self.location.lon)
        self.lst_label.setText(f"Local Sidereal Time: {lst.to_string(unit='hourangle', sep=':')}")

        # Calculate Sun's position
        sun_gcrs = get_sun(now)
        sun_altaz = sun_gcrs.transform_to(altaz_frame)
        sun_equatorial = sun_altaz.transform_to(ICRS)

        # Display Sun's RA/DEC
        sun_ra = sun_equatorial.ra.to_string(unit='hourangle', sep=':')
        sun_dec = sun_equatorial.dec.to_string(unit='degree', sep=':')
        self.sun_ra_dec_label.setText(f"Sun RA/DEC: {sun_ra} / {sun_dec}")

        # Display Sun's Alt/Az
        sun_alt = sun_altaz.alt.to_string(unit='degree', sep=':')
        sun_az = sun_altaz.az.to_string(unit='degree', sep=':')
        self.sun_alt_az_label.setText(f"Sun Alt/Az: {sun_alt} / {sun_az}")