from pathlib import Path

from flowlauncher import FlowLauncher

from app_finder import find_apps
from actions import open_folder, launch_app, copy_to_clipboard


DEFAULT_ICON = "icons/app.png"


def safe_folder_from_app(app):
    """
    Returns the best folder path we can use.

    Priority:
    1. install_folder
    2. parent folder of exe_path
    """
    install_folder = app.get("install_folder")
    exe_path = app.get("exe_path")

    if install_folder:
        return install_folder

    if exe_path:
        return str(Path(exe_path).parent)

    return None


def safe_main_path_from_app(app):
    exe_path = app.get("exe_path")
    install_folder = safe_folder_from_app(app)

    return exe_path or install_folder or "Path not found"


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

        for app in apps[:5]:
            name = app.get("name") or "Unknown app"
            exe_path = app.get("exe_path")
            install_folder = safe_folder_from_app(app)
            version = app.get("version")
            publisher = app.get("publisher")
            source = app.get("source")

            main_path = safe_main_path_from_app(app)

            details = []

            if version:
                details.append(f"Version: {version}")

            if publisher:
                details.append(f"Publisher: {publisher}")

            if source:
                details.append(f"Source: {source}")

            detail_text = " | ".join(details)
            subtitle = main_path

            if detail_text:
                subtitle = f"{main_path} | {detail_text}"

            # Main result: open install folder
            results.append(
                {
                    "Title": name,
                    "SubTitle": f"Open install folder | {subtitle}",
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "open_app_folder",
                        "parameters": [install_folder],
                    },
                }
            )

            # Visible action: launch app
            if exe_path:
                results.append(
                    {
                        "Title": f"↳ Launch {name}",
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
                        "Title": "↳ Copy executable path",
                        "SubTitle": exe_path,
                        "IcoPath": DEFAULT_ICON,
                        "JsonRPCAction": {
                            "method": "copy_selected_path",
                            "parameters": [exe_path],
                        },
                    }
                )

            # Visible action: copy install folder
            if install_folder:
                results.append(
                    {
                        "Title": "↳ Copy install folder path",
                        "SubTitle": install_folder,
                        "IcoPath": DEFAULT_ICON,
                        "JsonRPCAction": {
                            "method": "copy_selected_path",
                            "parameters": [install_folder],
                        },
                    }
                )

        return results

    def open_app_folder(self, install_folder):
        if not install_folder:
            return

        open_folder(install_folder)

    def launch_selected_app(self, exe_path):
        if not exe_path:
            return

        launch_app(exe_path)

    def copy_selected_path(self, path):
        if not path:
            return

        copy_to_clipboard(path)


if __name__ == "__main__":
    AppTrace()