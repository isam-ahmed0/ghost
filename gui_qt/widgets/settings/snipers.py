"""Snipers settings panel for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from gui_qt.widgets.settings.base import SettingsCard, cfg_get


class SnipersPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = SettingsCard("Snipers")

        snipers = cfg_get("snipers", {})
        self.checkboxes = {}

        sniper_types = [
            ("nitro", "Nitro Sniper"),
            ("giveaway", "Giveaway Sniper"),
            ("drop", "Drop Sniper"),
        ]

        for key, label in sniper_types:
            sniper_cfg = snipers.get(key, {}) if isinstance(snipers, dict) else {}
            enabled = sniper_cfg.get("enabled", False) if isinstance(sniper_cfg, dict) else False
            cb = card.add_checkbox(label, checked=bool(enabled))
            self.checkboxes[key] = cb

        layout.addWidget(card)
        layout.addStretch()
