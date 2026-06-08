from flowlauncher import FlowLauncher

from app_finder import find_apps
from actions import open_folder, launch_app, copy_to_clipboard


DEFAULT_ICON = "icons/app.png"


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
                    "SubTitle": "Try another name, for example chrome, python, git, node",
                    "IcoPath": DEFAULT_ICON,
                }
            ]

        results = []

        for app in apps[:10]:
            name = app.get("name") or "Unknown app"
            exe_path = app.get("exe_path")
            install_folder = app.get("install_folder")
            version = app.get("version")
            publisher = app.get("publisher")
            source = app.get("source")

            main_path = exe_path or install_folder or "Path not found"

            extra_info = []

            if version:
                extra_info.append(f"Version: {version}")

            if publisher:
                extra_info.append(f"Publisher: {publisher}")

            if source:
                extra_info.append(f"Source: {source}")

            subtitle = main_path

            if extra_info:
                subtitle = f"{main_path} | {' | '.join(extra_info)}"

            results.append(
                {
                    "Title": name,
                    "SubTitle": subtitle,
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
        open_folder(install_folder)

    def launch_selected_app(self, exe_path):
        launch_app(exe_path)

    def copy_selected_path(self, path):
        copy_to_clipboard(path)

    def context_menu(self, data):
        name, exe_path, install_folder = data

        menu_items = []

        if install_folder:
            menu_items.append(
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

        if exe_path:
            menu_items.append(
                {
                    "Title": "Launch app",
                    "SubTitle": exe_path,
                    "IcoPath": DEFAULT_ICON,
                    "JsonRPCAction": {
                        "method": "launch_selected_app",
                        "parameters": [exe_path],
                    },
                }
            )

            menu_items.append(
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
            menu_items.append(
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

        return menu_items


if __name__ == "__main__":
    AppTrace()