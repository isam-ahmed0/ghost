"""Custom frameless titlebar for Ghost Qt GUI."""
import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent

import gui_qt.theme as theme
from gui_qt.images import Images


class Titlebar(QWidget):
    """Custom titlebar for frameless window — drag, minimize, close."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setObjectName("titlebar")
        self.images = Images()
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(8)

        self._ico = QLabel()
        self._ico.setPixmap(self.images.get_pixmap("ghost-logo").scaled(
            16, 16, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ) if self.images.get_pixmap("ghost-logo") else QPixmap())
        layout.addWidget(self._ico)

        self._title = QLabel("Ghost")
        self._title.setStyleSheet("font-weight: 600; font-size: 12px;")
        layout.addWidget(self._title)

        layout.addStretch()

        self._min_btn = QPushButton("—")
        self._min_btn.setFixedSize(32, 24)
        self._min_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._min_btn.clicked.connect(self._minimize)
        layout.addWidget(self._min_btn)

        self._close_btn = QPushButton("×")
        self._close_btn.setFixedSize(32, 24)
        self._close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_btn.clicked.connect(self._close)
        layout.addWidget(self._close_btn)

    def _minimize(self):
        window = self.window()
        if window:
            window.showMinimized()

    def _close(self):
        window = self.window()
        if window:
            window.close()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_pos is not None:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_pos = None
        event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        window = self.window()
        if window:
            if window.isMaximized():
                window.showNormal()
            else:
                window.showMaximized()
        event.accept()
