#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

import argparse
import json
import yaml

__docformat__ = "restructuredtext en"

def main():
    options = _parse_args()

    with open(options.js) as f:
        data = json.load(f)

    with open(options.yaml, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="Converts a given JSON file into a YAML file.")
    parser.add_argument("js", help="Input JSON file")
    parser.add_argument("yaml", help="Input YAML file")

    return parser.parse_args()


if __name__ == "__main__":
    main()
