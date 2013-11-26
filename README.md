Testbed for deployment via ansible
==================================

Type ``vagrant up`` to pull up a test machine. Its SSH port is mapped to the
host on port 2202, the root password is lel.

Call ansible via:

    ansible-playbook -i hosts -c ssh -k ./user_setup.yml
