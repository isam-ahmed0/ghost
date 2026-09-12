"""Rich Presence settings panel for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from utils.config import Config
from gui_qt.widgets.settings.base import SettingsCard, make_line_edit


class RichPresencePanel(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.cfg = Config()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = SettingsCard("Rich Presence")

        rpc = self.cfg.get_rich_presence()

        self.details_entry = make_line_edit(text=rpc.details or "")
        card.add_row("Details", self.details_entry)

        self.state_entry = make_line_edit(text=rpc.state or "")
        card.add_row("State", self.state_entry)

        self.large_image_entry = make_line_edit(text=rpc.large_image or "")
        card.add_row("Large Image URL", self.large_image_entry)

        self.large_text_entry = make_line_edit(text=rpc.large_text or "")
        card.add_row("Large Image Text", self.large_text_entry)

        self.small_image_entry = make_line_edit(text=rpc.small_image or "")
        card.add_row("Small Image URL", self.small_image_entry)

        self.small_text_entry = make_line_edit(text=rpc.small_text or "")
        card.add_row("Small Image Text", self.small_text_entry)

        layout.addWidget(card)
        layout.addStretch()
