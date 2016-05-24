#!/usr/bin/python

import csv
import os


# Open CSV as dictionary
management_file = open('management.csv')
management_dict = csv.DictReader(management_file)

h_list = []
try:
    for row in management_dict:
        h_var = (row["hostname"])
        var={row["hostname"] : row}
        h_list.append(row["hostname"])

    os.chdir('./files')

    for x in h_list:
        mgmt = open(x+".mgmt")
        mgmt_contents = mgmt.read()
        mgmt.close()

        vlans = open(x+".vlans")
        vlans_contents = vlans.read()
        vlans.close()

        switchports = open(x+".switchports")
        switchports_contents = switchports.read()
        switchports.close()


        merged = open(x+".config", "w") # open in `w` mode to write
        merged.write(mgmt_contents + vlans_contents + switchports_contents) # concatenate the contents
        merged.close()

    print("-------------------------------------------------------")
    print("Configuration files merged as ./files/<hostname>.config")
    print("-------------------------------------------------------")

except Exception as e:
    print("An error has occurred - merging has not happened correctly")
