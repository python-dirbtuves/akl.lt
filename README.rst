AKL web site project.

This repository is move from https://launchpad.net/akl-web-site .

Requirements
============

sudo apt-get install curl git-core build-essential python-dev libxml2-dev libxslt1-dev zlib1g-dev libpng12-dev libjpeg-dev exuberant-ctags nfs-kernel-server nfs-common

Vagrant
=======
Download and install Vagrant 1.6.* from https://www.vagrantup.com/downloads.html .

Start VM:

vagrant up # Will ask for password to set up NFS mount which is faster on Linux/OSX
vagrant ssh

cd /home/vagrant/akl.lt
make # bootstrap takes a while, be patient
make test # Make sure everything is green
make run # and open http://127.0.0.1:8000 in your browser

Internationalisation
====================

Write translation messages in Lithuanian language.
