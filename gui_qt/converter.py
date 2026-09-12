#!/usr/bin/env python3
"""
Ghost GUI Auto-Converter — tkinter → PySide6 Qt
Reads ghost/gui/**/*.py (tkinter source) and generates ghost/gui_qt/**/*.py (Qt output).

Usage:
    python gui_qt/converter.py [--force] [--dry-run]

Flags:
    --force     Regenerate all files, even unchanged ones
    --dry-run   Show what would be generated without writing files
"""
import ast
import hashlib
import os
import sys
import textwrap
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent.resolve()
GHOST_ROOT = SCRIPT_DIR.parent
TK_GUI_DIR = GHOST_ROOT / "gui"
QT_GUI_DIR = SCRIPT_DIR
CACHE_FILE = QT_GUI_DIR / ".converter_cache.json"

# ---------------------------------------------------------------------------
# Widget mapping: tkinter → Qt
# ---------------------------------------------------------------------------
WIDGET_MAP = {
    "ttk.Frame": "QWidget",
    "ttk.Label": "QLabel",
    "ttk.Button": "QPushButton",
    "ttk.Entry": "QLineEdit",
    "ttk.Text": "QTextEdit",
    "ttk.Separator": "QFrame",
    "ttk.Checkbutton": "QCheckBox",
    "ttk.Combobox": "QComboBox",
    "ttk.Spinbox": "QSpinBox",
    "ttk.Progressbar": "QProgressBar",
    "ttk.Scrollbar": "QScrollBar",
    "ttk.Treeview": "QTreeWidget",
    "ttk.Notebook": "QTabWidget",
    "ttk.LabelFrame": "QGroupBox",
    "RoundedFrame": "QFrame",
    "RoundedButton": "QPushButton",
    "RoundedProgressbar": "QProgressBar",
    "RoundedSlider": "QSlider",
    "RoundedSwitch": "QCheckBox",
    "ScrolledFrame": "QScrollArea",
}

# Style mapping: ghost style enum → theme module constant
STYLE_MAP = {
    "Style.WINDOW_BORDER.value": "theme.BG_SIDEBAR",
    "Style.SIDEBAR_SELECTED.value": "theme.BG_HOVER",
    "Style.ENTRY_BG.value": "theme.BG_ELEVATED",
    "Style.ENTRY_FG.value": "theme.TEXT_PRIMARY",
    "Style.SETTINGS_PILL_HOVER.value": "theme.BG_HOVER",
    "Style.SETTINGS_PILL_SELECTED.value": "theme.BG_ACTIVE",
    "Style.DARK_GREY.value": "theme.TEXT_MUTED",
    "Style.LIGHT_GREY.value": "theme.TEXT_SECONDARY",
    "Style.PRIMARY_BTN_HOVER.value": "theme.ACCENT_HOVER",
    "Style.TOOL_HOVER.value": "theme.BG_HOVER",
}

# Layout method mapping
LAYOUT_MAP = {
    "pack": "QVBoxLayout",
    "grid": "QGridLayout",
    "place": "QVBoxLayout",
}

# ---------------------------------------------------------------------------
# Hash cache for change detection
# ---------------------------------------------------------------------------
def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _load_cache() -> dict:
    if CACHE_FILE.exists():
        import json
        return json.loads(CACHE_FILE.read_text())
    return {}


def _save_cache(cache: dict):
    import json
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


