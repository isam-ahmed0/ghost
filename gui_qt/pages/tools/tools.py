"""Tools index page for Ghost Qt GUI."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from gui_qt.images import Images
import gui_qt.theme as theme


class ToolCard(QFrame):
    """Clickable card for a tool."""

    def __init__(self, name, description, icon_pixmap, on_click, parent=None):
        super().__init__(parent)
        self.setObjectName("toolCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(70)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(16)

        if icon_pixmap:
            icon_label = QLabel()
            icon_label.setPixmap(icon_pixmap)
            layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        text_layout.addWidget(name_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 11px;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Click entire card
        self.mousePressEvent = lambda e: on_click()


class ToolsPage(QWidget):
    def __init__(self, bot_controller=None, images=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller
        self.images = images or Images()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("Tools")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)

        tools = [
            ("Surveillance", "Search a user's message history across mutual servers", "surveillance", None),
            ("Message Logger", "Logs every deleted message sent in your servers", "message_logger", None),
            ("Auto AFK Reply", "Automatically reply to DMs when you're away", "auto_afk_reply", None),
            ("Backups", "Create and restore backups of your Discord account", "backups", None),
            ("User Lookup", "Look up information about a user by their ID", "user_lookup", None),
            ("Password Generator", "Generate strong, random passwords", "password_gen", None),
        ]

        for name, desc, icon_key, callback in tools:
            card = ToolCard(name, desc, self.images.get_pixmap(icon_key), callback or (lambda: None))
            container_layout.addWidget(card)

        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
