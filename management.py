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
#     "hosts": ["ACCESS-SW1", "ACCESS-SW2", "ACCESS-SW3"]
# }, "_meta": {
#     "hostvars": {
#         "ACCESS-SW1": {
#             "username": "testuser",
#             "mgt_source_interface": "vlan2",
#             "snmp_ro_community": "teststring",
#             "enable": "testenable",
#             "group": "access_switches",
#             "ip_default_gw": "10.1.1.1",
#             "hostname": "ACCESS-SW1",
#             "syslog_server_1": "10.255.255.1",
#             "domain_name": "test.com",
#             "snmp_server_2_string": "string1",
#             "syslog_server_2": "10.255.255.2",
#             "ntp_server_1": "10.255.255.1",
#             "ntp_server_2": "10.255.255.2",
#             "snmp_server_1_string": "string1",
#             "snmp_contact": "bender@planetexpress.com",
#             "timezone": "AEST 10 0",
#             "snmp_server_1_ip": "10.255.255.1",
#             "password": "testpassword",
#             "syslog_trap_level": "notifications",
#             "snmp_server_2_ip": "10.255.255.2"
#         },
#         "ACCESS-SW3": {
#             "username": "testuser",
#             "mgt_source_interface": "ge0/1",
#             "snmp_ro_community": "teststring",
#             "enable": "testenable",
#             "group": "wan_routers",
#             "ip_default_gw": "10.1.1.1",
#             "hostname": "ACCESS-SW3",
#             "syslog_server_1": "10.255.255.1",
#             "domain_name": "test.com",
#             "snmp_server_2_string": "",
#             "syslog_server_2": "",
#             "ntp_server_1": "10.255.255.1",
#             "ntp_server_2": "10.255.255.2",
#             "snmp_server_1_string": "string3",
#             "snmp_contact": "bender@planetexpress.com",
#             "timezone": "AEST 10 0",
#             "snmp_server_1_ip": "10.255.255.1",
#             "password": "testpassword",
#             "syslog_trap_level": "notifications",
#             "snmp_server_2_ip": ""
#         },
#         "ACCESS-SW2": {
#             "username": "testuser",
#             "mgt_source_interface": "vlan2",
#             "snmp_ro_community": "teststring",
#             "enable": "testenable",
#             "group": "access_switches",
#             "ip_default_gw": "10.1.1.1",
#             "hostname": "ACCESS-SW2",
#             "syslog_server_1": "10.255.255.1",
#             "domain_name": "test.com",
#             "snmp_server_2_string": "string2",
#             "syslog_server_2": "10.255.255.2",
#             "ntp_server_1": "10.255.255.1",
#             "ntp_server_2": "10.255.255.2",
#             "snmp_server_1_string": "string2",
#             "snmp_contact": "bender@planetexpress.com",
#             "timezone": "AEST 10 0",
#             "snmp_server_1_ip": "10.255.255.1",
#             "password": "testpassword",
#             "syslog_trap_level": "notifications",
#             "snmp_server_2_ip": "10.255.255.2"
#         }
#     }
# }}
