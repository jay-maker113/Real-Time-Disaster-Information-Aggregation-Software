from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from files.constants import ASSETS_DIR

class AlertCard(QWidget):
    """
    A clickable card widget to display a brief summary
    of a disaster alert in the dashboard.
    Emits a signal with the full alert dict when clicked.
    """
    clicked = pyqtSignal(dict)

    def __init__(self, alert_data):
        super().__init__()
        self.alert_data = alert_data
        self.init_ui(alert_data)

    def init_ui(self, alert_data):
        image_path = alert_data.get("imagefile", "")
        disaster_name = alert_data.get("title", "")
        location = alert_data.get("location", "")
        time_ago = alert_data.get("time_ago", "")
        severity = alert_data.get("severity", "")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Image
        image_label = QLabel()
        image_label.setFixedSize(200, 200)
        try:
            pixmap = QPixmap(f"{ASSETS_DIR}/{image_path}")
            if not pixmap.isNull():
                pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(pixmap)
        except Exception:
            pass
        image_label.setAlignment(Qt.AlignCenter)

        # Info text
        info_text = f"""
        <b style="font-size: 26px;">{disaster_name}</b><br>
        <i style="font-size: 16px;">Time: {time_ago}</i><br>
        <i style="font-size: 16px;">Location: {location}</i><br>
        <i style="font-size: 14px;">Severity: {severity}</i>
        """

        self.info_label = QLabel(info_text)
        self.info_label.setWordWrap(True)

        # Try loading custom font, fallback if not found
        try:
            font_id = QFontDatabase.addApplicationFont(f"{ASSETS_DIR}/Comfortaa-Bold.ttf")
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                custom_font = QFont(families[0], 11)
                self.info_label.setFont(custom_font)
        except Exception:
            pass

        self.info_label.setFixedHeight(180)
        self.info_label.setMinimumWidth(600)
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Style
        self.info_label.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 8px;
            padding: 8px;
        """)

        # Add widgets
        layout.addWidget(image_label)
        layout.addWidget(self.info_label)
        layout.addStretch()
        self.setLayout(layout)

        # Set pointer cursor for clickability
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        """
        Emit full alert_data when clicked.
        """
        self.clicked.emit(self.alert_data)
        super().mousePressEvent(event)
