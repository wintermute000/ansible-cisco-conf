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
        h_hosts_raw=[]
        h_var_total = {}

        # Open CSV as dictionary
        vlan_file = open('vlans.csv')
        vlan_dict = csv.DictReader(vlan_file)

        # Iterate
        for row in vlan_dict:
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML
                del row["hostname"]

                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"vlans":  row}
                var = {h_name : row}

                h_var_total.update(var)

        # remove duplicates from list of hosts
        h_list = list(set(h_hosts_raw))

        # return stdout in ansible compliant JSON output
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

# EXAMPLE JSON OUTPUT IN ANSIBLE INVENTORY FORMAT
# {"group": {
#     "hosts": ["ACCESS-SW1", "ACCESS-SW3", "ACCESS-SW2"]
# }, "_meta": {
#     "hostvars": {
#         "ACCESS-SW1": {
#             "vlans": {
#                 "10": "data-10",
#                 "20": "data-20",
#                 "40": "voice",
#                 "30": "data-30"
#             }
#         },
#         "ACCESS-SW3": {
#             "vlans": {
#                 "10": "data-10",
#                 "20": "data-20",
#                 "40": "voice",
#                 "30": "data-30"
#             }
#         },
#         "ACCESS-SW2": {
#             "vlans": {
#                 "10": "data-10",
#                 "20": "data-20",
#                 "40": "voice",
#                 "30": "data-30"
#             }
#         }
#     }
# }}
