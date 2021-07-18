#!/bin/sh

set -e

blue=`tput setaf 4`
reset=`tput sgr0`

echo ""
echo "${blue}[!!]${reset} Installing python dependencies"
echo ""
echo pip install -U pip setuptools wheel
pip install -U pip setuptools wheel
echo pip install ruamel.yaml astral
pip install ruamel.yaml astral
echo ""
echo "${blue}[!!]${reset} Installing executable scripts, config files and services"
echo ""
echo chmod +x alacritty-circadian.py
chmod +x alacritty-circadian.py
echo cp alacritty-circadian.py /usr/local/bin/
cp alacritty-circadian.py /usr/local/bin/
echo cp alacritty-circadian.service $HOME/.config/systemd/user/
cp alacritty-circadian.service $HOME/.config/systemd/user/
echo systemctl --user daemon-reload
systemctl --user daemon-reload
echo cp circadian.y*ml $HOME/.config/alacritty/
cp circadian.y*ml $HOME/.config/alacritty/

echo "
${blue}[!!]${reset} alacritty-circadian has been installed.
${blue}[!!]${reset}
${blue}[!!]${reset} Edit the .yaml file in
${blue}[!!]${reset} $HOME/.config/alacritty/circadian.y*ml, then
${blue}[!!]${reset} start/enable its systemd user service:
${blue}[!!]${reset}
${blue}[!!]${reset}   systemctl --user enable alacritty-circadian.service
${blue}[!!]${reset}   systemctl --user start alacritty-circadian.service

"
