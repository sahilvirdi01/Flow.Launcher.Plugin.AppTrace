from pathlib import Path

from flowlauncher import FlowLauncher

from app_finder import find_apps
from actions import open_folder, launch_app, copy_to_clipboard


DEFAULT_ICON = "assets\\favicon.ico"

LAUNCHABLE_EXTENSIONS = {".exe", ".lnk", ".bat", ".cmd", ".com"}


def is_launchable_path(path_value):
    if not path_value:
        return False

    path = Path(path_value)

    if not path.exists() or not path.is_file():
        return False

    return path.suffix.lower() in LAUNCHABLE_EXTENSIONS

def safe_folder_from_app(app):
    install_folder = app.get("install_folder")
    exe_path = app.get("exe_path")

    if install_folder:
        return install_folder

    if exe_path:
        return str(Path(exe_path).parent)

    return None


def short_version(version):
    if not version:
        return None

    parts = version.split(".")

    if len(parts) >= 2:
        return f"v{parts[0]}.{parts[1]}"

    return f"v{version}"


def build_app_subtitle(app, install_folder):
    publisher = app.get("publisher")
    version = short_version(app.get("version"))
    source = app.get("source")

    parts = []

    if install_folder:
        parts.append("Enter: open folder")
    else:
        parts.append("Folder path not available")

    parts.append("Right-click: more actions")

    if publisher:
        parts.append(publisher)

    if version:
        parts.append(version)

    if source:
        parts.append(source)

    return " • ".join(parts)


class AppTrace(FlowLauncher):
    def query(self, query):
        query = query.strip()

        if not query:
            return [
                {
                    "Title": "Type an app name",
                    "SubTitle": "Example: where chrome, where python, where vscode",
                    "IcoPath": DEFAULT_ICON,
                }
            ]

        apps = find_apps(query)

        if not apps:
            return [
                {
                    "Title": f"No app found for: {query}",
                    "SubTitle": "Try another name like chrome, python, git, node, code",
                    "IcoPath": DEFAULT_ICON,
                }
            ]

        results = []

        for app in apps[:8]:
            name = app.get("name") or "Unknown app"
            exe_path = app.get("exe_path")
            install_folder = safe_folder_from_app(app)

            results.append(
                {
                    "Title": name,
                    "SubTitle": build_app_subtitle(app, install_folder),
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "open_app_folder",
                        "parameters": [install_folder],
                    },
                    "ContextData": [
                        name,
                        exe_path,
                        install_folder,
                    ],
                }
            )

        return results

    def open_app_folder(self, install_folder):
        if install_folder:
            open_folder(install_folder)

    def launch_selected_app(self, exe_path):
        if is_launchable_path(exe_path):
            launch_app(exe_path)

    def copy_selected_path(self, path):
        if path:
            copy_to_clipboard(path)

    def context_menu(self, data):
        name, exe_path, install_folder = data

        results = []

        if install_folder:
            results.append(
                {
                    "Title": "Open install folder",
                    "SubTitle": install_folder,
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "open_app_folder",
                        "parameters": [install_folder],
                    },
                }
            )

        if is_launchable_path(exe_path):
            results.append(
                {
                    "Title": f"Launch {name}",
                    "SubTitle": exe_path,
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "launch_selected_app",
                        "parameters": [exe_path],
                    },
                }
            )

            results.append(
                {
                    "Title": "Copy executable path",
                    "SubTitle": exe_path,
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "copy_selected_path",
                        "parameters": [exe_path],
                    },
                }
            )

        if install_folder:
            results.append(
                {
                    "Title": "Copy install folder path",
                    "SubTitle": install_folder,
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "copy_selected_path",
                        "parameters": [install_folder],
                    },
                }
            )

        if not results:
            results.append(
                {
                    "Title": "No actions available",
                    "SubTitle": "This app was found, but no valid path was available",
                    "IcoPath": DEFAULT_ICON,
                }
            )

        return results


if __name__ == "__main__":
    AppTrace()