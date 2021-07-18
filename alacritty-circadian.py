#!/usr/bin/python

from ruamel.yaml import YAML
from os.path import expandvars
from pathlib import Path
from datetime import datetime, timedelta
from threading import Timer
from sys import exit
from astral import Observer
from astral.sun import sun

# Initialize ruamel
yaml = YAML()
yaml.default_flow_style = False

# Set fixed paths
alacritty_path = Path.home() / Path(".config/alacritty")
config_path = list(alacritty_path.glob("alacritty.y*ml"))[0]
switch_path = list(alacritty_path.glob("circadian.y*ml"))[0]

times_of_sun = {
    "dawn",
    "sunrise",
    "noon",
    "sunset",
    "dusk",
}

def switch_theme(theme_data, config_data):
    # No need for truncating
    config_data["colors"] = theme_data["colors"]
    yaml.dump(config_data, config_path)

def get_theme_time(theme, switch_data):
    theme_time_str = theme["time"]
    if theme_time_str in times_of_sun:
        try:
            obs = Observer(latitude = switch_data["coordinates"]["latitude"],
                           longitude = switch_data["coordinates"]["longitude"])
        except KeyError:
            exit("[ERROR] Coordinates not set")
        except ValueError:
            exit("[ERROR] Unable to convert coordinates, check if latitude " +
                 "and longitude values are set and valid")
        theme_time = sun(obs)[theme_time_str]
    else:
        try: theme_time = datetime.strptime(theme["time"],"%H:%M")
        except: exit("[ERROR] Unknown time format \"" + theme["time"] + "\"")
    return theme_time

def set_appropriate_theme(switch_data, today_time, theme_folder_path):
    # nearest list element neighbor to today_time
    diff = -1
    for theme in switch_data["themes"]:
        theme_time = get_theme_time(theme, switch_data)
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
    if not theme_folder_path.exists():
        exit("[ERROR] Path " + str(theme_folder_path) + " not found")
    today_time = datetime.today()
    for theme in switch_data["themes"]:
        try:
            curr_theme_path = list(theme_folder_path.glob(theme["name"] + ".y*ml"))[0]
        except:
            exit("[ERROR] Unknown theme \"" + theme["name"] +"\"")
        theme_time = get_theme_time(theme, switch_data)
        theme_data = yaml.load(curr_theme_path)
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
