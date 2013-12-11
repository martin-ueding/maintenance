#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

import argparse
import datetime
import dateutil.parser
import glob
import json
import os
import os.path
import prettytable
import subprocess
import sys
import threading
import time
import yaml

import colorcodes

__docformat__ = "restructuredtext en"

_c = colorcodes.Colorcodes()

statusfile = os.path.expanduser("~/.local/share/maintenance.js")
save_data_lock = threading.Lock()
print_lock = threading.Lock()

all_threads = []

def print_block(lines):
    with print_lock:
        print()
        for line in lines:
            print(line)

class Task(threading.Thread):
    def __init__(self, command, attributes, options, data):
        """
        :param command: Command to run.
        :type command: str
        :param attributes: Attributes of this task.
        :type attributes: dict
        :param dry: Whether to only print command.
        :type dry: bool
        """
        super().__init__()
        self.command = command
        self.attributes = attributes
        self.options = options
        self.data = data
        self.done = False
        self.output = []

    def print(self, line):
        if self.attributes['disk']:
            print(line)
        else:
            self.output.append(line)

    def flush(self):
        if len(self.output) == 0:
            return

        with print_lock:
            for line in self.output:
                print(line)

    def run(self):
        """
        Performs a single task.
        """
        task = os.path.basename(self.command)
        run = True

        if self.attributes['disk']:
            print_lock.acquire()

        self.print(_c.bold + task + _c.reset)
        self.print(_c.bold + ("="*len(task)) + _c.reset)
        self.print("")

        internet, power = pre_check()

        if (self.attributes['internet'] and not internet) or self.options.f:
            run = False
            self.print("Aborting this task. You can use “-f” to run it anyway.")

        if run and not self.options.dry:
            syscommand = os.path.join("/usr/lib/maintenance/tasks",
                                      self.command)
            # If this is a disk heavy task, show the output right away.
            try:
                if self.attributes['disk']:
                    subprocess.check_call([syscommand])
                else:
                    output = subprocess.check_output([syscommand], stderr=subprocess.STDOUT).decode()
                    if len(output.strip()) == 0:
                        self.print("(no output)")
                    else:
                        self.print(output)
            except subprocess.CalledProcessError as e:
                self.print(_c.red + "Error in {command}:".format(command=syscommand) + _c.reset)
                self.print(e)
                if self.attributes['disk']:
                    print_lock.release()
            except OSError as e:
                self.print(_c.red + "Could not execute {command}.".format(command=syscommand) + _c.reset)
                if self.attributes['disk']:
                    print_lock.release()
            else:
                if save_data_lock.acquire():
                    if not task in self.data:
                        self.data[task] = {}
                    self.data[task]["last"] = str(datetime.datetime.now())
                    save_data(self.data)
                    save_data_lock.release()
                else:
                    self.print("Error locking!")

        self.done = True

        self.print("")

        if self.attributes['disk']:
            print_running_tasks(without=self)
            print_lock.release()
        else:
            self.flush()

def print_tasks(tasks):
    fields = list(list(tasks.items())[0][1].keys())
    table = prettytable.PrettyTable(['command'] + fields)
    table.align = 'l'
    table.align['interval'] = 'r'
    for command, task in sorted(tasks.items()):
        table.add_row([command] + list(task.values()))

    print(table)

def print_running_tasks(without=None):
    alive = []
    waiting = []

    for thread in all_threads:
        if thread.is_alive() and thread is not without:
            alive.append(thread.command)
        elif not thread.done:
            waiting.append(thread.command)

    lines = []

    if len(alive) > 0:
        lines.append(_c.green + "Running: " + ", ".join(sorted(alive)) + _c.reset)
    if len(waiting) > 0:
        lines.append(_c.orange + "Waiting: " + ", ".join(sorted(waiting)) + _c.reset)

    output = "\n".join(lines)
    print(output)
    print()

def main():
    options = _parse_args()

    taskfile = '/etc/maintenance/tasks.js'
    tasks = {}
    with open(taskfile) as f:
        tasks = yaml.load(f)

    data = {}
    if os.path.isfile(statusfile):
        with open(statusfile) as f:
            data = json.load(f)

    threads_disk = []
    threads_nodisk = []
    for command, attributes in tasks.items():
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

        thread = Task(command, attributes, options, data) 
        if attributes['disk']:
            threads_disk.append(thread)
        else:
            threads_nodisk.append(thread)

    print("Tasks that are done this session:")
    print()
    tasks = sorted([thread.command for thread in threads_disk + threads_nodisk])
    for line in ["- {}".format(task) for task in tasks]:
        print(line)
    print()

    global all_threads
    all_threads = threads_disk + threads_nodisk

    # Start all the threads that do not use the disk very much.
    for thread in threads_nodisk:
        thread.start()

    print_running_tasks()

    # Start one thread that uses the disk and wait for that.
    for thread in threads_disk:
        thread.start()
        thread.join()

    # Wait for all other threads. I guess that they will have finished by then
    # anyway.
    for thread in threads_nodisk:
        thread.join()

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
