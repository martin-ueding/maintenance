#!/bin/bash
# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

set -e
set -u

shopt -s globstar

for git_dir in "$HOME/Branches/"**/.git/
do
	pushd "$git_dir"
	pushd ..
	echo "---> Cleaning $(pwd) <---"
	git gc
	popd
	popd
done
