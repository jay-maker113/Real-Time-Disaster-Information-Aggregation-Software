from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QMessageBox
from PyQt5.QtCore import QTimer
from files.gdacs_alerts import fetch_gdacs_alerts
from files.Alertdetails import AlertCard

class DashboardPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.old_alert_ids = set()
        self.init_ui()
        self.load_data()

        # --- AUTO REFRESH ---
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.check_for_updates)
        self.refresh_timer.start(5 * 60 * 1000)  # 5 min interval

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        active_alerts_label = QLabel("🚨 Active Disaster Alerts")
        active_alerts_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(active_alerts_label)

        self.active_alerts_scroll = QScrollArea()
        self.active_alerts_content = QWidget()
        self.active_alerts_layout = QVBoxLayout(self.active_alerts_content)
        self.active_alerts_scroll.setWidget(self.active_alerts_content)
        self.active_alerts_scroll.setWidgetResizable(True)
        layout.addWidget(self.active_alerts_scroll)

    def check_for_updates(self):
        """
        Called by timer to auto-refresh alerts.
        """
        new_alerts = fetch_gdacs_alerts()
        new_ids = {a["id"] for a in new_alerts}

        # If there are alerts we didn't have before
        if new_ids.difference(self.old_alert_ids):
            self.old_alert_ids = new_ids
            self.load_data()
            self.show_notification("New disaster alerts available!")

    def show_notification(self, msg_text):
        """
        Show a simple pop-up informing the user of new alerts.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(msg_text)
        msg.setWindowTitle("Disaster Alerts Update")
        msg.exec_()

    def load_data(self):
        """
        Fetch alerts and display AlertCard widgets.
        """
        try:
            alerts = fetch_gdacs_alerts()
        except Exception as e:
            print(f"[Dashboard] Failed to fetch alerts: {e}")
            alerts = []

        self.old_alert_ids = {a["id"] for a in alerts}

        # Clear old alert widgets
        while self.active_alerts_layout.count():
            widget = self.active_alerts_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # If no alerts, show a message
        if not alerts:
            no_alerts = QLabel("No active alerts at the moment.")
            no_alerts.setStyleSheet("font-size: 18px;")
            self.active_alerts_layout.addWidget(no_alerts)
            return

        # Add each alert card
        for alert in alerts:
            try:
                card = AlertCard(alert)
                card.clicked.connect(lambda _, a=alert: self.show_alert_details(a))
                self.active_alerts_layout.addWidget(card)
            except Exception as e:
                print(f"[Dashboard] Failed to add card: {e}")

        self.active_alerts_layout.addStretch()

    def show_alert_details(self, alert):
        self.parent.alert_details_page.set_alert_details(alert)
        self.parent.stacked_widget.setCurrentWidget(self.parent.alert_details_page)
