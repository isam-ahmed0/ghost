"""Base settings card widget for Ghost Qt GUI."""
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QHBoxLayout, QComboBox
)
from PySide6.QtCore import Qt

import gui_qt.theme as theme
from utils.config import Config


def cfg_get(key, default=None):
    """Config.get() wrapper that returns *default* if the key is missing."""
    cfg = Config()
    try:
        return cfg.get(key)
    except (KeyError, Exception):
        return default


class SettingsCard(QFrame):
    """Rounded card container for settings sections."""

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("settingsCard")
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(20, 16, 20, 16)
        self._layout.setSpacing(10)

        if title:
            lbl = QLabel(title)
            lbl.setObjectName("sectionTitle")
            self._layout.addWidget(lbl)

    def add_row(self, label_text, widget):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setMinimumWidth(120)
        row.addWidget(lbl)
        row.addWidget(widget)
        self._layout.addLayout(row)
        return widget

    def add_widget(self, widget):
        self._layout.addWidget(widget)

    def add_separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        self._layout.addWidget(sep)

    def add_checkbox(self, label_text, checked=False, on_change=None):
        cb = QCheckBox(label_text)
        cb.setChecked(checked)
        if on_change:
            cb.stateChanged.connect(on_change)
        self._layout.addWidget(cb)
        return cb


def make_line_edit(placeholder="", text="", password=False):
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setText(text)
    if password:
        le.setEchoMode(QLineEdit.EchoMode.Password)
    return le


def make_combo(options, current=""):
    cb = QComboBox()
    cb.addItems(options)
    if current and current in options:
        cb.setCurrentText(current)
    return cb


def make_button(text, object_name="toolBtn", callback=None):
    btn = QPushButton(text)
    btn.setObjectName(object_name)
    btn.setFixedHeight(38)
    if callback:
        btn.clicked.connect(callback)
    return btn
