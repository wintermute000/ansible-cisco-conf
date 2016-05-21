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

        # Define list of access data port hosts and skip header
        h_access_data_hosts_raw=[]
        h_access_data_var_total ={}

        # Define list of access etherchannel port hosts and skip header
        switchports_file4 = open('switchports.csv')
        switchports_dict4 = csv.DictReader(switchports_file4)
        h_etherchannel_hosts_raw=[]
        h_etherchannel_var_total ={}

        for row in switchports_dict4:
            h_type = row["port_category"]
            if h_type == "etherchannel":
                h_etherchannel_hosts_raw.append(row["hostname"])
                var={row["hostname"] : row}
                h_etherchannel_var_total.update(var)

        #remove duplicates from list of hosts
        h_etherchannel_hosts = list(set(h_etherchannel_hosts_raw))

        return {
            "etherchannel": {
                "hosts": h_etherchannel_hosts
                     },
            "_meta": {
                "hostvars": h_etherchannel_var_total
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


