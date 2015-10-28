#!/bin/bash

git clone https://github.com/saltstack/salt-pylint.git
cd salt-pylint
sudo python setup.py install

sudo yum install python-modernize python-pip python-pep8 pytho-pylint python-pep257

sudo pip install --upgrade yapf
