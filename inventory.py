#!/usr/bin/env python

import argparse
import json
import paramiko
import subprocess
import csv
import sys
import pprint
from itertools import ifilterfalse
from collections import defaultdict

class Inventory(object):

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

    def host_list(self):
        inventory_file = open('inventory.csv')
        inventory_reader = csv.reader(inventory_file, delimiter=',')

        # Define list of hosts and skip header
        h_list=[]
        next(inventory_reader)

        # Produce list of hosts
        for row in inventory_reader:
            h_entry = row[0]
            h_list.append(h_entry)

        # Define host list as YAML dictionary

        inventory_file2 = open('inventory.csv')
        inventory_dict2 = csv.DictReader(inventory_file2)
        host_var_total = {}

        for host in h_list:
            var= {host: next(inventory_dict2)}
            host_var_total.update(var)
            print(host_var_total)

        return {
            "group": {
                "hosts": h_list
                     },
            "_meta": {
                "hostvars": host_var_total
            }
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.host_list()
            json.dump(self.inventory, sys.stdout)

        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()


if __name__ == '__main__':
    Inventory()


