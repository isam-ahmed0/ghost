"""Session Spoofing settings panel for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel
from gui_qt.widgets.settings.base import SettingsCard, cfg_get


class SessionSpoofingPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = SettingsCard("Session Spoofing")

        spoofing = cfg_get("session_spoofing", {})
        self.enabled_cb = card.add_checkbox(
            "Enable session spoofing",
            checked=spoofing.get("enabled", False) if isinstance(spoofing, dict) else False,
        )

        layout.addWidget(card)
        layout.addStretch()
