#!/usr/bin/env bash
set -e -x
sudo apt-get install python3 python-dev python3-dev
git clone git@gitlab.abgf.gov.br:e-sce/odoo12.git .
virtualenv -p python3 .
bin/pip install -U zc.buildout pip
bin/buildout

