#!/bin/sh

set -e

rm /usr/local/bin/alacritty-circadian.py > /dev/null 2>&1
rm $HOME/.config/systemd/user/alacritty-circadian.service > /dev/null 2>&1
rm -rf $HOME/.config/alacritty/alacritty-circadian > /dev/null 2>&1
rm $HOME/.config/alacritty/alacritty-circadian/circadian.yaml > /dev/null 2>&1

echo "

alacritty-circadian has been uninstalled.

Disable the running services if you haven't yet:

  systemctl --user disable alacritty-circadian.service
  systemctl --user stop alacritty-circadian.service

pip packages haven't been removed. To uninstall ruamel.yaml, simply run:

  pip uninstall ruamel.yaml

"
