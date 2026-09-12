"""Backups tool page for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class BackupsPage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("Backups")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Create and restore backups of your Discord account, friends, and servers.")
        desc.setObjectName("bodyText")
        layout.addWidget(desc)

        create_btn = QPushButton("Create Backup")
        create_btn.setObjectName("successBtn")
        create_btn.setFixedHeight(38)
        layout.addWidget(create_btn)

        restore_btn = QPushButton("Restore Backup")
        restore_btn.setObjectName("primaryBtn")
        restore_btn.setFixedHeight(38)
        layout.addWidget(restore_btn)

        layout.addStretch()
