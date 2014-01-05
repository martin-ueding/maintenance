#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import concurrent.futures
import datetime
import dateutil.parser
import glob
import json
import os
import os.path
import pkg_resources
import prettytable
import subprocess
import sys
import time
import yaml

import colorcodes

__docformat__ = "restructuredtext en"

_c = colorcodes.Colorcodes()

statusfile = os.path.expanduser("~/.local/share/maintenance.js")

def task(command, attributes, options, data):
    task = os.path.basename(command)
    run = True

    internet, power = pre_check()

    if (attributes['internet'] and not internet) or options.f:
        run = False
        print("Aborting this task. You can use “-f” to run it anyway.")

    taskname = os.path.join('tasks', command)
    if pkg_resources.resource_exists(__name__, taskname):
        syscommand = pkg_resources.resource_filename(__name__, taskname)
    else:
        syscommand = command

    output = None

    if run and not options.dry:
        try:
            if attributes['disk']:
                subprocess.check_call([syscommand], stderr=subprocess.STDOUT)
            else:
                output = subprocess.check_output([syscommand], stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as e:
            print(_c.red + "Error in {command}:".format(command=syscommand) + _c.reset)
            print(e)
            if attributes['disk']:
                print_lock.release()
        except OSError as e:
            print(_c.red + "Could not execute {command}.".format(command=syscommand) + _c.reset)
            if attributes['disk']:
                print_lock.release()
        else:
            if not task in data:
                data[task] = {}
            data[task]["last"] = str(datetime.datetime.now())

    return output

def main():
    options = _parse_args()

    taskfile = 'tasks.yaml'
    tasks = {}
    tasks = yaml.load(pkg_resources.resource_stream(__name__, taskfile))

    data = {}
    if os.path.isfile(statusfile):
        with open(statusfile) as f:
            data = json.load(f)

    calls_disk = []
    calls_nodisk = []
    for command, attributes in sorted(tasks.items()):
        needs = True

        if command in data:
            diff = datetime.datetime.now() - dateutil.parser.parse(data[command]["last"])
            if diff < datetime.timedelta(attributes['interval']):
                needs = False

        if options.local and not attributes["local"]:
            needs = False

        if len(options.tasks) > 0:
            needs = command in options.tasks

        if not needs:
            continue

        if attributes['disk']:
            calls_disk.append([command, attributes, options, data])
        else:
            calls_nodisk.append([command, attributes, options, data])

    print("Tasks that are done this session:")
    print()
    tasks = sorted([call[0] for call in calls_disk + calls_nodisk])
    for line in ["- {}".format(task) for task in tasks]:
        print(line)
    print()

    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for args in calls_nodisk:
            print('Scheduling', args[0])
            futures.append([args[0], executor.submit(task, *args)])

        print()

        # Start one thread that uses the disk and wait for that.
        for args in calls_disk:
            print('Running', args[0])
            task(*args)
            save_data(data)

        print()

        for command, future in futures:
            print(future.result())
            print()

        save_data(data)

def save_data(data):
    """
    Saves all the data.
    """
    with open(statusfile, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def pre_check():
    """
    Checks whether internet connection and power are attached.

    :return: Whether internet and power are connected.
    :rtype: tuple
    """
    powered = True

    powerfile = "/sys/class/power_supply/AC/online"
    if os.path.isfile(powerfile):
        with open(powerfile) as f:
            powered = int(f.read()) != 0

    connected = False

    try:
        subprocess.check_output(["ping", "-c", "1", "-w", "2",
                                 "martin-ueding.de"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pass
    else:
        connected = True

    return connected, powered

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="Runs periodic tasks and logs that they are done.")
    parser.add_argument("tasks", metavar="task", type=str, nargs="*", help="Task to run.")
    parser.add_argument("-n", action="store_true", dest="dry", default=False, help="Dry run, only show what would be done.")
    parser.add_argument("-f", action="store_true", help="Run even without power and internet connection.")
    parser.add_argument("--local", action="store_true", help="Run only local tasks.")

    return parser.parse_args()

if __name__ == "__main__":
    main()
