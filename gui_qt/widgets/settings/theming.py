"""Theming settings panel for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from utils.config import Config
import gui_qt.theme as theme
from gui_qt.widgets.settings.base import SettingsCard, make_line_edit


class ThemingPanel(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.cfg = Config()
        self.bot_controller = bot_controller
        self.theme_entries = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Theme selector card
        card = SettingsCard("Theme Editor")

        current_theme = self.cfg.theme
        theme_dict = current_theme.to_dict() if hasattr(current_theme, 'to_dict') else {}

        for key, value in theme_dict.items():
            entry = make_line_edit(text=str(value))
            card.add_row(key.capitalize(), entry)
            self.theme_entries[key] = entry

        card.add_separator()

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setObjectName("successBtn")
        save_btn.setFixedHeight(38)
        save_btn.clicked.connect(self._save_theme)
        btn_row.addWidget(save_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.setFixedHeight(38)
        delete_btn.clicked.connect(self._delete_theme)
        btn_row.addWidget(delete_btn)

        btn_row.addStretch()
        btn_container = QWidget()
        btn_container.setLayout(btn_row)
        card.add_widget(btn_container)

        layout.addWidget(card)
        layout.addStretch()

    def _save_theme(self):
        for key, entry in self.theme_entries.items():
            self.cfg.theme.set(key, entry.text())
        self.cfg.theme.save(notify=False)
        self.cfg.save(notify=False)

    def _delete_theme(self):
        if self.cfg.theme.name.lower() == "ghost":
            return
        self.cfg.delete_theme(self.cfg.theme.name)
