"""Onboarding page for Ghost Qt GUI."""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from utils.config import Config
from utils import files


class OnboardingPage(QWidget):
    def __init__(self, run_callback=None, bot_controller=None, parent=None):
        super().__init__(parent)
        self.run_callback = run_callback
        self.bot_controller = bot_controller
        self.cfg = Config()
        self.current_step = "welcome"

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(60, 40, 60, 40)
        self.layout.setSpacing(16)

        self._draw_welcome()

    def _clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _draw_welcome(self):
        self._clear()
        self.current_step = "welcome"

        subtitle = QLabel("Welcome to")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; font-weight: bold; color: #cbcbd2;")
        self.layout.addWidget(subtitle)

        title = QLabel("Ghost")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 64px; font-weight: bold;")
        self.layout.addWidget(title)

        self.layout.addSpacing(40)

        start_btn = QPushButton("Get Started")
        start_btn.setObjectName("primaryBtn")
        start_btn.setFixedHeight(42)
        start_btn.setFixedWidth(200)
        start_btn.clicked.connect(self._draw_token_input)
        self.layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _draw_token_input(self):
        self._clear()
        self.current_step = "token"

        title = QLabel("Let's get started!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        subtitle = QLabel("Ghost runs on your own account. Please enter your Discord token to continue.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(20)

        self.token_entry = QLineEdit()
        self.token_entry.setPlaceholderText("Paste your token here...")
        self.token_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_entry.setMinimumWidth(350)
        self.layout.addWidget(self.token_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(20)

        next_btn = QPushButton("Next")
        next_btn.setObjectName("primaryBtn")
        next_btn.setFixedHeight(42)
        next_btn.setFixedWidth(200)
        next_btn.clicked.connect(self._draw_prefix_input)
        self.layout.addWidget(next_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _draw_prefix_input(self):
        token = self.token_entry.text().strip()
        if not token:
            return

        self.cfg.set("token", token, save=False)
        self.cfg.save()

        self._clear()
        self.current_step = "prefix"

        title = QLabel("Now choose a prefix.")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        subtitle = QLabel("Ghost uses old school bot command prefixes. Set a prefix to execute commands.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(20)

        self.prefix_entry = QLineEdit()
        self.prefix_entry.setPlaceholderText("Enter your desired prefix...")
        self.prefix_entry.setMinimumWidth(350)
        self.layout.addWidget(self.prefix_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(20)

        next_btn = QPushButton("Next")
        next_btn.setObjectName("primaryBtn")
        next_btn.setFixedHeight(42)
        next_btn.setFixedWidth(200)
        next_btn.clicked.connect(self._draw_webhook_setup)
        self.layout.addWidget(next_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _draw_webhook_setup(self):
        prefix = self.prefix_entry.text().strip()
        if not prefix:
            return

        self.cfg.set("prefix", prefix, save=False)
        self.cfg.save()

        self._clear()
        self.current_step = "webhooks"

        title = QLabel("Setup webhooks?")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        subtitle = QLabel("Do you want Ghost to create a fresh Discord server for sniper webhooks and rich embeds?")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(20)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        yes_btn = QPushButton("Yes")
        yes_btn.setObjectName("successBtn")
        yes_btn.setFixedHeight(42)
        yes_btn.setFixedWidth(120)
        yes_btn.clicked.connect(lambda: self._finish(True))
        btn_row.addWidget(yes_btn)

        skip_btn = QPushButton("Skip")
        skip_btn.setObjectName("dangerBtn")
        skip_btn.setFixedHeight(42)
        skip_btn.setFixedWidth(120)
        skip_btn.clicked.connect(lambda: self._finish(False))
        btn_row.addWidget(skip_btn)

        self.layout.addLayout(btn_row)

    def _finish(self, setup_webhooks):
        if setup_webhooks:
            webhook_path = files.get_application_support() + "/data/cache/CREATE_WEBHOOKS"
            os.makedirs(os.path.dirname(webhook_path), exist_ok=True)
            with open(webhook_path, "w") as f:
                f.write("True")

        self.cfg.save()

        if self.run_callback:
            self.run_callback(preserve_position=True)
