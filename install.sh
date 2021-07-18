#!/bin/sh

set -e

echo ""
echo "[!!] Installing ruamel.yaml"
echo ""
echo pip install -U pip setuptools wheel
pip install -U pip setuptools wheel
echo pip install ruamel.yaml
pip install ruamel.yaml
echo ""
echo "[!!] Installing executable scripts, config files and services"
echo ""
echo chmod +x alacritty-circadian.py
chmod +x alacritty-circadian.py
echo cp alacritty-circadian.py /usr/local/bin
cp alacritty-circadian.py /usr/local/bin
echo cp alacritty-circadian.service $HOME/.config/systemd/user/
cp alacritty-circadian.service $HOME/.config/systemd/user/
echo mkdir -p $HOME/.config/alacritty/alacritty-circadian
mkdir -p $HOME/.config/alacritty/alacritty-circadian
echo cp circadian.yaml $HOME/.config/alacritty/alacritty-circadian/
cp circadian.yaml $HOME/.config/alacritty/alacritty-circadian/

echo "
[!!] alacritty-circadian has been installed.
[!!]
[!!] Edit the .yaml file in
[!!] $HOME/.config/alacritty/alacritty-circadian/circadian.yaml, then
[!!] start/enable its systemd user service:
[!!]
[!!]   systemctl --user enable alacritty-circadian.service
[!!]   systemctl --user start alacritty-circadian.service

"
