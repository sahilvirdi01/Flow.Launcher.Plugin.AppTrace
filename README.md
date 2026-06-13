# App Trace 

Apptrace helps you quickly find where windows applications are installed

Default trigger keyword: `where`

## Description

Type an app name using the `where` keyword, and AppTrace will search installed applications and developer tools from the Windows Registry and PATH.

Example:

```text
where flow
```

AppTrace will show matching apps. Select an app to open its install folder, or use the context menu for extra actions like launching the app or copying paths.


## Usage


```text
where python
where code
where brave
```

Type a query after the `where` keyword:

```text
where <app name>
```

Use the result context menu for more actions:

```text
- Open install folder
- Launch app
- Copy executable path
- Copy install folder path
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

Use Plugin Store, or install manually:

```text
pm install https://github.com/sahilvirdi01/Flow.Launcher.Plugin.AppTrace/releases/download/v0.1.0/AppTrace-v0.1.0.zip
```

---

This project is licensed under the MIT License.
