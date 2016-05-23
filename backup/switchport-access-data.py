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

class switchports(object):

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

    def host_list(self):
        switchports_file = open('switchports.csv')
        switchports_dict = csv.DictReader(switchports_file)

        # Define list of access data port hosts
        h_hosts_raw=[]
        h_access_data_var_total ={}



        for row in switchports_dict:
            h_type = row["port_category"]

            if h_type == "access_data":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                #var={row["hostname"] : row}
                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"access_ports":  row}
                var = {h_name : row}
                h_access_data_var_total.update(var)


        #remove duplicates from list of hosts
        h_hosts = list(set(h_hosts_raw))

        return {
            "access_hosts": {
                "hosts": h_hosts
                     },
            "_meta": {
                "hostvars": h_access_data_var_total
            }
        }


    # Empty switchports for testing.
    def empty_switchports(self):
        return {'_meta': {'hostvars': {}}}

    def __init__(self):
        self.switchports = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.switchports = self.host_list()
            json.dump(self.switchports, sys.stdout)

        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.switchports = self.empty_switchports()
        # If no groups or vars are present, return an empty switchports.
        else:
            self.switchports = self.empty_switchports()


if __name__ == '__main__':
    switchports()


