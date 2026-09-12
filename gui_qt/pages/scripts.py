"""Scripts page for Ghost Qt GUI."""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from utils.config import Config
from utils.files import get_application_support, open_path_in_explorer
from utils.defaults import DEFAULT_SCRIPT
import gui_qt.theme as theme


class ScriptsPage(QWidget):
    def __init__(self, gui=None, bot_controller=None, parent=None):
        super().__init__(parent)
        self.gui = gui
        self.bot_controller = bot_controller
        self.cfg = Config()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(12)

        # Title
        title = QLabel("Scripts")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Header with search + buttons
        header = QHBoxLayout()
        header.setSpacing(8)

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search local scripts...")
        self.search_entry.textChanged.connect(self._filter_scripts)
        header.addWidget(self.search_entry)

        open_folder_btn = QPushButton()
        open_folder_btn.setObjectName("toolBtn")
        open_folder_btn.setFixedSize(38, 38)
        open_folder_btn.clicked.connect(
            lambda: open_path_in_explorer(get_application_support() + "/scripts")
        )
        header.addWidget(open_folder_btn)

        new_btn = QPushButton("+")
        new_btn.setObjectName("primaryBtn")
        new_btn.setFixedSize(38, 38)
        new_btn.clicked.connect(self._create_script)
        header.addWidget(new_btn)

        layout.addLayout(header)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Scroll area for scripts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scripts_container = QWidget()
        self.scripts_layout = QVBoxLayout(self.scripts_container)
        self.scripts_layout.setContentsMargins(0, 0, 0, 0)
        self.scripts_layout.setSpacing(6)
        self.scripts_layout.addStretch()

        scroll.setWidget(self.scripts_container)
        layout.addWidget(scroll)

        self._refresh_scripts()

    def _refresh_scripts(self):
        # Clear existing
        while self.scripts_layout.count() > 1:
            item = self.scripts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        scripts = self.cfg.get_scripts() if hasattr(self.cfg, 'get_scripts') else []
        for script in scripts:
            card = self._make_script_card(script)
            self.scripts_layout.insertWidget(self.scripts_layout.count() - 1, card)

    def _make_script_card(self, script):
        frame = QFrame()
        frame.setObjectName("pageCard")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        name_label = QLabel(script)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(name_label)

        layout.addStretch()

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("toolBtn")
        edit_btn.setFixedHeight(32)
        edit_btn.clicked.connect(lambda: self._open_editor(script))
        layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.setFixedHeight(32)
        delete_btn.clicked.connect(lambda: self._delete_script(script))
        layout.addWidget(delete_btn)

        return frame

    def _open_editor(self, script):
        import subprocess
        path = get_application_support() + f"/scripts/{script}"
        try:
            subprocess.run(["code", path], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception:
            try:
                subprocess.run(["notepad", path], creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                pass

    def _delete_script(self, script):
        reply = QMessageBox.question(
            self, "Delete Script",
            f"Are you sure you want to delete {script}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            os.remove(get_application_support() + f"/scripts/{script}")
            self._refresh_scripts()

    def _create_script(self):
        num = 0
        name = "example.py"
        scripts_dir = get_application_support() + "/scripts"
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)

        while os.path.exists(f"{scripts_dir}/{name}"):
            num += 1
            name = f"example{num}.py"

        with open(f"{scripts_dir}/{name}", "w") as f:
            f.write(DEFAULT_SCRIPT)

        self._refresh_scripts()

    def _filter_scripts(self, text):
        for i in range(self.scripts_layout.count()):
            item = self.scripts_layout.itemAt(i)
            if item and item.widget():
                card = item.widget()
                name_label = card.findChild(QLabel)
                if name_label:
                    card.setVisible(text.lower() in name_label.text().lower() or text == "")
