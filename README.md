<h1 align="center">
  <br>
    <img src="/assets/logo.png" alt="Repository Banner" width="20%">  
  <br>
    AppTrace
</h1>


## Description

AppTrace is a plugin for [Flow Launcher](https://www.flowlauncher.com/) that helps you quickly find where Windows applications are installed.

Type an app name using the `where` keyword, and AppTrace will search installed applications and developer tools from the Windows Registry and PATH.

Example:

```text
where flow
```

AppTrace will show matching apps. Select an app to open its install folder, or use the context menu for extra actions like launching the app or copying paths.


## Usage

Type a query after the `where` keyword:

```text
where <app name>
```

Examples:

```text
where chrome
where python
where git
where node
where code
```

The plugin will search for matching installed apps and display them in Flow Launcher.

Select an app result to open its install folder.

Use the result context menu for more actions:

```text
Open install folder
Launch app
Copy executable path
Copy install folder path
```

For example, searching:

```text
where chrome
```

may show:

```text
Google Chrome
Enter: open folder • Right-click: more actions • Google LLC • v126.0 • Registry
```

Context actions may include:

```text
Open install folder
C:\Program Files\Google\Chrome\Application

Launch Google Chrome
C:\Program Files\Google\Chrome\Application\chrome.exe

Copy executable path
C:\Program Files\Google\Chrome\Application\chrome.exe

Copy install folder path
C:\Program Files\Google\Chrome\Application
```


## Features

- Quickly search installed Windows applications from Flow Launcher
- Open an application's install folder
- Copy executable paths
- Copy install folder paths
- Display useful app metadata such as publisher, version, and source
- Search Windows Registry uninstall entries
- Search executables available through PATH

## Installation

### Manual Installation

1. Download the plugin or clone this repository.

2. Copy the `AppTrace` folder to the Flow Launcher plugins directory:

```bash
%APPDATA%\FlowLauncher\Plugins
```

The final structure should look like this:

```text
%APPDATA%\FlowLauncher\Plugins\AppTrace\plugin.json
```

3. Restart Flow Launcher.

4. Search using:

```text
where chrome
```

## Rquirements

You need:

- Windows
- Flow Launcher installed
- Python installed for development

Clone the repository:

```powershell
git clone https://github.com/sahilvirdi01/AppTrace.git
cd AppTrace
```

Install the Flow Launcher Python helper package into the plugin folder:

```powershell
python -m pip install flowlauncher -t .
```

This project vendors the `flowlauncher` helper package inside the plugin folder so normal users do not need to manually install dependencies.


## Limitations

AppTrace currently searches:

```text
Windows Registry uninstall entries
PATH executables
```

Some apps may not appear, including:

- Portable apps
- Some Microsoft Store apps
- Apps without proper Registry entries
- Apps installed in unusual locations
- Apps where the Registry icon path is not the actual launcher path

For safety, the launch action is only shown when the detected path points to a valid launchable file type like  .exe, .lnk, .bat, .cmd, .com




## Version

Current version:

```text
0.1.0
```


## License

This project is licensed under the MIT License.

---
