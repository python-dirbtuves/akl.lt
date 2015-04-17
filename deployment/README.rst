Testing deployment scripts
==========================

::

    vagrant up
    ssh-copy-id vagrant@10.0.0.42
    ansible-playbook -u vagrant -i 10.0.0.42, playbook.yml
