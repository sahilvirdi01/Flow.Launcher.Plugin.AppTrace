from pathlib import Path
import shutil
import winreg


REGISTRY_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
]


def read_registry_value(key, value_name):
    try:
        value, _ = winreg.QueryValueEx(key, value_name)
        return value
    except FileNotFoundError:
        return None
    except OSError:
        return None


def find_in_registry(query: str):
    query = query.lower()
    results = []

    for root, path in REGISTRY_PATHS:
        try:
            registry_key = winreg.OpenKey(root, path)
        except OSError:
            continue

        for index in range(winreg.QueryInfoKey(registry_key)[0]):
            try:
                subkey_name = winreg.EnumKey(registry_key, index)
                subkey = winreg.OpenKey(registry_key, subkey_name)

                display_name = read_registry_value(subkey, "DisplayName")
                install_location = read_registry_value(subkey, "InstallLocation")
                display_icon = read_registry_value(subkey, "DisplayIcon")
                display_version = read_registry_value(subkey, "DisplayVersion")
                publisher = read_registry_value(subkey, "Publisher")

                if not display_name:
                    continue

                if query not in display_name.lower():
                    continue

                exe_path = clean_icon_path(display_icon)
                install_folder = install_location

                if not install_folder and exe_path:
                    install_folder = str(Path(exe_path).parent)

                results.append(
                    {
                        "name": display_name,
                        "exe_path": exe_path,
                        "install_folder": install_folder,
                        "version": display_version,
                        "publisher": publisher,
                        "source": "Registry"
                    }
                )

            except OSError:
                continue

    return results


def clean_icon_path(icon_path):
    if not icon_path:
        return None

    icon_path = icon_path.strip().strip('"')

    if "," in icon_path:
        possible_path = icon_path.split(",")[0]
        return possible_path.strip().strip('"')

    return icon_path


def find_in_path(app_name: str):
    exe_path = shutil.which(app_name)

    if not exe_path:
        return []

    path = Path(exe_path)

    return [
        {
            "name": path.stem,
            "exe_path": str(path),
            "install_folder": str(path.parent),
            "version": None,
            "publisher": None,
            "source": "PATH"
        }
    ]


def find_apps(query: str):
    results = []

    results.extend(find_in_registry(query))
    results.extend(find_in_path(query))

    return results


if __name__ == "__main__":
    query = input("Enter app name: ").strip()
    results = find_apps(query)

    if not results:
        print("No app found.")
    else:
        for app in results:
            print("-" * 40)
            print("Name:", app["name"])
            print("Executable:", app["exe_path"])
            print("Folder:", app["install_folder"])
            print("Version:", app["version"])
            print("Publisher:", app["publisher"])
            print("Source:", app["source"])