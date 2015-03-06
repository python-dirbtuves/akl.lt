AKL website project.

This repository is move from https://launchpad.net/akl-web-site .

Development environment
=======================

Requirements 
------------

- All instructions bellow should perfectly work on `Ubuntu 14.04`_. If you use
  something else, project setup may be slightly different.

.. _Ubuntu 14.04: http://www.ubuntu.com/download/desktop

- Before you start, make sure, that you have `github.com`_ with `SSH key`__ in
  place.

.. _github.com: https://github.com/
.. __: https://help.github.com/articles/generating-ssh-keys/

- Your ``~/.git/config`` should include your name and email (make sure, that you
  specify same email address you use for Github). The section in
  ``~/.git/config`` file should look like this::

      [user]
      name = Name Surname
      email = name.surname@example.com


Preparing development environment
---------------------------------

First of all, install ``git``::

    sudo apt install git

Then create project directory::

    mkdir akl.lt && cd akl.lt

This directory will contain several other repositories, main ``akl.lt`` website
repository and ``akl.lt-zope-export`` repository with exported data from old
``akl.lt`` website. So clone these two repositories::

    git clone git@github.com:python-dirbtuves/akl.lt.git 
    git clone git@github.com:mgedmin/akl.lt-zope-export.git

Now change current working directory to ``akl.lt`` and now we will work from
there::

    cd akl.lt

First thing you have to do is to install system dependencies, these are
development headers and some libraries (please note, that this command will be
run with ``sudo`` and will ask your password)::

    make ubuntu

Now, build project and then run tests to make sure, that everything is OK
(first command ``make`` will take some time to finish, be patient!)::

    make
    make test

Last thing to do, is to import data from old website export::

    bin/django akllt_importzope ../akl.lt-zope-export

Now you should be able to run development server and see new website working::

    make run

Vagrant
-------

If you don't have `Ubuntu 14.04`_, you can use Vagrant with Ubuntu virtual
machine.

Download and install Vagrant 1.6.* from https://www.vagrantup.com/downloads.html .

Start virtual machine

    sudo apt install nfs-kernel-server nfs-common

    vagrant up # Will ask for password to set up NFS mount which is faster on Linux/OSX

Build project inside virtual machine::

    vagrant ssh
    cd /home/vagrant/akl.lt
    make # bootstrap takes a while, be patient
    make test # Make sure everything is green
    make run # and open http://127.0.0.1:8000 in your browser

How to run tests
================

There are several ways how you can run tests. Below is list of all available
options:

- ::

      make testall

  This runs all available tests, including code style checkers and code
  linters.

- ::

      make test

  Runs only tests, without code style checkers and code linters.

- ::

      scripts/runtests.py akllt/dataimport

  Runs all tests from specified directory path.

- ::

      scripts/runtests.py akllt/dataimport/tests/test_image_import.py

  Runs all tests in specified file path.

- ::

      scripts/runtests.py akllt/dataimport/tests/test_image_import.py:ImportImageTests

  Run all tests in specified test case class.

- ::

      scripts/runtests.py akllt/dataimport/tests/test_image_import.py:ImportImageTests.test_import_page_image

  Run single test method.


Internationalisation
====================

Write translation messages in Lithuanian language.
