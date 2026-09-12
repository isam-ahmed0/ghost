"""Ghost Qt GUI — main window with sidebar navigation and stacked pages."""
import os
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QStatusBar, QLabel
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

from gui_qt.theme import apply_theme, set_theme
from gui_qt.images import Images
from gui_qt.widgets.sidebar import Sidebar
from gui_qt.widgets.titlebar import Titlebar
from gui_qt.pages.home import HomePage
from gui_qt.pages.settings import SettingsPage
from gui_qt.pages.scripts import ScriptsPage
from gui_qt.pages.onboarding import OnboardingPage
from gui_qt.pages.update import UpdatePage
from gui_qt.pages.tools.tools import ToolsPage
from utils.config import Config, VERSION


_ICON_PATH = Path(__file__).parent.parent / "data" / "icon.ico"


class GhostQtApp:
    """Main Ghost Qt application — Steam-style sidebar layout."""

    def __init__(self, bot_controller=None, update_info=None):
        self.bot_controller = bot_controller
        self.update_info = update_info
        self.cfg = Config()

        self.app = QApplication.instance() or QApplication(sys.argv)
        apply_theme(self.app)
        self.images = Images()

        if _ICON_PATH.exists():
            self.app.setWindowIcon(QIcon(str(_ICON_PATH)))

        self._build_ui()
        self._setup_signals()

    def _build_ui(self):
        self.window = QMainWindow()
        self.window.setWindowTitle(f"Ghost v{VERSION}")
        self.window.setMinimumSize(600, 530)
        self.window.resize(750, 530)

        if _ICON_PATH.exists():
            self.window.setWindowIcon(QIcon(str(_ICON_PATH)))

        central = QWidget()
        self.window.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.add_button("home", "home", "Home")
        self.sidebar.add_button("settings", "settings", "Settings")
        self.sidebar.add_button("scripts", "scripts", "Scripts")
        self.sidebar.add_button("tools", "tools", "Tools")
        self.sidebar.add_stretch()
        self.sidebar.add_button("logout", "logout", "Quit")
        main_layout.addWidget(self.sidebar)

        # Pages
        self.pages = QStackedWidget()

        self.home_page = HomePage(bot_controller=self.bot_controller)
        self.settings_page = SettingsPage(bot_controller=self.bot_controller)
        self.scripts_page = ScriptsPage(bot_controller=self.bot_controller)
        self.tools_page = ToolsPage(bot_controller=self.bot_controller, images=self.images)
        self.onboarding_page = OnboardingPage(bot_controller=self.bot_controller)
        self.update_page = UpdatePage(update_info=self.update_info)

        self.pages.addWidget(self.home_page)      # 0
        self.pages.addWidget(self.settings_page)  # 1
        self.pages.addWidget(self.scripts_page)   # 2
        self.pages.addWidget(self.tools_page)     # 3
        self.pages.addWidget(self.onboarding_page) # 4
        self.pages.addWidget(self.update_page)    # 5

        self.page_map = {
            "home": 0,
            "settings": 1,
            "scripts": 2,
            "tools": 3,
            "onboarding": 4,
            "update": 5,
        }

        main_layout.addWidget(self.pages)

        # Status bar
        self.status_bar = QStatusBar()
        self.window.setStatusBar(self.status_bar)

        self.status_icon = QLabel("●")
        self.status_icon.setObjectName("statusDot")
        self.status_text = QLabel("Starting...")
        self.status_text.setObjectName("statusText")
        self.status_bar.addWidget(self.status_icon)
        self.status_bar.addWidget(self.status_text)

        footer = QLabel(f"Ghost v{VERSION}")
        footer.setObjectName("footerText")
        self.status_bar.addPermanentWidget(footer)

    def _setup_signals(self):
        self.sidebar.page_changed.connect(self._switch_page)

        # Logout button
        if "logout" in self.sidebar.buttons:
            self.sidebar.buttons["logout"].clicked.connect(self._quit)

    def _switch_page(self, page_name):
        if page_name in self.page_map:
            index = self.page_map[page_name]
            self.pages.setCurrentIndex(index)

    def _set_status(self, text, color=None):
        self.status_text.setText(text)
        if color:
            import gui_qt.theme as theme
            color_map = {
                "success": theme.SUCCESS,
                "info": theme.INFO,
                "danger": theme.DANGER,
                "warning": theme.WARNING,
            }
            c = color_map.get(color, theme.TEXT_SECONDARY)
            self.status_icon.setStyleSheet(f"color: {c};")

    def draw_home(self):
        self.sidebar.set_current_page("home")
        self.pages.setCurrentIndex(self.page_map["home"])

    def draw_onboarding(self):
        self.sidebar.set_current_page("onboarding")
        self.pages.setCurrentIndex(self.page_map["onboarding"])

    def draw_update(self):
        self.sidebar.set_current_page("update")
        self.pages.setCurrentIndex(self.page_map["update"])

    def draw_settings(self):
        self.sidebar.set_current_page("settings")
        self.pages.setCurrentIndex(self.page_map["settings"])

    def draw_scripts(self):
        self.sidebar.set_current_page("scripts")
        self.pages.setCurrentIndex(self.page_map["scripts"])

    def draw_tools(self):
        self.sidebar.set_current_page("tools")
        self.pages.setCurrentIndex(self.page_map["tools"])

    def _on_bot_ready(self):
        self._set_status("Connected", "success")
        self.draw_home()

    def _check_bot_started(self):
        if self.bot_controller and self.bot_controller.bot_running:
            self._on_bot_ready()
        else:
            QTimer.singleShot(500, self._check_bot_started)

    def _quit(self):
        self.window.close()

    def run(self):
        if self.update_info and self.update_info.has_update:
            self.draw_update()
        else:
            try:
                token = self.cfg.get("token")
            except (KeyError, Exception):
                token = ""
            if not token:
                self.draw_onboarding()
            else:
                if self.bot_controller and not self.bot_controller.running:
                    self.bot_controller.start()
                self._set_status("Connecting...", "info")
                self._check_bot_started()

        self.window.show()
        sys.exit(self.app.exec())


def run_qt_gui(bot_controller=None, update_info=None):
    """Entry point for the Qt GUI."""
    gui = GhostQtApp(bot_controller=bot_controller, update_info=update_info)
    gui.run()
