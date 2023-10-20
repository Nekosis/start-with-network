#!/usr/bin/env python
# start-with-network - Start a configured set of applications when the network is available

import configparser
import os
import subprocess

import requests
from xdg.BaseDirectory import xdg_config_home


def main():
    config_file_path = os.path.join(
        xdg_config_home, "start-with-network/programs-list.conf"
    )

    if not os.path.isfile(config_file_path):
        raise Exception(
            f"No configuration file found. Please create a config file at {config_file_path}"
        )

    config = configparser.ConfigParser()
    config.read(config_file_path)

    if not config.sections():
        raise Exception(
            f"No programs found in the configuration file. Please add programs to the config file at {config_file_path}"
        )

    while True:
        if network_available():
            print("Network available.")
            break
        else:
            print("Network unavailable. Retrying...")

    for section in config.sections():
        program = config.get(section, "command")
        try:
            if program.split(" ", 1)[0] == "element-desktop":
                program_pgrep = "element"
            else:
                program_pgrep = program.split(" ", 1)[0]
            subprocess.check_output(["pgrep", "-fi", program_pgrep])
        except subprocess.CalledProcessError:
            print(f"Executing {program}...")
            subprocess.Popen(program, shell=True)
        else:
            print(f"{program} already running. skipping...")


def network_available(url="https://1.1.1.1"):
    try:
        requests.get(url)
        return True
    except requests.ConnectionError:
        return False


if __name__ == "__main__":
    main()
