#!/usr/bin/env python

import argparse
import json
import csv
import sys



class Inventory(object):

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

    def host_list(self):

        # Define list of hosts and list of hostvars
        h_list=[]
        h_var_total = {}

        # Open CSV as dictionary
        management_file = open('management.csv')
        management_dict = csv.DictReader(management_file)

        # Iterate
        for row in management_dict:
            h_var = (row["hostname"])
            var={row["hostname"] : row}

            h_list.append(row["hostname"])
            h_var_total.update(var)

        # Return YAML
        return {
            "group": {
                "hosts": h_list
                     },
            "_meta": {
                "hostvars": h_var_total
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


