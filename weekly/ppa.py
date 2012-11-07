#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import argparse
import apt
import os
import subprocess

import colorcodes

__docformat__ = "restructuredtext en"

_c = colorcodes.Colorcodes()

_packages = [

"a4-scan",
"copyright-updater",
"email-rename",
"git-changelog",
"git-tarball",
"jscribble",
"latex-edit",
"legacy-file-formats",
"mp3-packer",
"multiimage",
"pdflatex-multifont",
"project-ubernahme",
"risk-auto-dice",
"think-rotate",
"unwrap-pdf-to-jpeg",
"van-allen-sim-3d",
"vim-headings",
"xournal-page-count",

]

def main():
    options = _parse_args()

    basedir = os.path.expanduser("~/Packaging")

    for package in _packages:
        os.chdir(basedir)

        files = [x for x in os.listdir(os.path.join(basedir, package)) if os.path.isfile(os.path.join(basedir, package, x)) and x.endswith(".dsc")]

        if len(files) == 0:
            continue

        files.sort(cmp=apt.VersionCompare)

        latest_dsc = files[-1]

        files = [x for x in os.listdir(os.path.join(basedir, package)) if os.path.isdir(os.path.join(basedir, package, x)) and not x.endswith(".orig")]

        if len(files) == 0:
            continue

        files.sort(cmp=apt.VersionCompare)

        latest_dir = files[-1]

        print(_c.cyan + latest_dir + _c.reset)

        changes = latest_dsc[:-4]+"_source.changes"

        if os.path.isfile(os.path.join(basedir, package, changes)):
            print(_c.green + "Build exists" + _c.reset)
        else:
            try:
                os.chdir(os.path.join(basedir, package, latest_dir))
                subprocess.check_call(["debuild", "-S"])
            except subprocess.CalledProcessError as e:
                print(e)
                print(_c.red + "Build failed." + _c.reset)
        try:
            os.chdir(os.path.join(basedir, package))
            subprocess.check_call(["dput", "stable", changes])
        except subprocess.CalledProcessError as e:
            print(e)
            print(_c.red + "Upload failed." + _c.reset)

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    #parser.add_argument("args", metavar="N", type=str, nargs="*", help="Positional arguments.")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()

if __name__ == "__main__":
    main()
