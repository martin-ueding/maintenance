#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

import argparse
import distutils.version
import os

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

    basedir = os.path.expanduser("~/Branches")

    for package in _packages:
        files = os.listdir(os.path.join(basedir, package))

        files.sort(key=distutils.version.StrictVersion)

        print(files)
        


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
