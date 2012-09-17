#!/bin/bash
# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

set -e
set -u

# Clean up old unison files.
find "$HOME" -name ".unison.*" -print -delete
