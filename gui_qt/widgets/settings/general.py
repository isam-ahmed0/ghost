"""General settings panel for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox
from PySide6.QtCore import Qt
from gui_qt.widgets.settings.base import SettingsCard, make_line_edit, make_combo, cfg_get


class GeneralPanel(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # General settings card
        card = SettingsCard("General")

        self.token_entry = make_line_edit(
            placeholder="Paste your token here...",
            text=cfg_get("token", ""),
            password=True,
        )
        card.add_row("Token", self.token_entry)

        self.prefix_entry = make_line_edit(
            placeholder="!",
            text=cfg_get("prefix", "!"),
        )
        card.add_row("Prefix", self.prefix_entry)

        self.delay_entry = make_line_edit(
            placeholder="0",
            text=str(cfg_get("message_settings.auto_delete_delay", 0)),
        )
        card.add_row("Auto delete delay", self.delay_entry)

        style_options = ["codeblock", "image", "embed"]
        current_style = cfg_get("message_settings.style", "codeblock")
        self.style_combo = make_combo(style_options, current_style)
        card.add_row("Message style", self.style_combo)

        card.add_separator()

        theme_options = [
            "dark", "red", "green", "blue", "yellow",
            "orange", "pink", "purple", "light",
        ]
        current_theme = cfg_get("gui_theme", "dark")
        self.theme_combo = make_combo(theme_options, current_theme)
        card.add_row("GUI Theme", self.theme_combo)

        card.add_separator()

        self.edit_og_cb = card.add_checkbox(
            "Edit original message",
            checked=cfg_get("message_settings.edit_og", False),
        )

        self.startup_cb = card.add_checkbox(
            "Launch Ghost on startup",
            checked=cfg_get("launch_on_startup", False),
        )

        self.telemetry_cb = card.add_checkbox(
            "Send anonymous telemetry data",
            checked=cfg_get("telemetry", True),
        )

        layout.addWidget(card)
        layout.addStretch()
