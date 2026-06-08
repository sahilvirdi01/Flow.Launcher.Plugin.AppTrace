from pathlib import Path
import os
import subprocess


def open_folder(folder_path):
    if not folder_path:
        return False

    path = Path(folder_path)

    if not path.exists() or not path.is_dir():
        return False

    os.startfile(str(path))
    return True


def launch_app(app_path):
    if not app_path:
        return False

    path = Path(app_path)

    if not path.exists():
        return False

    # os.startfile is better for Windows app launching than subprocess.Popen
    os.startfile(str(path))
    return True


def copy_to_clipboard(text):
    if not text:
        return False

    subprocess.run(
        "clip",
        input=text,
        text=True,
        shell=True,
        check=False
    )

    return True