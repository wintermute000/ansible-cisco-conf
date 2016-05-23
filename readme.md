README FOR ansible-cisco-conf

This builds automated configuration templates for Cisco L2 switches in IOS/IOS-XE syntax.
It requires a working python and ansible environment.
If any errors are encountered executing, check line endings and convert to unix if necessary (suggest dos2unix)
If any python errors are encountered executing, pip-install the missing python modules.

Run generate.sh to execute. 
It presumes that a directory /files is present in the working directory!

Ansible is called three times via dynamic inventory method, then a python script merges the outputs into <hostname>.config files
located in ./files
The dyanmic inventory takes data from CSV files, this makes life much easier than hand populating correct YAML syntax.

- create-cisco-management.yml, using the dynamic inventory file of management.py. This refers to the CSV file management.csv.
- create-cisco-switchports.yml, using the dynamic inventory file of switchports.py. This refers to the CSV file switchports.csv.
- create-cisco-vlans.yml, using the dynamic inventory file of vlans.py. This refers to the CSV file vlans.csv.

Example CSV files are populated to illustrate the correct syntax. Management and VLANs are simple to understand, but Switchports can be 
quite fiddly - the key is to have 5 rows for each device (access_data, access_voice, etherchannel, trunk, parameters and description). 
The categories are hard coded in the script so do not deviate from the naming.
Note parameters can take /n carriage return entries if multiple custom configurations are required per port.

Each template can be easily expanded or edited for your custom requirements (e.g. common STP parameters in the vlan template). 

TO DO
- custom spanning tree module instead of shoving the same template across all devices via vlan role
- sort the dictionary outputs
- attempt to merge into one play - not sure if possible with dynamic inventory, or will be too much work to merge dictionaries correctly
- expand functionality for routers and/or L3 switches
- NXOS syntax and VPCs
- paramiko/netmiko the damned thing directly into mgt IP oh how I hate expect scripting
- wait for Cisco to get off their behind and obsolete this with APIC-EM finally

