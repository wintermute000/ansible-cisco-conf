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

        for row in switchports_dict:
            h_type = row["port_category"]

            if h_type == "access_data":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]

                row = {"access_ports": row}
                var = {h_name : row}

                h_access_data_var_total.update(var)

            if h_type == "access_voice":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"voice_ports":  row}
                var = {h_name : row}

                h_access_voice_var_total.update(var)

            if h_type == "trunk":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"trunk_ports":  row}
                var = {h_name : row}
                h_trunk_var_total.update(var)
                
            if h_type == "etherchannel":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"etherchannels":  row}
                var = {h_name : row}
                h_etherchannel_var_total.update(var)
                
            if h_type == "description":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"descriptions":  row}
                var = {h_name : row}
                h_description_var_total.update(var)
                
            if h_type == "parameters":
                h_hosts_raw.append(row["hostname"])
                h_name = row["hostname"]

                # delete variables not to be output to YAML

                del row["hostname"]
                del row["port_category"]
                # delete null values
                for k, v in row.items():
                    if v == '':
                        del row[k]
                row = {"parameters":  row}
                var = {h_name : row}
                h_parameters_var_total.update(var)

        # remove duplicates from list of hosts
        h_hosts = list(set(h_hosts_raw))




        # merge dictionaries
        for k in h_access_data_var_total:
            if k in h_ports_total:
                h_ports_total[k].update(h_access_data_var_total[k])
            else:
                h_ports_total[k] = h_access_data_var_total[k]

        for y in h_access_voice_var_total:
            if y in h_ports_total:
                h_ports_total[y].update(h_access_voice_var_total[y])
            else:
                h_ports_total[y] = h_access_voice_var_total[y]

        for z in h_trunk_var_total:
            if z in h_ports_total:
                h_ports_total[z].update(h_trunk_var_total[z])
            else:
                h_ports_total[z] = h_trunk_var_total[z]
                
        for a in h_etherchannel_var_total:
            if a in h_ports_total:
                h_ports_total[a].update(h_etherchannel_var_total[a])
            else:
                h_ports_total[a] = h_etherchannel_var_total[a]
                
        for b in h_description_var_total:
            if b in h_ports_total:
                h_ports_total[b].update(h_description_var_total[b])
            else:
                h_ports_total[b] = h_description_var_total[b]
                
        for c in h_parameters_var_total:
            if c in h_ports_total:
                h_ports_total[c].update(h_parameters_var_total[c])
            else:
                h_ports_total[c] = h_parameters_var_total[c]

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


