#!/bin/sh

echo ""
echo "[!!] Removing all alacritty-circadian files"
echo ""
echo rm /usr/local/bin/alacritty-circadian.py
rm /usr/local/bin/alacritty-circadian.py
echo rm $HOME/.config/systemd/user/alacritty-circadian.service
rm $HOME/.config/systemd/user/alacritty-circadian.service
echo rm -r $HOME/.config/alacritty/alacritty-circadian
rm -r $HOME/.config/alacritty/alacritty-circadian

echo "
[!!] alacritty-circadian has been uninstalled.
[!!]
[!!] Disable the running services if you haven't yet:
[!!]
[!!]   systemctl --user disable alacritty-circadian.service
[!!]   systemctl --user stop alacritty-circadian.service
[!!]
[!!] pip packages haven't been removed. To uninstall ruamel.yaml, simply run:
[!!]
[!!]   pip uninstall ruamel.yaml

"
