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
    except OSError:
        return None


def clean_icon_path(icon_path):
    
    if not icon_path:
        return None

    icon_path = icon_path.strip().strip('"')

    if "," in icon_path:
        icon_path = icon_path.split(",")[0].strip().strip('"')

    return icon_path


def is_valid_path(path_value):
    if not path_value:
        return False

    try:
        return Path(path_value).exists()
    except OSError:
        return False


def find_in_registry(query):
    query = query.lower().strip()
    results = []

    for root, registry_path in REGISTRY_PATHS:
        try:
            registry_key = winreg.OpenKey(root, registry_path)
        except OSError:
            continue

        subkey_count = winreg.QueryInfoKey(registry_key)[0]

        for index in range(subkey_count):
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

                if exe_path and not is_valid_path(exe_path):
                    exe_path = None

                install_folder = install_location

                if not install_folder and exe_path:
                    install_folder = str(Path(exe_path).parent)

                if install_folder and not is_valid_path(install_folder):
                    install_folder = None

                results.append(
                    {
                        "name": display_name,
                        "exe_path": exe_path,
                        "install_folder": install_folder,
                        "version": display_version,
                        "publisher": publisher,
                        "source": "Registry",
                    }
                )

            except OSError:
                continue

    return results


def find_in_path(query):
    query = query.strip()

    if not query:
        return []

    exe_path = shutil.which(query)

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
            "source": "PATH",
        }
    ]


def remove_duplicates(results):
    seen = set()
    unique_results = []

    for app in results:
        key = (
            app.get("name"),
            app.get("exe_path"),
            app.get("install_folder"),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_results.append(app)

    return unique_results


def find_apps(query):
    query = query.strip()

    if not query:
        return []

    results = []
    results.extend(find_in_registry(query))
    results.extend(find_in_path(query))

    return remove_duplicates(results)


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