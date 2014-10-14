#!/usr/bin/env bash

# Core dependencies
sudo apt-get install -y curl git-core build-essential

# Install python dev stuff
#TODO maybe pin version and/or use deadsnakes?
sudo apt-get install -y python-dev python-dbg

# Lib dependencies
sudo apt-get install -y python-dev libxml2-dev libxslt1-dev zlib1g-dev libpng12-dev libjpeg-dev
