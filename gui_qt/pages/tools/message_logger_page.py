"""Message Logger tool page for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt


class MessageLoggerPage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("Message Logger")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Logs every deleted message sent in your servers.")
        desc.setObjectName("bodyText")
        layout.addWidget(desc)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        btn_row = QVBoxLayout()
        clear_btn = QPushButton("Clear Log")
        clear_btn.setObjectName("dangerBtn")
        clear_btn.setFixedHeight(38)
        clear_btn.clicked.connect(lambda: self.log_display.clear())
        btn_row.addWidget(clear_btn)
        layout.addLayout(btn_row)

        layout.addStretch()
