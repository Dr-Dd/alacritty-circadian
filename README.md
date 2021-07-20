<p align="center"> 
  <img src="https://user-images.githubusercontent.com/37450282/126343276-6cb3983f-5a45-4cdd-9784-b6d4c00c18d5.png" width="650">
</p>

[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![AUR package](https://repology.org/badge/version-for-repo/aur/aurutils.svg)](https://repology.org/project/aurutils/versions)

# Alacritty Circadian

A cross-platform time based [alacritty](https://github.com/alacritty/alacritty) theme switcher inspired by the excellent
[circadian.el](https://github.com/guidoschmidt/circadian.el) Emacs package by
[guidoschmidt](https://github.com/guidoschmidt), written in Python.

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
manually when installing from pip.

### Git

Either download the release, or just clone the head:

```
$ git clone https://github.com/Dr-Dd/alacritty-circadian.git
$ cd alacritty-circadian
$ ./install.sh
```

## Configuration

The program parses a YAML file named `circadian.yaml` in
`~/.config/alacritty/circadian.yaml`.

It has the following fields:

```yml
# Choose whatever folder you like to store the themes
#
theme-folder: ~/.config/alacritty/themes
#
# Remember to double escape special chars for Windows paths and surround them
# with double quotes if you are using environment variables, e.g.:
#
# theme-folder: "%APPDATA%\\alacritty\\themes"

#
# If you want to use sun phases instead of time, put your coordinates in the
# config file
#
coordinates:
  latitude: 40.684485
  longitude: -74.401383

#
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
#
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

### System Service

The intended way to use the utility is via a system service.
On a systemd Linux this is attainable by adding the following service file to
`~/.config/systemd/user/alacritty-circadian.service`:

```ini
[Unit]
Description=Alacritty automatic theme switch

[Service]
ExecStart=$HOME/.local/bin/alacritty-circadian

[Install]
WantedBy=default.target
```

Installing via the AUR will automate this process for you, leaving you to just
enable the system services.

```
$ systemctl --user enable alacritty-circadian.service
$ systecmtl --user start alacritty-circadian.service
```

#### Windows and MacOS

You can do the same on Windows and MacOS but you'll have to write the system
service yourself.
