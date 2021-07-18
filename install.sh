#!/bin/sh

set -e

pip install -U pip setuptools wheel > /dev/null 2>&1
pip install ruamel.yaml > /dev/null 2>&1
chmod +x alacritty-circadian.py > /dev/null 2>&1
mv alacritty-circadian.py /usr/local/bin > /dev/null 2>&1
mv alacritty-circadian.service $HOME/.config/systemd/user/ > /dev/null 2>&1
mkdir $HOME/.config/alacritty/alacritty-circadian
mv circadian.yaml $HOME/.config/alacritty/alacritty-circadian/ > /dev/null 2>&1

echo "

alacritty-circadian has been installed.

Edit the .yaml file in $HOME/.config/alacritty/alacritty-circadian/circadian.yaml, then Start/enable its systemd user service:

  systemd --user enable alacritty-circadian.service
  systemd --user start alacritty-circadian.service"
