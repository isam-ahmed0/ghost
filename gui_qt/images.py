"""Image loader for Ghost Qt GUI — loads PNGs from data/icons/ as QIcon/QPixmap."""
import os
from pathlib import Path
from PySide6.QtGui import QPixmap, QIcon, QColor, QPainter, QPainterPath
from PySide6.QtCore import Qt
import gui_qt.theme as theme


_DATA_DIR = Path(__file__).parent.parent / "data"
_ICONS_DIR = _DATA_DIR / "icons"

ICON_MAP = {
    "home": "house-solid.png",
    "settings": "gear-solid.png",
    "theming": "paint-roller-solid.png",
    "snipers": "crosshairs-solid.png",
    "rich_presence": "discord-brands-solid.png",
    "console": "terminal-solid.png",
    "logout": "power-off-solid.png",
    "scripts": "script-solid.png",
    "apis": "cloud-solid.png",
    "session_spoofing": "shuffle-solid.png",
    "trash": "trash-solid.png",
    "trash-white": "trash-solid-white.png",
    "github": "github-brands-solid.png",
    "restart": "rotate-right-solid.png",
    "ghost-logo": "ghost-logo.png",
    "min": "min-solid.png",
    "max": "max-solid.png",
    "checkmark": "check-solid.png",
    "search": "magnifying-glass-solid.png",
    "plus": "plus-solid.png",
    "folder-open": "folder-open-solid.png",
    "file-signature": "file-signature-solid.png",
    "left-chevron": "chevron-left-solid.png",
    "right-chevron": "chevron-right-solid.png",
    "tools": "screwdriver-wrench-solid.png",
    "reset": "rotate-left-solid.png",
    "play": "play-solid.png",
    "stop": "stop-solid.png",
    "download": "download-solid.png",
    "copy": "copy-solid.png",
    "surveillance": "eye-solid.png",
    "message_logger": "log-solid.png",
    "auto_afk_reply": "reply-all-solid.png",
    "backups": "archive-solid.png",
    "user_lookup": "magnifying-glass-solid.png",
    "password_gen": "key-solid.png",
    "telemetry": "chart-solid.png",
}

# Default sizes per icon category
ICON_SIZES = {
    "bigger": (23, 23),
    "icon": (20, 20),
    "small": (15, 15),
    "smaller": (12, 12),
    "tiny": (10, 10),
    "logo": (50, 50),
}

ICON_CATEGORIES = {
    "bigger": ["scripts"],
    "small": ["trash", "github", "restart", "checkmark", "left-chevron",
              "file-signature", "trash-white", "right-chevron-small"],
    "tiny": ["submit", "max", "min", "search", "right-chevron-tiny", "copy-tiny"],
    "smaller": ["folder-open", "plus", "reset", "play", "stop", "right-chevron",
                "download", "copy"],
    "logo": ["ghost-logo"],
}


class Images:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Images, cls).__new__(cls)
            cls._instance._init_images()
        return cls._instance

    def _init_images(self):
        self.pixmaps = {}
        self.original_pixmaps = {}
        self._load_all()

    def _get_size(self, key):
        for cat, keys in ICON_CATEGORIES.items():
            if key in keys:
                return ICON_SIZES[cat]
        return ICON_SIZES["icon"]

    def _load_all(self):
        for key, filename in ICON_MAP.items():
            path = _ICONS_DIR / filename
            if path.exists():
                size = self._get_size(key)
                pixmap = QPixmap(str(path))
                if not pixmap.isNull():
                    scaled = pixmap.scaled(
                        size[0], size[1],
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    self.pixmaps[key] = scaled
                    self.original_pixmaps[key] = pixmap

    def get_pixmap(self, key):
        return self.pixmaps.get(key)

    def get_icon(self, key):
        pm = self.pixmaps.get(key)
        if pm:
            return QIcon(pm)
        return QIcon()

    def get_colored_icon(self, key, color_hex):
        """Return icon recolored to the given hex color."""
        pm = self.original_pixmaps.get(key)
        if not pm:
            return QIcon()
        colored = self._recolor_pixmap(pm, color_hex)
        return QIcon(colored)

    def _recolor_pixmap(self, source_pixmap, color_hex):
        """Recolor white/light pixels of a pixmap to the given color."""
        h = color_hex.lstrip("#")
        target = QColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        image = source_pixmap.toImage().convertToFormat(
            self._qimage_format()
        )
        for y in range(image.height()):
            for x in range(image.width()):
                px = QColor(image.pixelColor(x, y))
                if px.lightnessF() > 0.7:
                    image.setPixelColor(x, y, target)
        return QPixmap.fromImage(image)

    @staticmethod
    def _qimage_format():
        from PySide6.QtGui import QImage
        return QImage.Format.Format_ARGB32

    def get(self, key):
        """Compatibility with tkinter images.get() — returns QPixmap."""
        return self.pixmaps.get(key)
