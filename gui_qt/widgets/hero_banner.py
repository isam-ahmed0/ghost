"""Hero banner widget for Ghost Qt GUI (adapted from reference2)."""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont, QFontMetrics
from pathlib import Path
import gui_qt.theme as theme


_HERO_IMAGE_PATH = Path(__file__).parent.parent / "data" / "waves.png"


class HeroBanner(QLabel):
    """Custom hero banner with gradient background, glow orbs, and text."""

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent)
        self._title = title
        self._subtitle = subtitle
        self._hero_image = None
        self.setMinimumHeight(180)
        self.setMaximumHeight(180)

        if _HERO_IMAGE_PATH.exists():
            self._hero_image = QPixmap(str(_HERO_IMAGE_PATH))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        accent = self._hex_to_qcolor(theme.ACCENT)
        accent2 = self._hex_to_qcolor(theme.ACCENT_2)
        bg_base = self._hex_to_qcolor(theme.BG_BASE)
        bg_surface = self._hex_to_qcolor(theme.BG_SURFACE)
        bg_elevated = self._hex_to_qcolor(theme.BG_ELEVATED)
        text_bright = self._hex_to_qcolor(theme.TEXT_BRIGHT)
        text_secondary = self._hex_to_qcolor(theme.TEXT_SECONDARY)

        # Background
        if self._hero_image and not self._hero_image.isNull():
            scaled = self._hero_image.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(0, 0, scaled)
            painter.fillRect(0, 0, w, h, QColor(bg_base.red(), bg_base.green(), bg_base.blue(), 160))
        else:
            gradient = QLinearGradient(0, 0, w, h)
            gradient.setColorAt(0, bg_base)
            gradient.setColorAt(0.5, bg_surface)
            gradient.setColorAt(1, bg_base)
            painter.fillRect(0, 0, w, h, gradient)

        # Glow orbs
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(accent.red(), accent.green(), accent.blue(), 25))
        painter.drawEllipse(int(w * 0.75) - 80, int(h * 0.35) - 80, 160, 160)
        painter.setBrush(QColor(accent2.red(), accent2.green(), accent2.blue(), 20))
        painter.drawEllipse(int(w * 0.15) - 65, int(h * 0.7) - 65, 130, 130)

        # Bottom accent line
        gradient = QLinearGradient(0, 0, w, 0)
        gradient.setColorAt(0, QColor(accent.red(), accent.green(), accent.blue(), 200))
        gradient.setColorAt(1, QColor(accent2.red(), accent2.green(), accent2.blue(), 200))
        painter.setBrush(gradient)
        painter.drawRect(0, h - 3, w, 3)

        # Title
        painter.setPen(text_bright)
        title_font = QFont("Host Grotesk", 24)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(28, int(h * 0.45), self._title)

        # Subtitle
        painter.setPen(text_secondary)
        sub_font = QFont("Host Grotesk", 13)
        painter.setFont(sub_font)
        painter.drawText(28, int(h * 0.45) + 32, self._subtitle)

        # Version badge
        from utils.config import VERSION
        badge_text = f"v{VERSION}"
        badge_font = QFont("Host Grotesk", 11)
        painter.setFont(badge_font)
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(badge_text) + 20
        bx, by = 28, h - 38
        painter.setBrush(QColor(bg_elevated.red(), bg_elevated.green(), bg_elevated.blue(), 220))
        painter.setPen(QColor(accent.red(), accent.green(), accent.blue(), 100))
        painter.drawRoundedRect(bx, by, tw, 24, 12, 12)
        painter.setPen(accent2)
        painter.drawText(bx, by, tw, 24, Qt.AlignmentFlag.AlignCenter, badge_text)

        painter.end()

    @staticmethod
    def _hex_to_qcolor(hex_str, alpha=255):
        h = hex_str.lstrip("#")
        return QColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)
