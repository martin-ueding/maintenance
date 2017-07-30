.. Copyright © 2013-2014, 2017 Martin Ueding <dev@martin-ueding.de>

###########
maintenance
###########

This is a collection of maintenance scripts. There a ``maintenance`` script
that runs the task scripts and save the execution date into a JSON file. That
way, the tasks are done periodically.

Cron is the canonical thing to use for periodically tasks. The problem with
cron is that it does not let me choose when to run the tasks. I often have
limited battery capacity or no internet connection. Running an online backup
does not make sense then. With this script, I can choose when to run the tasks.
And I can abort it when I run out of time and continue at some later point.

Installation
============

::

    make
    sudo make install

Depenencies
===========

- bash
- python3
- python3-setuptools
- python3-termcolor
- python3-yaml
