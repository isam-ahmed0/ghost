"""Surveillance tool page for Ghost Qt GUI."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt


class SurveillancePage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("Surveillance")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Search a user's message history across mutual servers.")
        desc.setObjectName("bodyText")
        layout.addWidget(desc)

        self.user_id_entry = QLineEdit()
        self.user_id_entry.setPlaceholderText("Enter user ID...")
        layout.addWidget(self.user_id_entry)

        self.query_entry = QLineEdit()
        self.query_entry.setPlaceholderText("Search query...")
        layout.addWidget(self.query_entry)

        search_btn = QPushButton("Search")
        search_btn.setObjectName("primaryBtn")
        search_btn.setFixedHeight(38)
        layout.addWidget(search_btn)

        self.results_label = QLabel("")
        self.results_label.setObjectName("bodyText")
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)

        layout.addStretch()
