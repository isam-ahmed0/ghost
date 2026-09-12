"""APIs settings panel for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from gui_qt.widgets.settings.base import SettingsCard, make_line_edit, cfg_get


class APIsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = SettingsCard("APIs")

        self.openai_key = make_line_edit(
            text=cfg_get("api_keys.openai", ""),
            password=True,
        )
        card.add_row("OpenAI API Key", self.openai_key)

        layout.addWidget(card)
        layout.addStretch()
