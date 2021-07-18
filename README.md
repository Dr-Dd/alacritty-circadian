# Alacritty Circadian
A time based alacritty theme switcher 

## Installation

```
$ git clone https://github.com/Dr-Dd/alacritty-circadian.git
$ cd alacritty-circadian
$ ./install.sh
```
## Usage

To use it either run the service

```
$ alacritty-circadian.py
```

or enable it on systemd

```
$ systemctl --user enable alacritty-circadian.service
$ systemctl --user start alacritty-circadian.service
```

## Description
The software is just a simple systemd service written in python. It uses the 
ruamel.yaml parser library for manipulating the yaml config files without
garbling comments.

## Inspiration 
Inspired by the excellent 
[circadian.el](https://github.com/guidoschmidt/circadian.el) Emacs package by
[guidoschmidt](https://github.com/guidoschmidt).
