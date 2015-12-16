#!/bin/bash

git clone https://github.com/saltstack/salt-pylint.git
cd salt-pylint
sudo python setup.py install

sudo yum -y install python-modernize python-pip

pip install --upgrade pip
sudo pip install --upgrade pep8
sudo pip install --upgrade pylint
sudo pip install --upgrade pep257
sudo pip install --upgrade yapf
