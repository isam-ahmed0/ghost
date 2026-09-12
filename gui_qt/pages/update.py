"""Update page for Ghost Qt GUI."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class UpdatePage(QWidget):
    def __init__(self, update_info=None, parent=None):
        super().__init__(parent)
        self.update_info = update_info

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Update Available")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        if update_info:
            desc = QLabel(f"A new version of Ghost is available.\nCurrent: {update_info.current_version}\nLatest: {update_info.latest_version}")
        else:
            desc = QLabel("An update is available.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addSpacing(20)

        update_btn = QPushButton("Update Now")
        update_btn.setObjectName("successBtn")
        update_btn.setFixedHeight(42)
        update_btn.setFixedWidth(200)
        layout.addWidget(update_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        skip_btn = QPushButton("Skip")
        skip_btn.setObjectName("toolBtn")
        skip_btn.setFixedHeight(42)
        skip_btn.setFixedWidth(200)
        layout.addWidget(skip_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
