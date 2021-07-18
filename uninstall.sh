#!/bin/sh

blue=`tput setaf 4`
reset=`tput sgr0`

echo ""
echo "${blue}[!!]${reset} Removing all alacritty-circadian files"
echo ""
echo rm /usr/local/bin/alacritty-circadian.py
rm /usr/local/bin/alacritty-circadian.py
echo rm $HOME/.config/systemd/user/alacritty-circadian.service
rm $HOME/.config/systemd/user/alacritty-circadian.service
echo rm $HOME/.config/alacritty/circadian.y*ml
rm  $HOME/.config/alacritty/circadian.y*ml

echo "
${blue}[!!]${reset} alacritty-circadian has been uninstalled.
${blue}[!!]${reset}
${blue}[!!]${reset} Disable the running services if you haven't yet:
${blue}[!!]${reset}
${blue}[!!]${reset}   systemctl --user disable alacritty-circadian.service
${blue}[!!]${reset}   systemctl --user stop alacritty-circadian.service
${blue}[!!]${reset}
${blue}[!!]${reset} pip packages haven't been removed. To uninstall ruamel.yaml, simply run:
${blue}[!!]${reset}
${blue}[!!]${reset}   pip uninstall ruamel.yaml astral

"
