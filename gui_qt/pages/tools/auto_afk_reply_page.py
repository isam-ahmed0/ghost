"""Auto AFK Reply tool page for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PySide6.QtCore import Qt


class AutoAFKReplyPage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("Auto AFK Reply")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Automatically reply to DMs when you're away from the keyboard.")
        desc.setObjectName("bodyText")
        layout.addWidget(desc)

        self.enable_cb = QCheckBox("Enable Auto AFK Reply")
        layout.addWidget(self.enable_cb)

        self.reply_message = QLineEdit()
        self.reply_message.setPlaceholderText("Reply message...")
        layout.addWidget(self.reply_message)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedHeight(38)
        layout.addWidget(save_btn)

        layout.addStretch()
