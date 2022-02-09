#!/usr/bin/env python

"""
Small python module for handling the automatic theme switching of alacritty
via explicit time or phases of the sun
"""

# Std imports
import sys
from os.path import expandvars
from pathlib import Path
from datetime import datetime, timezone, timedelta
from threading import Thread, Timer, Lock, get_ident

# dbus
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

# External imports
from ruamel.yaml import YAML
from astral import Observer
from astral.sun import sun

# Create global thread lock
lock = Lock()
# Global thread queue
thread_list = []

# Initialize ruamel
yaml = YAML()
yaml.default_flow_style = False

# Set fixed paths
#
# Platform dependent paths
if sys.platform in ("linux", "darwin", "cygwin"):
    alacritty_path = Path.home() / Path(".config/alacritty")
elif sys.platform == "win32":
    alacritty_path = Path(expandvars("%APPDATA%")) / Path("alacritty")
config_path = list(alacritty_path.glob("alacritty.y*ml"))[0]
try:
    alacritty_circadian_path = list(alacritty_path.glob("circadian.y*ml"))[0]
except IndexError:
    sys.exit("[ERROR] Circadian config file not found")

# Load yaml parts
config_data = yaml.load(config_path)
alacritty_circadian_data = yaml.load(alacritty_circadian_path)
theme_folder_path = Path(expandvars(
    alacritty_circadian_data["theme-folder"])).expanduser()
if not theme_folder_path.exists():
    sys.exit("[ERROR] Path " + str(theme_folder_path) + " not found")

times_of_sun = {
    "dawn",
    "sunrise",
    "noon",
    "sunset",
    "dusk",
}

def switch_theme(theme_data):
    """
    Put theme_data in alacritty's config_data.
    """
    config_data["colors"] = theme_data["colors"]
    yaml.dump(config_data, config_path)


def thread_switch_theme(theme_data):
    """
    Wrapper function to make a thread run switch_theme and exit gracefully.
    See switch_theme for more info.
    """
    # Thread locking to prevent race conditions
    with lock:
        switch_theme(theme_data)
    print("[LOG] Thread timer-" + str(get_ident()) + " has finished execution, exiting")
    sys.exit()


def get_theme_time(theme, now_time):
    """
    Get the time associated with theme, either from a times_of_sun
    String or an HH:MM timestamp.
    """
    theme_time_str = theme["time"]
    if theme_time_str in times_of_sun:
        try:
            obs = Observer(
                latitude = alacritty_circadian_data["coordinates"]["latitude"],
                longitude = alacritty_circadian_data["coordinates"]["longitude"])
        except KeyError:
            sys.exit("[ERROR] Coordinates not set")
        except ValueError:
            sys.exit("[ERROR] Unable to convert coordinates, check if " +
                     "latitude and longitude values are set and valid")
        theme_time = sun(obs)[theme_time_str]
    else:
        try:
            theme_time = datetime.strptime(theme["time"], "%H:%M")
        except ValueError:
            sys.exit("[ERROR] Unknown time format \"" + theme["time"] + "\"")
    theme_time = theme_time.replace(year=now_time.year, month=now_time.month,
                                    day=now_time.day)
    # "Convert" to localtime (datetime doesn't convert since the time is the
    # same as the localtime, so actually we just make the naive timestamp
    # offset aware)
    theme_time = theme_time.astimezone(tz=None)
    # Convert to UTC
    theme_time = theme_time.astimezone(tz=timezone.utc)
    return theme_time


def set_appropriate_theme(now_time):
    """
    Get the nearest neighbor themes list element to now_time and set it as the
    current theme.
    """
    # nearest list element neighbor to now_time
    diff = -1
    try:
        theme_alist = alacritty_circadian_data["themes"]
    except KeyError:
        sys.exit("[ERROR] Circadian config theme section not found")
    if isinstance(theme_alist, type(None)):
        sys.exit("[ERROR] No themes specified in circadian config")
    for theme in theme_alist:
        theme_time = get_theme_time(theme, now_time)
        switch_time = now_time.replace(hour=theme_time.hour,
                                       minute=theme_time.minute, second=0,
                                       microsecond=0)
        delta_t = now_time - switch_time
        seconds = delta_t.seconds + 1
        if seconds > 0 and (seconds < diff or diff == -1):
            diff = seconds
            preferred_theme = theme
    try:
        theme_path = list(theme_folder_path.glob(preferred_theme["name"]
                                                 + ".y*ml"))[0]
    except IndexError:
        sys.exit("[ERROR] Unknown theme \"" + preferred_theme["name"]
                 + "\"")
    theme_data = yaml.load(theme_path)
    switch_theme(theme_data)


def set_theme_switch_timers():
    """
    Set a suitable theme and start/restart thread timers
    for theme switching. The main daemon loop.
    """
    set_appropriate_theme(datetime.now(timezone.utc))
    # Hot loop
    while True:
        now_time = datetime.now(timezone.utc)
        for theme in alacritty_circadian_data["themes"]:
            try:
                curr_theme_path = list(theme_folder_path.glob(theme["name"]
                                                              + ".y*ml"))[0]
            except IndexError:
                sys.exit("[ERROR] Unknown theme \"" + theme["name"]
                         + "\"")
            theme_time = get_theme_time(theme, now_time)
            theme_data = yaml.load(curr_theme_path)
            if theme_time < now_time:
                # Set Date to today
                switch_time = now_time.replace(day=now_time.day,
                                               hour=theme_time.hour,
                                               minute=theme_time.minute,
                                               second=0, microsecond=0)
                # Add one day without overflowing current month
                switch_time = switch_time + timedelta(days=1)
            else:
                switch_time = now_time.replace(hour=theme_time.hour,
                                               minute=theme_time.minute,
                                               second=0, microsecond=0)
            delta_t = switch_time - now_time
            seconds = delta_t.seconds + 1
            timer_thread = Timer(seconds, thread_switch_theme, [theme_data])
            thread_list.append(timer_thread)
            timer_thread.start()
            # Flush stdout to output to log journal
            local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
            print("[LOG] Setting up timer-" + str(timer_thread.ident) + " for " + str(theme["name"])
                  + " at: " + str(switch_time.astimezone(local_timezone)), flush=True)
        for thread in thread_list:
            thread.join()
        # All threads have finished, flush
        thread_list.clear()

def handle_wakeup_callback(going_to_sleep_flag):
    if going_to_sleep_flag == 0:
        print("[LOG] System has just woken up from hibernate/sleep, refreshing threads")
        for thread in thread_list:
            thread.cancel()
        set_appropriate_theme(datetime.now(timezone.utc))

def enable_dbus_main_loop():
    DBusGMainLoop(set_as_default=True)
    system_bus = dbus.SystemBus()
    dbus.mainloop.glib.threads_init()
    system_bus.add_signal_receiver(
        handle_wakeup_callback,
        'PrepareForSleep',
        'org.freedesktop.login1.Manager',
        'org.freedesktop.login1'
        )
    loop = GLib.MainLoop()
    loop.run()

def main():
    """
    Entry point
    """
    print("[LOG] Starting dbus main loop")
    dbus_thread = Thread(target=enable_dbus_main_loop)
    dbus_thread.start()
    # Set flag to true for first run
    set_theme_switch_timers()

if __name__ == "__main__":
    main()
