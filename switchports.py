#!/usr/bin/env python

import argparse
import json
import csv
import sys


class switchports(object):

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

    def host_list(self):
        # Open CSV file as dictionary
        switchports_file = open('switchports.csv')
        switchports_dict = csv.DictReader(switchports_file)

        # Define variables
        h_hosts_raw=[]
        h_access_data_var_total = {}
        h_access_voice_var_total = {}
        h_trunk_var_total = {}
        h_etherchannel_var_total = {}
        h_description_var_total = {}
        h_parameters_var_total = {}
        h_ports_total ={}

        # Define dictionary of dictionaries to iterate over
        # key : value = category : dict
        h_cat = {"access_data": h_access_data_var_total,"access_voice": h_access_voice_var_total,"trunk": h_trunk_var_total,"etherchannel": h_etherchannel_var_total, "description": h_description_var_total, "parameters":h_parameters_var_total}

        # Iterate over CSV dictionary and append to correct category's dictionary
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
            # format as required by ansible JSON { hostname : { category : { values} } }
            row = {h_type: row}
            var = {h_name : row}
            # append to correct dictionary
            h_cat[h_type].update(var)

        # remove duplicates from list of hosts
        h_hosts = list(set(h_hosts_raw))

        # merge category dictionaries
        h_list = [h_access_data_var_total, h_access_voice_var_total, h_trunk_var_total, h_etherchannel_var_total, h_description_var_total, h_parameters_var_total]
        n=0
        while n<=(len(h_list)-1):
            for k in h_list[n]:
                if k in h_ports_total:
                    h_ports_total[k].update(h_list[n][k])
                else:
                    h_ports_total[k] = h_list[n][k]
            n=n+1

        # return stdout in ansible compliant JSON output
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


#  EXAMPLE JSON OUTPUT IN ANSIBLE INVENTORY FORMAT

# {"group": {
#     "hosts": ["ACCESS-SW1", "ACCESS-SW2", "ACCESS-SW3"]
# }, "_meta": {
#     "hostvars": {
#         "ACCESS-SW1": {
#             "description": {
#                 "g1/0/12-22": "User VLAN 30 + Voice",
#                 "g1/0/1-11": "User VLAN 10 + Voice",
#                 "g1/0/24": "Port-channel 1 member",
#                 "g1/0/23": "Port-channel 1 member",
#                 "Po1": "Uplink to core"
#             },
#             "parameters": {
#                 "g1/0/12-22": "spanning-tree portfast",
#                 "g1/0/1-11": "spanning-tree portfast",
#                 "g1/0/24": "speed auto\nduplex auto",
#                 "g1/0/23": "speed auto\nduplex auto",
#                 "Po1": "switchport trunk native vlan 999"
#             },
#             "trunk": {
#                 "Po1": "10,20,30,40"
#             },
#             "etherchannel": {
#                 "g1/0/24": "1",
#                 "g1/0/23": "1"
#             },
#             "access_data": {
#                 "g1/0/12-22": "30",
#                 "g1/0/1-11": "10"
#             },
#             "access_voice": {
#                 "g1/0/12-22": "40",
#                 "g1/0/1-11": "40"
#             }
#         },
#         "ACCESS-SW3": {
#             "description": {
#                 "g1/0/24": "Port-channel 3 member",
#                 "Po3": "Uplink to core",
#                 "g1/0/23": "Port-channel 3 member",
#                 "g1/0/1-22": "User VLAN 10 + Voice"
#             },
#             "parameters": {
#                 "g1/0/12-22": "spanning-tree portfast",
#                 "g1/0/1-11": "spanning-tree portfast",
#                 "Po3": "switchport trunk native vlan 999"
#             },
#             "trunk": {
#                 "Po3": "10,20,30,40"
#             },
#             "etherchannel": {
#                 "g1/0/24": "3",
#                 "g1/0/23": "3"
#             },
#             "access_data": {
#                 "g1/0/1-22": "10"
#             },
#             "access_voice": {
#                 "g1/0/1-22": "40"
#             }
#         },
#         "ACCESS-SW2": {
#             "description": {
#                 "g1/0/12-22": "User VLAN 30 + Voice",
#                 "g1/0/1-11": "User VLAN 10 + Voice",
#                 "g1/0/24": "Port-channel 2 member",
#                 "Po2": "Uplink to core",
#                 "g1/0/23": "Port-channel 2 member"
#             },
#             "parameters": {
#                 "g1/0/12-22": "spanning-tree portfast",
#                 "g1/0/1-11": "spanning-tree portfast",
#                 "Po2": "switchport trunk native vlan 999"
#             },
#             "trunk": {
#                 "Po2": "10,20,30,40"
#             },
#             "etherchannel": {
#                 "g1/0/24": "2",
#                 "g1/0/23": "2"
#             },
#             "access_data": {
#                 "g1/0/12-22": "30",
#                 "g1/0/1-11": "20"
#             },
#             "access_voice": {
#                 "g1/0/12-22": "40",
#                 "g1/0/1-11": "40"
#             }
#         }
#     }
# }}
