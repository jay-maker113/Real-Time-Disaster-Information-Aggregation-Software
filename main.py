import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QSizePolicy
)

from files.Dashboard import DashboardPage
from files.emergency import EmergencyPage
from files.Mappage import MapPage
from files.Alertpage import AlertDetailsPage
from files.constants import DISASTERBOXES, ASSETS_DIR

# Ensure assets directory exists
if not os.path.isdir(ASSETS_DIR):
    print(f"[main.py] Warning: ASSETS_DIR not found -> {ASSETS_DIR}")



class MainAPP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Disaster Information System")
        self.setGeometry(50, 50, 1280, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_sidebar()
        self.create_main_content()
        self.update_stylesheet()

        # Start with dashboard view
        self.show_dashboard()

    def create_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)

        buttons = [
            ("🗺 Map", self.show_map),
            ("🌐 Dashboard", self.show_dashboard),
            ("🚨 Emergency", self.show_emergency),
        ]

        for text, handler in buttons:
            btn = AccessibleButton(text)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

    def create_main_content(self):
        self.stacked_widget = QStackedWidget()

        # Initialize pages
        self.map_page = MapPage(DISASTERBOXES)
        self.dashboard_page = DashboardPage(self)
        self.emergency_page = EmergencyPage()
        self.alert_details_page = AlertDetailsPage(self)

        # Add pages to stack
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.map_page)
        self.stacked_widget.addWidget(self.emergency_page)
        self.stacked_widget.addWidget(self.alert_details_page)

        self.main_layout.addWidget(self.stacked_widget, 1)

    def update_stylesheet(self):
        """
        Base styling for UI elements.
        """
        style = """
            QWidget {
                background-color: #f0f4f8;
                color: #2d3748;
            }
            QPushButton {
                background-color: #ffffff;
                color: #2d3748;
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ebf8ff;
            }
            QTextEdit, QLineEdit, QTextBrowser {
                background-color: #ffffff;
                border: 1px solid #cbd5e0;
                border-radius: 6px;
                padding: 8px;
            }
        """
        self.setStyleSheet(style)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

    def show_map(self):
        # Refresh map page so any new shapes are shown
        self.map_page.load_map()
        self.stacked_widget.setCurrentWidget(self.map_page)

    def show_emergency(self):
        self.stacked_widget.setCurrentWidget(self.emergency_page)


class AccessibleButton(QPushButton):
    """
    A sidebar button with consistent styling & pointer cursor.
    """
    def __init__(self, text):
        super().__init__(text)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 16px;
                border-radius: 8px;
            }
        """)


# -------------------
# App Entry
# -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainAPP()
    window.show()
    sys.exit(app.exec_())
