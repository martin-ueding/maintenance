#!/bin/bash
# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

set -e
set -u

clamscan -r "$HOME" &> "$HOME/TODO/Virus Scan $(date --rfc-3339=seconds).log"
