#!/bin/bash
# "MAKE SURE FOLLOWING CSV FILES ARE CORRECTLY POPULATED
# "management.csv"
# "vlans.csv"
# "switchports.csv"

cd /home/ansible/ansible-cisco-conf
ansible-playbook -v -i ./vlans.py ./create-cisco-vlans.yml
ansible-playbook -v -i ./switchports.py ./create-cisco-switchports.yml
ansible-playbook -v -i ./management.py ./create-cisco-management.yml
python ./merge-configs.py


