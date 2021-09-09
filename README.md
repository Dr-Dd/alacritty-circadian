<p align="center">
  <img src="https://user-images.githubusercontent.com/37450282/126490791-43feaa96-564f-4ef4-bcc3-159f801f7c41.png" width="600">
</p>

[![PyPI version](https://badge.fury.io/py/alacritty-circadian.svg)](https://badge.fury.io/py/alacèritty-circadian)
![AUR version](https://img.shields.io/aur/version/alacritty-circadian)

# Alacritty Circadian

A cross-platform time based [alacritty](https://github.com/alacritty/alacritty) theme switcher inspired by the excellent
[circadian.el](https://github.com/guidoschmidt/circadian.el) Emacs package by
[guidoschmidt](https://github.com/guidoschmidt), written in Python.

* [Installation](#installation)
   * [Pip](#pip)
   * [AUR](#aur)
   * [Git](#git)
* [Configuration](#configuration)
   * [Theme format](#theme-format)
* [Usage](#usage)
   * [System Services](#system-services)
      * [Linux (Systemd)](#linux-systemd)
      * [Windows (shell:startup)](#windows-shellstartup)
      * [MacOS (launchd)](#macos-launchd)
* [Known Problems](#known-problems)
   * [Ruamel Hibernation WakeUp](#ruamel-hibernation-wakeup) 

## Installation

The package can be installed from multiple sources (other than Git releases):

### Pip

```
$ pip install alacritty-circadian 
```

### AUR

Using the yay AUR wrapper:

```
$ yay alacritty-circadian
```

This will also install the required system services, which have to be added
manually when installing from pip. Read below for more info.

### Git

Either download the release, or just clone the head. Then, cd into the 
directory and install the package locally.

```
$ python -m build
$ pip install .
```

You'll find some example config files in `docs/`

Note: the package has been made with `setuptools` and `build`

## Configuration

The program parses a YAML file named `circadian.yaml` in
`~/.config/alacritty/circadian.yaml`.

It has the following fields:

```yml
#
# Choose whatever folder you like to store the themes
#
# If you are a *NIX user:
theme-folder: ~/.config/alacritty/themes
#
# If you are a WINDOWS user:
# Remember to escape special chars for Windows paths and surround them
# with double quotes if you are using environment variables, e.g.:
theme-folder: "%APPDATA%\\alacritty\\themes"

#
# If you want to use sun phases instead of time, put your coordinates in the
# config file:
coordinates:
  latitude: 40.684485
  longitude: -74.401383

# Themes are an associative array of the following format.
# Theme names MUST NOT use file extensions.
#
# 'time' values can either be:
#   - an HH:MM time format
#   - one of the following sun phases:
#       * dawn
#       * sunrise
#       * noon
#       * sunset
#       * dusk
themes:
  - time: sunset
    name: tokyo-night
  - time: 7:00
    name: pencil-light
```

### Theme format

All themes should use the format commonly used for alacritty themes:

```yml
# Colors
colors:
  # Default Colors
  primary:
    background: '0xf1f1f1'
    foreground: '0x424242'
  # Normal colors
  normal:
    black:   '0x212121'
    ...

    # Other alacritty compatible fields
```

You can find a comprehensive list of them at [alacritty-theme](https://github.com/eendroroy/alacritty-theme).

## Usage

To start the service just run the CLI script:

```
$ alacritty-circadian
```

### System Services

The intended way to use the utility is via a system service.

#### Linux (Systemd)

On a systemd init Linux this is attainable by adding the following service file
to `~/.config/systemd/user/alacritty-circadian.service`:

```ini
[Unit]
Description=Alacritty automatic theme switch

[Service]
ExecStart=alacritty-circadian

[Install]
WantedBy=default.target
```

Installing via the AUR will automate this process for you, leaving you to just
enable the system services.

```
$ systemctl --user enable alacritty-circadian.service
$ systecmtl --user start alacritty-circadian.service
```

#### Windows (shell:startup)

Included in the releases are `.exe` binaries to use as a startup
application, just download one and add a shortcut to it in the `Startup` Windows
folder (`Win + R 'shell:startup'` to open it). After that you'll be able to see
it in your task manager.

#### MacOS (launchd)

It should be quite easy to add a `launchd` service in `~/Library/LaunchAgents`
although you'll have to provide your own service file (i don't own a Mac).
