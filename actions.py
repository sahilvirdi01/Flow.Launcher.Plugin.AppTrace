from pathlib import Path
import os
import subprocess
import pyperclip


def open_folder(folder_path):
    if not folder_path:
        return

    path = Path(folder_path)

    if path.exists():
        os.startfile(str(path))


def launch_app(exe_path):
    if not exe_path:
        return

    path = Path(exe_path)

    if path.exists():
        subprocess.Popen([str(path)], shell=False)


def copy_to_clipboard(text):
    if text:
        pyperclip.copy(text)