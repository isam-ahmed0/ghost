"""Password Generator tool page for Ghost Qt GUI."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout
)
from PySide6.QtCore import Qt
import random
import string


class PasswordGenPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        title = QLabel("Password Generator")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        desc = QLabel("Generate strong, random passwords with customizable options.")
        desc.setObjectName("bodyText")
        layout.addWidget(desc)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setFont(type(self.password_display)().font())
        layout.addWidget(self.password_display)

        # Options
        opts = QHBoxLayout()
        self.uppercase_cb = QCheckBox("Uppercase")
        self.uppercase_cb.setChecked(True)
        opts.addWidget(self.uppercase_cb)

        self.numbers_cb = QCheckBox("Numbers")
        self.numbers_cb.setChecked(True)
        opts.addWidget(self.numbers_cb)

        self.symbols_cb = QCheckBox("Symbols")
        self.symbols_cb.setChecked(True)
        opts.addWidget(self.symbols_cb)

        opts.addStretch()
        layout.addLayout(opts)

        gen_btn = QPushButton("Generate")
        gen_btn.setObjectName("primaryBtn")
        gen_btn.setFixedHeight(38)
        gen_btn.clicked.connect(self._generate)
        layout.addWidget(gen_btn)

        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.setObjectName("toolBtn")
        copy_btn.setFixedHeight(38)
        copy_btn.clicked.connect(self._copy)
        layout.addWidget(copy_btn)

        layout.addStretch()

        self._generate()

    def _generate(self):
        chars = string.ascii_lowercase
        if self.uppercase_cb.isChecked():
            chars += string.ascii_uppercase
        if self.numbers_cb.isChecked():
            chars += string.digits
        if self.symbols_cb.isChecked():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        password = "".join(random.choices(chars, k=16))
        self.password_display.setText(password)

    def _copy(self):
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.password_display.text())
