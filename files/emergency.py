import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QComboBox, QLabel
from files.constants import ASSETS_DIR


class EmergencyPage(QWidget):
    """
    Displays emergency contacts for countries.
    Loads data from emergency_contacts.json and shows
    Ambulance, Fire, and Police numbers.
    """

    def __init__(self):
        super().__init__()
        self.emergency_data = []
        self.init_ui()
        self.load_emergency_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        instruction = QLabel("Select a country to view emergency contact numbers:")
        layout.addWidget(instruction)

        self.country_selector = QComboBox()
        self.country_selector.addItem("Select Country")
        self.country_selector.currentIndexChanged.connect(self.update_contacts)
        layout.addWidget(self.country_selector)

        self.contacts = QTextEdit()
        self.contacts.setReadOnly(True)
        layout.addWidget(self.contacts)

    def load_emergency_data(self):
        """
        Loads emergency_contacts.json safely.
        If missing or invalid, shows a message.
        """
        try:
            json_path = os.path.join(ASSETS_DIR, "emergency_contacts.json")
            with open(json_path, "r") as file:
                self.emergency_data = json.load(file)

            for entry in self.emergency_data:
                country_name = entry.get("Country", {}).get("Name", "Unknown")
                self.country_selector.addItem(country_name)

        except FileNotFoundError:
            print(f"[EmergencyPage] emergency_contacts.json not found at {ASSETS_DIR}")
            self.contacts.setHtml("<h2>Emergency contacts file missing.</h2>")
        except Exception as e:
            print(f"[EmergencyPage] Failed to load emergency data: {e}")
            self.contacts.setHtml("<h2>Error loading emergency contacts.</h2>")

    def update_contacts(self):
        """
        Shows emergency numbers for the selected country.
        """
        idx = self.country_selector.currentIndex()
        if idx == 0:
            self.contacts.setHtml("<h2>Please select a country to see emergency contacts.</h2>")
            return

        try:
            country_entry = self.emergency_data[idx - 1]
            html = self.get_emergency_contacts_html(country_entry)
            self.contacts.setHtml(html)
        except Exception as e:
            print(f"[EmergencyPage] Error parsing contact data: {e}")
            self.contacts.setHtml("<h2>Unable to display contacts.</h2>")

    def get_emergency_contacts_html(self, country_data):
        """
        Formats Ambulance, Fire, Police numbers into HTML.
        """
        country_name = country_data.get("Country", {}).get("Name", "Unknown")

        ambulance = country_data.get("Ambulance", {}).get("All", [])
        fire = country_data.get("Fire", {}).get("All", [])
        police = country_data.get("Police", {}).get("All", [])

        ambulance_numbers = ", ".join(filter(None, ambulance)) or "N/A"
        fire_numbers = ", ".join(filter(None, fire)) or "N/A"
        police_numbers = ", ".join(filter(None, police)) or "N/A"

        return f"""
        <h2>Emergency Contacts for {country_name}</h2>
        <ul>
            <li><b>🚑 Ambulance:</b> {ambulance_numbers}</li>
            <li><b>🚒 Fire Dept:</b> {fire_numbers}</li>
            <li><b>👮 Police:</b> {police_numbers}</li>
        </ul>
        """
