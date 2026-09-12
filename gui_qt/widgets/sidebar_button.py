"""Sidebar button with hover glow animation (from reference2)."""
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QIcon
import gui_qt.theme as theme


class SidebarButton(QPushButton):
    """Icon-only sidebar button with hover glow effect."""

    def __init__(self, icon, tooltip="", parent=None):
        super().__init__(parent)
        self.setIcon(icon)
        self.setToolTip(tooltip)
        self.setCheckable(True)
        self.setFixedHeight(42)
        self.setMinimumWidth(45)
        self.setIconSize(self.sizeHint())
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_glow()

    def _setup_glow(self):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(0)
        self._shadow.setOffset(0, 0)
        self._shadow.setColor(QColor(theme.ACCENT))
        self.setGraphicsEffect(self._shadow)

        self._glow_anim = QPropertyAnimation(self._shadow, b"blurRadius", self)
        self._glow_anim.setDuration(150)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        if not self.isChecked():
            self._glow_anim.stop()
            self._glow_anim.setStartValue(self._shadow.blurRadius())
            self._glow_anim.setEndValue(18)
            self._glow_anim.start()

    def leaveEvent(self, event):
        self._glow_anim.stop()
        self._glow_anim.setStartValue(self._shadow.blurRadius())
        self._glow_anim.setEndValue(0)
        self._glow_anim.start()
