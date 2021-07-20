# Alacritty Circadian
[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![AUR package](https://repology.org/badge/version-for-repo/aur/aurutils.svg)](https://repology.org/project/aurutils/versions)

A cross-platform time based alacritty theme switcher inspired by the excellent
[circadian.el](https://github.com/guidoschmidt/circadian.el) Emacs package by
[guidoschmidt](https://github.com/guidoschmidt), written in Python.

## Installation

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
manually when installing from pip

### Git

Either download the release, or just clone the head

```
$ git clone https://github.com/Dr-Dd/alacritty-circadian.git
$ cd alacritty-circadian
$ ./install.sh
```

## Configuration
The program parses a YAML file named `circadian.yaml` in
`~/.config/alacritty/circadian.yaml`.

It has the following fields:
```yaml
# Choose whatever folder you'd like to store themes
#
theme-folder: ~/.config/alacritty/themes
#
# Remember to double escape special chars for Windows paths and surround them
# with double quote if you are using environment variables
#
theme-folder: "%APPDATA%\\alacritty\\themes"

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
# 'time' values can be either be:
#   - an HH:MM time format
#   - one following sun phases:
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

```yaml
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

  ...
  # Bright colors
  bright:
    black:   '0x212121'
    red:     '0xfb007a'
    green:   '0x5fd7af'
    yellow:  '0xf3e430'
    blue:    '0x20bbfc'
    magenta: '0x6855de'
    cyan:    '0x4fb8cc'
    white:   '0xf1f1f1'
```

You can find a comprehensive list of them at  [alacritty-theme](https://github.com/eendroroy/alacritty-theme).

## Usage

To use just run the script from the CLI

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
ExecStart=/usr/local/bin/alacritty-circadian.py

[Install]
WantedBy=default.target
```

#### Windows and MacOS

You can do the same on Windows and MacOS but you'll have to write the system
services yourself.
