"""Console widget for Ghost Qt GUI — log display with color-coded prefixes."""
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCharFormat, QFont

import gui_qt.theme as theme
from gui_qt.images import Images
from utils.console import get_formatted_time


# Prefix colors matching ghost's tkinter console
PREFIX_COLORS = {
    "sniper": "#ff4d4d",
    "command": "#0b91ff",
    "info": "#2aefef",
    "success": "#4fee4c",
    "warning": "#eceb18",
    "error": "#ff4d4d",
    "cli": "#ffb6c1",
    "rpc": "#ffb6c1",
    "captcha": "#eceb18",
    "nitro": "#0b91ff",
}


class Console(QWidget):
    """Log console with color-coded prefix output."""

    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller
        self.images = Images()
        self.logs = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("JetBrainsMono Nerd Font", 12))
        layout.addWidget(self.text_edit)

        self._load_default_tags()

    def _load_default_tags(self):
        """Set up default text formats for log prefixes."""
        self._formats = {}
        for prefix, color in PREFIX_COLORS.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            fmt.setFont(QFont("JetBrainsMono Nerd Font", 12, QFont.Weight.Bold))
            self._formats[prefix] = fmt

        self._timestamp_fmt = QTextCharFormat()
        self._timestamp_fmt.setForeground(QColor(theme.TEXT_MUTED))
        self._timestamp_fmt.setFont(QFont("JetBrainsMono Nerd Font", 12, QFont.Weight.Bold))

        self._text_fmt = QTextCharFormat()
        self._text_fmt.setForeground(QColor(theme.TEXT_SECONDARY))
        self._text_fmt.setFont(QFont("JetBrainsMono Nerd Font", 12, QFont.Weight.Bold))

        self._sniper_key_fmt = QTextCharFormat()
        self._sniper_key_fmt.setForeground(QColor("#eceb18"))
        self._sniper_key_fmt.setFont(QFont("JetBrainsMono Nerd Font", 12, QFont.Weight.Bold))

    def add_log(self, prefix, text):
        time = get_formatted_time()
        self.logs.append((time, prefix, text))
        self._render_log(time, prefix, text)

    def add_sniper(self, sniper_obj):
        self.add_log("sniper", sniper_obj)

    def _render_log(self, time, prefix, text):
        cursor = self.text_edit.textCursor()

        # Timestamp
        cursor.setCharFormat(self._timestamp_fmt)
        cursor.insertText(f"[{time}] ")

        # Prefix
        fmt = self._formats.get(prefix.lower(), self._text_fmt)
        cursor.setCharFormat(fmt)
        cursor.insertText(f"[{prefix}] ")

        # Content
        if prefix.lower() == "sniper" and isinstance(text, dict):
            cursor.setCharFormat(self._text_fmt)
            cursor.insertText(f"{text.get('title', '')}\n")
            desc = text.get("description", {})
            for key, value in desc.items():
                cursor.setCharFormat(self._timestamp_fmt)
                padding = " " * len(f"[{time}] ")
                cursor.insertText(f"{padding}")
                cursor.setCharFormat(self._sniper_key_fmt)
                cursor.insertText(f"{key}: ")
                cursor.setCharFormat(self._text_fmt)
                cursor.insertText(f"{value}\n")
            cursor.insertText("\n")
        else:
            cursor.setCharFormat(self._text_fmt)
            cursor.insertText(f"{text}\n")

        self.text_edit.setTextCursor(cursor)
        self.text_edit.verticalScrollBar().setValue(
            self.text_edit.verticalScrollBar().maximum()
        )

    def clear(self):
        self.logs.clear()
        self.text_edit.clear()

    def update(self):
        """Re-render all logs."""
        self.text_edit.clear()
        for time, prefix, text in self.logs:
            self._render_log(time, prefix, text)
