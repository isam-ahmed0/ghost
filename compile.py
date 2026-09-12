import os
import sys
import platform
import subprocess
import argparse
import plistlib

from utils.config import VERSION

def sign_macos_app(path):
    print(f"Signing macOS app at {path}...")
    subprocess.run([
        "codesign",
        "--deep",
        "--force",
        "--verbose",
        "--sign",
        "-",
        path
    ], check=True)

def build(qt=False):
    system = platform.system()

    name = "Ghost"
    entry_script = "ghost.py"
    icon = "data/icon.ico" if system == "Windows" else "data/icon.png"

    args = [
        sys.executable, "-m", "PyInstaller",
        f"--name={name}",
        "--clean",
        "--noconfirm",
        f"--icon={icon}",
        "--hidden-import=discord",
        "--hidden-import=discord.ext.commands",
        "--collect-submodules=discord",
    ]

    if qt:
        args += [
            "--onedir",
            "--windowed",
            "--noupx",
            "--hidden-import=PySide6.QtWidgets",
            "--hidden-import=PySide6.QtCore",
            "--hidden-import=PySide6.QtGui",
            "--collect-submodules=curl_cffi",
        ]
    else:
        args += [
            "--onefile",
            "--noconsole",
            "--hidden-import=PIL.ImageTk",
            "--hidden-import=PIL._tkinter_finder",
        ]

    args.append(entry_script)

    if system == "Windows":
        args += [
            "--add-data=data\\*;data",
            "--add-data=data\\fonts\\*;data/fonts",
            "--add-data=data\\icons\\*;data/icons",
        ]
    else:
        args += [
            "--add-data=data/*:data",
            "--add-data=data/fonts/*:data/fonts",
            "--add-data=data/icons/*:data/icons",
        ]
        if not qt:
            args.append("--osx-bundle-identifier=fun.benny.ghost")

    mode = "Qt GUI (one-folder)" if qt else "CLI (one-file)"
    print(f"Building Ghost {VERSION} for {system} [{mode}]...")
    subprocess.run(args, check=True)

    if system == "Darwin":
        app_path = os.path.join("dist", "Ghost.app")
        sign_macos_app(app_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Ghost")
    parser.add_argument("--qt", action="store_true", help="Build Qt GUI (one-folder, windowed)")
    args = parser.parse_args()
    build(qt=args.qt)
