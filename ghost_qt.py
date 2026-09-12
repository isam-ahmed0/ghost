"""Ghost Qt GUI entry point — always launches PySide6 GUI."""
import os
import sys
import certifi
import multiprocessing

sys.setrecursionlimit(10000)
os.environ["SSL_CERT_FILE"] = certifi.where()

if sys.platform == "darwin":
    multiprocessing.set_start_method("fork", force=True)

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

from utils.files import get_application_support
from utils.config import Config
from utils import startup_check, check_fonts, console, load_fonts, is_admin, run_elevated, relaunch_normal, send_telemetry_ping, get_update_info
from gui_qt.main import run_qt_gui


def main():
    get_application_support()
    update_info = get_update_info()
    startup_check.check()
    cfg = Config()
    cfg.check()
    cfg.set_headless(False)
    send_telemetry_ping()

    if cfg.get_skip_fonts():
        cfg.set_skip_fonts(False)
    elif not check_fonts():
        if sys.platform == "win32" and not is_admin():
            run_elevated()
            return
        load_fonts()

    run_qt_gui(update_info=update_info)


if __name__ == "__main__":
    main()
