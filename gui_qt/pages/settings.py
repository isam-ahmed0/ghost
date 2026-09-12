"""Settings page for Ghost Qt GUI."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt

import gui_qt.theme as theme
from gui_qt.widgets.settings.general import GeneralPanel
from gui_qt.widgets.settings.theming import ThemingPanel
from gui_qt.widgets.settings.rich_presence import RichPresencePanel
from gui_qt.widgets.settings.snipers import SnipersPanel


class SettingsPage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller
        self.current_tab = "general"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        # Title
        title = QLabel("Settings")
        title.setFont(title.font())
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Tab bar
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(8)

        self.tabs = {}
        self.tab_buttons = {}

        tab_names = ["General", "Theming", "Rich Presence", "Snipers"]
        tab_keys = ["general", "theming", "rich_presence", "snipers"]

        for name, key in zip(tab_names, tab_keys):
            btn = QPushButton(name)
            btn.setObjectName("settingsPill")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._switch_tab(k))
            tab_bar.addWidget(btn)
            self.tab_buttons[key] = btn

        tab_bar.addStretch()
        layout.addLayout(tab_bar)

        # Pages
        self.pages = QStackedWidget()

        self.general_panel = GeneralPanel(bot_controller=bot_controller)
        self.theming_panel = ThemingPanel(bot_controller=bot_controller)
        self.rich_presence_panel = RichPresencePanel(bot_controller=bot_controller)
        self.snipers_panel = SnipersPanel()

        self.pages.addWidget(self.general_panel)
        self.pages.addWidget(self.theming_panel)
        self.pages.addWidget(self.rich_presence_panel)
        self.pages.addWidget(self.snipers_panel)

        self.page_map = {
            "general": 0,
            "theming": 1,
            "rich_presence": 2,
            "snipers": 3,
        }

        layout.addWidget(self.pages)

        # Default tab
        self._switch_tab("general")

    def _switch_tab(self, key):
        if key in self.page_map:
            self.pages.setCurrentIndex(self.page_map[key])
            self.current_tab = key

            for tab_key, btn in self.tab_buttons.items():
                btn.setChecked(tab_key == key)
