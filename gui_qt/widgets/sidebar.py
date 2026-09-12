"""Sidebar widget for Ghost Qt GUI — icon-based navigation with hover glow."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap

from gui_qt.images import Images
from gui_qt.widgets.sidebar_button import SidebarButton


class Sidebar(QWidget):
    """Left sidebar with icon buttons for page navigation."""
    page_changed = Signal(str)

    WIDTH = 65

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(self.WIDTH)
        self.images = Images()
        self.buttons = {}
        self.current_page = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 15, 0, 15)
        layout.setSpacing(4)

        self._layout = layout

    def add_button(self, page_name, icon_key, tooltip=""):
        btn = SidebarButton(self.images.get_icon(icon_key), tooltip, self)
        btn.clicked.connect(lambda: self._on_click(page_name))
        self.buttons[page_name] = btn
        self._layout.addWidget(btn)
        return btn

    def add_stretch(self):
        self._layout.addStretch()

    def set_current_page(self, page_name):
        self.current_page = page_name
        for name, btn in self.buttons.items():
            btn.setChecked(name == page_name)

    def _on_click(self, page_name):
        if page_name == self.current_page:
            return
        self.set_current_page(page_name)
        self.page_changed.emit(page_name)

    def disable_non_essential(self):
        """Disable buttons except home/console during startup."""
        for name, btn in self.buttons.items():
            if name not in ("home", "console"):
                btn.setEnabled(False)

    def enable_all(self):
        for btn in self.buttons.values():
            btn.setEnabled(True)