# ---------------------------------------------------------------------------
# AST-based converter
# ---------------------------------------------------------------------------
class TkinterToQtConverter:
    """Converts a single tkinter source file to Qt equivalent."""

    def __init__(self, source_path: Path, output_path: Path):
        self.source = source_path
        self.output = output_path
        self.imports = set()
        self.qt_imports = set()
        self.classes = []
        self.warnings = []

    def convert(self) -> str:
        """Main conversion entry point."""
        source = self.source.read_text(encoding="utf-8")

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            self.warnings.append(f"Syntax error in {self.source.name}: {e}")
            return self._fallback_convert(source)

        self._analyze_imports(tree)
        self._analyze_classes(tree)

        return self._generate_output(source)

    def _analyze_imports(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports.add(node.module)

    def _analyze_classes(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(ast.dump(base))
                self.classes.append({
                    "name": node.name,
                    "bases": bases,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                })

    def _fallback_convert(self, source: str) -> str:
        """Fallback: wrap original source with Qt-compatible header."""
        return self._generate_output(source)

    def _generate_output(self, source: str) -> str:
        lines = []
        lines.append(f'"""Auto-converted from {self.source.name} (tkinter → Qt)."""')
        lines.append("")

        # Qt imports
        qt_imports = self._get_recommended_imports()
        for imp in sorted(qt_imports):
            lines.append(imp)
        lines.append("")

        # Theme import
        lines.append("import gui_qt.theme as theme")
        lines.append("")

        # Convert source sections
        for line in source.split("\n"):
            converted = self._convert_line(line)
            lines.append(converted)

        return "\n".join(lines)

    def _get_recommended_imports(self) -> set:
        imports = set()

        if any(c["bases"] and "QWidget" in c["bases"] for c in self.classes):
            imports.add("from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout")

        has_label = any("ttk.Label" in str(c) for c in self.classes)
        has_button = any("ttk.Button" in str(c) or "RoundedButton" in str(c) for c in self.classes)
        has_entry = any("ttk.Entry" in str(c) for c in self.classes)

        if has_label:
            imports.add("from PySide6.QtWidgets import QLabel")
        if has_button:
            imports.add("from PySide6.QtWidgets import QPushButton")
        if has_entry:
            imports.add("from PySide6.QtWidgets import QLineEdit")

        imports.add("from PySide6.QtCore import Qt")

        return imports

    def _convert_line(self, line: str) -> str:
        converted = line

        # Replace widget constructors
        for tk_widget, qt_widget in WIDGET_MAP.items():
            converted = converted.replace(tk_widget, qt_widget)

        # Replace style references
        for tk_style, qt_style in STYLE_MAP.items():
            converted = converted.replace(tk_style, qt_style)

        # Convert pack/grid calls to Qt layout hints (comments)
        if ".pack(" in converted and "def " not in converted:
            converted = self._convert_pack(converted)
        elif ".grid(" in converted and "def " not in converted:
            converted = self._convert_grid(converted)

        # Convert configure calls
        if ".configure(" in converted:
            converted = self._convert_configure(converted)

        # Convert bind calls
        if ".bind(" in converted:
            converted = self._convert_bind(converted)

        return converted

    def _convert_pack(self, line: str) -> str:
        """Add layout comment for pack() calls."""
        stripped = line.strip()
        if stripped.startswith("#"):
            return line
        indent = len(line) - len(line.lstrip())
        return " " * indent + "# TODO:layout " + stripped

    def _convert_grid(self, line: str) -> str:
        """Add layout comment for grid() calls."""
        stripped = line.strip()
        if stripped.startswith("#"):
            return line
        indent = len(line) - len(line.lstrip())
        return " " * indent + "# TODO:layout " + stripped

    def _convert_configure(self, line: str) -> str:
        """Convert .configure() to Qt property setting."""
        converted = line

        # background → setStyleSheet
        if "background=" in converted:
            color = converted.split("background=")[1].split(")")[0].strip().rstrip(")")
            indent = len(line) - len(line.lstrip())
            return " " * indent + f"# TODO:style background={color}"

        # foreground → setStyleSheet
        if "foreground=" in converted:
            color = converted.split("foreground=")[1].split(")")[0].strip().rstrip(")")
            indent = len(line) - len(line.lstrip())
            return " " * indent + f"# TODO:style foreground={color}"

        return converted

    def _convert_bind(self, line: str) -> str:
        """Convert .bind() to Qt signal/slot."""
        converted = line

        if '"<Button-1>"' in converted:
            converted = converted.replace('.bind("<Button-1>"', ".clicked.connect(")
        elif '"<Enter>"' in converted:
            converted = converted.replace('.bind("<Enter>"', ".enterEvent.connect(")
        elif '"<Leave>"' in converted:
            converted = converted.replace('.bind("<Leave>"', ".leaveEvent.connect(")
        elif '"<FocusIn>"' in converted:
            converted = converted.replace('.bind("<FocusIn>"', ".focusInEvent.connect(")
        elif '"<FocusOut>"' in converted:
            converted = converted.replace('.bind("<FocusOut>"', ".focusOutEvent.connect(")
        elif '"<Return>"' in converted:
            converted = converted.replace('.bind("<Return>"', ".returnPressed.connect(")
        elif '"<KeyRelease>"' in converted:
            indent = len(line) - len(line.lstrip())
            return " " * indent + "# TODO:event " + line.strip()

        return converted

    def write_output(self, content: str, force: bool = False, dry_run: bool = False):
        if dry_run:
            print(f"[DRY RUN] Would write: {self.output}")
            return

        self.output.parent.mkdir(parents=True, exist_ok=True)

        if not force and self.output.exists():
            existing_hash = _file_hash(self.output)
            new_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
            if existing_hash == new_hash:
                print(f"[SKIP] {self.output.relative_to(GHOST_ROOT)} (unchanged)")
                return

        self.output.write_text(content, encoding="utf-8")
        print(f"[OK] {self.output.relative_to(GHOST_ROOT)}")

        if self.warnings:
            for w in self.warnings:
                print(f"  [WARN] {w}")


# ---------------------------------------------------------------------------
# Conversion registry
# ---------------------------------------------------------------------------
CONVERSIONS = [
    # (source, output)
    ("gui/main.py", "gui_qt/main_converted.py"),
    ("gui/components/sidebar.py", "gui_qt/widgets/sidebar_converted.py"),
    ("gui/components/titlebar.py", "gui_qt/widgets/titlebar_converted.py"),
    ("gui/components/console.py", "gui_qt/widgets/console_converted.py"),
    ("gui/components/rounded_frame.py", "gui_qt/widgets/rounded_frame_converted.py"),
    ("gui/components/rounded_button.py", "gui_qt/widgets/rounded_button_converted.py"),
    ("gui/pages/home.py", "gui_qt/pages/home_converted.py"),
    ("gui/pages/settings.py", "gui_qt/pages/settings_converted.py"),
    ("gui/pages/scripts.py", "gui_qt/pages/scripts_converted.py"),
    ("gui/pages/onboarding.py", "gui_qt/pages/onboarding_converted.py"),
    ("gui/pages/update.py", "gui_qt/pages/update_converted.py"),
    ("gui/pages/tools/tools.py", "gui_qt/pages/tools/tools_converted.py"),
    ("gui/pages/tools/surveillance_page.py", "gui_qt/pages/tools/surveillance_page_converted.py"),
    ("gui/pages/tools/message_logger_page.py", "gui_qt/pages/tools/message_logger_page_converted.py"),
    ("gui/pages/tools/user_lookup_page.py", "gui_qt/pages/tools/user_lookup_page_converted.py"),
    ("gui/pages/tools/password_gen.py", "gui_qt/pages/tools/password_gen_converted.py"),
    ("gui/pages/tools/auto_afk_reply_page.py", "gui_qt/pages/tools/auto_afk_reply_page_converted.py"),
    ("gui/pages/tools/backups_page.py", "gui_qt/pages/tools/backups_page_converted.py"),
    ("gui/helpers/style.py", "gui_qt/theme_converted.py"),
]


def main():
    parser = argparse.ArgumentParser(description="Ghost GUI Auto-Converter")
    parser.add_argument("--force", action="store_true", help="Regenerate all files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    print("=" * 60)
    print("Ghost GUI Auto-Converter: tkinter → PySide6 Qt")
    print("=" * 60)
    print()

    cache = _load_cache()
    converted = 0
    skipped = 0

    for src_rel, out_rel in CONVERSIONS:
        src_path = GHOST_ROOT / src_rel
        out_path = GHOST_ROOT / out_rel

        if not src_path.exists():
            print(f"[SKIP] {src_rel} (source not found)")
            skipped += 1
            continue

        src_hash = _file_hash(src_path)

        # Check if source changed
        if not args.force and src_rel in cache and cache[src_rel] == src_hash:
            print(f"[CACHED] {src_rel}")
            skipped += 1
            continue

        print(f"[CONVERT] {src_rel} → {out_rel}")

        converter = TkinterToQtConverter(src_path, out_path)
        content = converter.convert()
        converter.write_output(content, force=args.force, dry_run=args.dry_run)

        # Update cache
        cache[src_rel] = src_hash
        converted += 1

    if not args.dry_run:
        _save_cache(cache)

    print()
    print(f"Done: {converted} converted, {skipped} skipped")
    print(f"Output: {QT_GUI_DIR.relative_to(GHOST_ROOT)}")
    print()
    print("Generated _converted.py files are drafts. Review and rename to replace originals.")
    print("Run with --force to regenerate all files.")


if __name__ == "__main__":
    main()
