#!/usr/bin/python

from ruamel.yaml import YAML
from os.path import expandvars
from pathlib import Path
from datetime import datetime, timedelta
from threading import Timer

# Initialize ruamel
yaml = YAML()
yaml.default_flow_style = False

# Set fixed paths
alacritty_path = Path.home() / Path(".config/alacritty")
config_path = list(alacritty_path.glob("alacritty.y*ml"))[0]
switch_path = list((alacritty_path / Path("alacritty-theme-switch")).glob("theme-switch.y*ml"))[0]

def switch_theme(theme_data, config_data):
    # No need for truncating
    config_data["colors"] = theme_data["colors"]
    yaml.dump(config_data, config_path)

def set_appropriate_theme(switch_data, today_time, theme_folder_path):
    # nearest list element neighbor to today_time
    diff = -1
    for theme in switch_data["themes"]:
        theme_time = datetime.strptime(theme["time"],"%H:%M")
        switch_time = today_time.replace(hour = theme_time.hour, minute = theme_time.minute, second = 0, microsecond = 0)
        delta_t =  today_time - switch_time
        seconds = delta_t.seconds + 1
        if seconds > 0 and (seconds < diff or diff == -1):
            diff = seconds
            preferred_theme = theme
        theme_data = list(theme_folder_path.glob(preferred_theme["name"] + ".y*ml"))[0]
        switch_theme(yaml.load(theme_data), yaml.load(config_path))

def set_theme_switch_timers():
    switch_data = yaml.load(switch_path)
    config_data = yaml.load(config_path)
    theme_folder_path = Path(expandvars(switch_data["theme-folder"])).expanduser()
    today_time = datetime.today()
    for theme in switch_data["themes"]:
        curr_theme_path = list(theme_folder_path.glob(theme["name"] + ".y*ml"))[0]
        theme_data = yaml.load(curr_theme_path)
        theme_time = datetime.strptime(theme["time"],"%H:%M")
        switch_time = today_time.replace(hour = theme_time.hour, minute = theme_time.minute, second = 0, microsecond = 0)
        delta_t = switch_time - today_time
        seconds = delta_t.seconds + 1
        t = Timer(seconds, switch_theme, [theme_data, config_data])
        t.start()
    set_appropriate_theme(switch_data, today_time, theme_folder_path)
    # Recurse @ 00:00
    midnight = today_time.replace(day = today_time.day + 1, hour = 0, minute = 0, second = 0, microsecond = 0)
    delta_t = midnight - today_time
    seconds = delta_t.seconds + 1
    t = Timer(seconds, set_theme_switch_timers, [])
    t.start()

def main():
    # .yaml takes precedence over .yml
    set_theme_switch_timers()

if __name__ == "__main__":
    main()
