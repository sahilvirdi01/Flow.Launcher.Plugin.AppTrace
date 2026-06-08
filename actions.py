from pathlib import Path
import os
import subprocess


def open_folder(folder_path):
    if not folder_path:
        return False

    path = Path(folder_path)

    if not path.exists():
        return False

    os.startfile(str(path))
    return True


def launch_app(exe_path):
    if not exe_path:
        return False

    path = Path(exe_path)

    if not path.exists():
        return False

    subprocess.Popen([str(path)], shell=False)
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