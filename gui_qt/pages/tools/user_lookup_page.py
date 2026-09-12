"""User Lookup tool page for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt


class UserLookupPage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("User Lookup")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Look up information about a user by their ID.")
        desc.setObjectName("bodyText")
        layout.addWidget(desc)

        self.user_id_entry = QLineEdit()
        self.user_id_entry.setPlaceholderText("Enter user ID...")
        layout.addWidget(self.user_id_entry)

        lookup_btn = QPushButton("Lookup")
        lookup_btn.setObjectName("primaryBtn")
        lookup_btn.setFixedHeight(38)
        layout.addWidget(lookup_btn)

        self.result_label = QLabel("")
        self.result_label.setObjectName("bodyText")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        layout.addStretch()
