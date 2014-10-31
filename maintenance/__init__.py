#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import concurrent.futures
import configparser
import datetime
import glob
import json
import os
import os.path
import subprocess
import sys
import time

import dateutil.parser
import pkg_resources
import prettytable
import termcolor


__docformat__ = "restructuredtext en"

statusfile = os.path.expanduser("~/.local/share/maintenance.js")

def task(command, attributes, options, data):
    task = os.path.basename(command)
    run = True
    output_list = []

    internet, power = pre_check()

    if (attributes.getboolean('internet') and not internet) or options.f:
        run = False
        output_list.append("Aborting this task. You can use “-f” to run it anyway.")

    taskname = os.path.join('tasks', command)
    if pkg_resources.resource_exists(__name__, taskname):
        syscommand = pkg_resources.resource_filename(__name__, taskname)
    else:
        syscommand = command

    if run and not options.dry:
        try:
            if attributes.getboolean('disk'):
                subprocess.check_call([syscommand], stderr=subprocess.STDOUT)
            else:
                output_list.append(subprocess.check_output([syscommand], stderr=subprocess.STDOUT).decode())
        except subprocess.CalledProcessError as e:
            output_list.append(termcolor.colored("Error in {command}:".format(command=syscommand), 'red'))
            output_list.append(e)
        except OSError as e:
            output_list.append(termcolor.colored("Could not execute {command}.".format(command=syscommand), 'red'))
        else:
            if not task in data:
                data[task] = {}
            data[task]["last"] = str(datetime.datetime.now())

    output = '\n'.join([str(x) for x in output_list])
    output = output.strip()
    if len(output) == 0:
        return termcolor.colored('(none)', 'yellow', attrs=['bold'])
    else:
        return output

def orgoutput(*words):
    termcolor.cprint(' '.join(words), 'white', attrs=['bold'])

def main():
    options = _parse_args()

    taskfile = os.path.expanduser('~/.config/maintenance/tasks.ini')
    tasks = configparser.ConfigParser()
    tasks.read(taskfile)

    data = {}
    if os.path.isfile(statusfile):
        with open(statusfile) as f:
            data = json.load(f)

    calls_disk = []
    calls_nodisk = []
    for command in sorted(tasks.sections()):
        needs = True

        if command in data:
            diff = datetime.datetime.now() - dateutil.parser.parse(data[command]["last"])
            if diff < datetime.timedelta(float(tasks[command]['interval'])):
                needs = False

        if options.local and not tasks[command].getboolean("local"):
            needs = False

        if len(options.tasks) > 0:
            needs = command in options.tasks

        if not needs:
            continue

        if tasks[command].getboolean('disk') and not options.ssd:
            calls_disk.append([command, tasks[command], options, data])
        else:
            calls_nodisk.append([command, tasks[command], options, data])

    orgoutput("Tasks that are done this session:")
    print()
    tasks = sorted([call[0] for call in calls_disk + calls_nodisk])
    for line in ["- {}".format(task) for task in tasks]:
        orgoutput(line)

    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for args in calls_nodisk:
            futures.append([args[0], executor.submit(task, *args)])

        for args in calls_disk:
            print()
            orgoutput('Running', args[0])
            task(*args)
            save_data(data)

        for command, future in futures:
            print()
            orgoutput('Result for', command)
            print(future.result())

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
    parser.add_argument("--ssd", action="store_true", help="Run everything in parallel.")

    return parser.parse_args()

if __name__ == "__main__":
    main()
