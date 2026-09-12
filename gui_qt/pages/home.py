"""Home page for Ghost Qt GUI."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Qt, QTimer
from gui_qt.widgets.hero_banner import HeroBanner
from gui_qt.widgets.console import Console
from utils.config import VERSION


class HomePage(QWidget):
    def __init__(self, bot_controller=None, parent=None):
        super().__init__(parent)
        self.bot_controller = bot_controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Hero banner
        self.hero = HeroBanner("Ghost", "Discord selfbot toolkit")
        layout.addWidget(self.hero)

        # Account details card
        self.details_frame = QFrame()
        self.details_frame.setObjectName("settingsCard")
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(20, 12, 20, 12)

        self.user_label = QLabel("Loading...")
        self.user_label.setObjectName("heroTitle")
        details_layout.addWidget(self.user_label)

        self.username_label = QLabel("")
        self.username_label.setObjectName("heroSubtitle")
        details_layout.addWidget(self.username_label)

        layout.addWidget(self.details_frame)

        # Status row
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(20, 8, 20, 8)

        self.version_label = QLabel(f"Version: {VERSION}")
        self.version_label.setObjectName("mutedText")
        status_layout.addWidget(self.version_label)

        self.uptime_label = QLabel("Uptime: 0s")
        self.uptime_label.setObjectName("mutedText")
        status_layout.addWidget(self.uptime_label)

        self.latency_label = QLabel("Latency: --ms")
        self.latency_label.setObjectName("mutedText")
        status_layout.addWidget(self.latency_label)

        status_layout.addStretch()
        layout.addWidget(status_widget)

        # Console
        self.console = Console(bot_controller=bot_controller)
        layout.addWidget(self.console)

        # Start update timers
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_details)
        self._update_timer.start(1000)

    def _update_details(self):
        if not self.bot_controller:
            return
        try:
            user = self.bot_controller.get_user()
            if user:
                self.user_label.setText(user.display_name)
                self.username_label.setText(user.name)

            self.uptime_label.setText(f"Uptime: {self.bot_controller.get_uptime()}")
            self.latency_label.setText(f"Latency: {self.bot_controller.get_latency()}")
        except Exception:
            pass
