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
        h_access_voice_var_total ={}
        h_trunk_var_total ={}
        h_etherchannel_var_total ={}
        h_description_var_total ={}
        h_parameters_var_total ={}
        h_ports_total ={}
        h_cat = {"access_data": h_access_data_var_total,"access_voice": h_access_voice_var_total,"trunk": h_trunk_var_total,"etherchannel": h_etherchannel_var_total, "description": h_description_var_total, "parameters":h_parameters_var_total}

        for row in switchports_dict:
            h_type = row["port_category"]
            h_hosts_raw.append(row["hostname"])
            h_name = row["hostname"]
            # delete variables not to be output to YAML

            del row["hostname"]
            del row["port_category"]
            # delete null values
            for k, v in row.items():
                if v == '':
                    del row[k]

            row = {h_type: row}
            var = {h_name : row}
            h_cat[h_type].update(var)

        # remove duplicates from list of hosts
        h_hosts = list(set(h_hosts_raw))

        # merge dictionaries

        h_list = [h_access_data_var_total, h_access_voice_var_total, h_trunk_var_total, h_etherchannel_var_total, h_description_var_total, h_parameters_var_total]

        n=0
        while n<=(len(h_list)-1):
            for k in h_list[n]:
                if k in h_ports_total:
                    h_ports_total[k].update(h_list[n][k])
                else:
                    h_ports_total[k] = h_list[n][k]
            n=n+1

        return {
            "group": {
                "hosts": sorted(h_hosts)
                     },
            "_meta": {
                "hostvars": h_ports_total
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


