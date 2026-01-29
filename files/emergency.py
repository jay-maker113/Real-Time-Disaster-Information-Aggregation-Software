from email.mime.text import MIMEText
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QTextEdit,QComboBox
import smtplib
import json

from files.constants import filename

class EmergencyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_emergency_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)


        self.country_selector = QComboBox()
        self.country_selector.addItem("Select Country")
        self.country_selector.currentIndexChanged.connect(self.update_contacts)
        layout.addWidget(self.country_selector)


        self.contacts = QTextEdit()
        self.contacts.setReadOnly(True)
        layout.addWidget(self.contacts)



    def load_emergency_data(self):

        with open(f'{filename}\\emergency_contacts.json', 'r') as file:
            self.emergency_data = json.load(file)


        for entry in self.emergency_data:
            country_name = entry["Country"]["Name"]
            self.country_selector.addItem(country_name)

    def update_contacts(self):
        country_index = self.country_selector.currentIndex()
        if country_index == 0: 
            self.contacts.setHtml("<h2>Please select a country to see emergency contacts.</h2>")
            return


        selected_country = self.emergency_data[country_index - 1]  
        contacts_html = self.get_emergency_contacts(selected_country)
        self.contacts.setHtml(contacts_html)

    def get_emergency_contacts(self, country_data):
        country_name = country_data["Country"]["Name"]
        

        ambulance_numbers = ", ".join(filter(None, country_data["Ambulance"]["All"])) if country_data["Ambulance"]["All"] else "N/A"
        fire_numbers = ", ".join(filter(None, country_data["Fire"]["All"])) if country_data["Fire"]["All"] else "N/A"
        police_numbers = ", ".join(filter(None, country_data["Police"]["All"])) if country_data["Police"]["All"] else "N/A"

        return f"""
            <h2>Emergency Contacts for {country_name}</h2>
            <ul>
                <li>🚑 Ambulance: {ambulance_numbers}</li>
                <li>🚒 Fire Department: {fire_numbers}</li>
                <li>👮 Police: {police_numbers}</li>
            </ul>
        """
