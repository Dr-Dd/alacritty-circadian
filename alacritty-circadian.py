#!/usr/bin/python

from ruamel.yaml import YAML
from os.path import expandvars
from pathlib import Path
from datetime import datetime
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
alacritty_circadian_path = list(alacritty_path.glob("circadian.y*ml"))[0]

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


def thread_switch_theme(theme_data, config_data):
    switch_theme(theme_data, config_data)
    exit()


def get_theme_time(theme, alacritty_circadian_data, now_time):
    theme_time_str = theme["time"]
    if theme_time_str in times_of_sun:
        try:
            obs = Observer(
                latitude=alacritty_circadian_data["coordinates"]["latitude"],
                longitude=alacritty_circadian_data["coordinates"]["longitude"])
        except KeyError:
            exit("[ERROR] Coordinates not set")
        except ValueError:
            exit("[ERROR] Unable to convert coordinates, check if latitude " +
                 "and longitude values are set and valid")
        theme_time = sun(obs)[theme_time_str]
    else:
        try:
            theme_time = datetime.strptime(theme["time"], "%H:%M")
        except ValueError:
            exit("[ERROR] Unknown time format \"" + theme["time"] + "\"")
    # Convert datetime to naive if aware and fix YY/MM/DD
    theme_time = theme_time.replace(year=now_time.year, month=now_time.month,
                                    day=now_time.day, tzinfo=None)
    return theme_time


def set_appropriate_theme(alacritty_circadian_data, now_time,
                          theme_folder_path, config_data):
    # nearest list element neighbor to now_time
    diff = -1
    for theme in alacritty_circadian_data["themes"]:
        theme_time = get_theme_time(theme, alacritty_circadian_data, now_time)
        switch_time = now_time.replace(hour=theme_time.hour,
                                       minute=theme_time.minute, second=0,
                                       microsecond=0)
        delta_t = now_time - switch_time
        seconds = delta_t.seconds + 1
        if seconds > 0 and (seconds < diff or diff == -1):
            diff = seconds
            preferred_theme = theme
    theme_path = list(theme_folder_path.glob(preferred_theme["name"]
                                             + ".y*ml"))[0]
    theme_data = yaml.load(theme_path)
    switch_theme(theme_data, config_data)


def set_theme_switch_timers():
    alacritty_circadian_data = yaml.load(alacritty_circadian_path)
    config_data = yaml.load(config_path)
    theme_folder_path = Path(expandvars(
        alacritty_circadian_data["theme-folder"])).expanduser()
    if not theme_folder_path.exists():
        exit("[ERROR] Path " + str(theme_folder_path) + " not found")
    set_appropriate_theme(alacritty_circadian_data, datetime.today(),
                          theme_folder_path, config_data)
    # Hot loop
    while True:
        thread_list = []
        now_time = datetime.today()
        for theme in alacritty_circadian_data["themes"]:
            try:
                curr_theme_path = list(theme_folder_path.glob(theme["name"]
                                                              + ".y*ml"))[0]
            except IndexError:
                exit("[ERROR] Unknown theme \"" + theme["name"]
                     + "\"")
            theme_time = get_theme_time(theme, alacritty_circadian_data,
                                        now_time)
            theme_data = yaml.load(curr_theme_path)
            if theme_time < now_time:
                switch_time = now_time.replace(day=now_time.day+1,
                                               hour=theme_time.hour,
                                               minute=theme_time.minute,
                                               second=0, microsecond=0)
            else:
                switch_time = now_time.replace(hour=theme_time.hour,
                                               minute=theme_time.minute,
                                               second=0, microsecond=0)
            delta_t = switch_time - now_time
            seconds = delta_t.seconds + 1
            t = Timer(seconds, thread_switch_theme, [theme_data, config_data])
            thread_list.append(t)
            t.start()
            # Flush stdout to output to log journal
            print("[LOG] Setting up a timer for " + str(theme["name"])
                  + " at: " + str(switch_time), flush=True)
        for thread in thread_list:
            thread.join()


def main():
    # .yaml takes precedence over .yml
    set_theme_switch_timers()


if __name__ == "__main__":
    main()
