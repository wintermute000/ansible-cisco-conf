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
- attempt to merge into one play - not sure if possible with dynamic inventory, or will be too much work to merge dictionaries correctly
- expand functionality for routers and/or L3 switches
- NXOS syntax and VPCs
- paramiko/netmiko the damned thing directly into mgt IP oh how I hate expect scripting
- wait for Cisco to get off their behind and obsolete this with APIC-EM finally



### ILLUSTRATE INPUT CSV FORMAT
ansible@ubuntu-test:~/ansible-cisco-conf$ cat ./management.csv 

hostname,group,username,password,enable,domain_name,ntp_server_1,ntp_server_2,syslog_server_1,syslog_server_2,syslog_trap_level,mgt_source_interface,snmp_contact,snmp_ro_community,snmp_server_1_ip,snmp_server_1_string,snmp_server_2_ip,snmp_server_2_string,timezone,ip_default_gw
ACCESS-SW1,access_switches,testuser,testpassword,testenable,test.com,10.255.255.1,10.255.255.2,10.255.255.1,10.255.255.2,notifications,vlan2,bender@planetexpress.com,teststring,10.255.255.1,string1,10.255.255.2,string1,AEST 10 0,10.1.1.1
ACCESS-SW2,access_switches,testuser,testpassword,testenable,test.com,10.255.255.1,10.255.255.2,10.255.255.1,10.255.255.2,notifications,vlan2,bender@planetexpress.com,teststring,10.255.255.1,string2,10.255.255.2,string2,AEST 10 0,10.1.1.1
ACCESS-SW3,wan_routers,testuser,testpassword,testenable,test.com,10.255.255.1,10.255.255.2,10.255.255.1,,notifications,ge0/1,bender@planetexpress.com,teststring,10.255.255.1,string3,,,AEST 10 0,10.1.1.1


ansible@ubuntu-test:~/ansible-cisco-conf$ cat ./switchports.csv 

hostname,port_category,Po1,Po2,Po3,g1/0/1-11,g1/0/12-22,g1/0/23,g1/0/24,g1/0/1-22
ACCESS-SW1,description,Uplink to core,,,User VLAN 10 + Voice,User VLAN 30 + Voice,Port-channel 1 member,Port-channel 1 member,
ACCESS-SW1,access_data,,,,10,30,,,
ACCESS-SW1,access_voice,,,,40,40,,,
ACCESS-SW1,trunk,"10,20,30,40",,,,,,,
ACCESS-SW1,etherchannel,,,,,,1,1,
ACCESS-SW1,parameters,switchport trunk native vlan 999,,,spanning-tree portfast,spanning-tree portfast,"speed auto
duplex auto","speed auto
duplex auto",
ACCESS-SW2,description,,Uplink to core,,User VLAN 10 + Voice,User VLAN 30 + Voice,Port-channel 2 member,Port-channel 2 member,
ACCESS-SW2,access_data,,,,20,30,,,
ACCESS-SW2,access_voice,,,,40,40,,,
ACCESS-SW2,trunk,,"10,20,30,40",,,,,,
ACCESS-SW2,etherchannel,,,,,,2,2,
ACCESS-SW2,parameters,,switchport trunk native vlan 999,,spanning-tree portfast,spanning-tree portfast,,,
ACCESS-SW3,description,,,Uplink to core,,,Port-channel 3 member,Port-channel 3 member,User VLAN 10 + Voice
ACCESS-SW3,access_data,,,,,,,,10
ACCESS-SW3,access_voice,,,,,,,,40
ACCESS-SW3,trunk,,,"10,20,30,40",,,,,
ACCESS-SW3,etherchannel,,,,,,3,3,
ACCESS-SW3,parameters,,,switchport trunk native vlan 999,spanning-tree portfast,spanning-tree portfast,,,

ansible@ubuntu-test:~/ansible-cisco-conf$ cat ./vlans.csv 
hostname,10,20,30,40
ACCESS-SW1,data-10,data-20,data-30,voice
ACCESS-SW2,data-10,data-20,data-30,voice
ACCESS-SW3,data-10,data-20,data-30,voice




### RUN ANSIBLE VIA SHELL SCRIPT
ansible@ubuntu-test:~/ansible-cisco-conf$ ./generate-configs.sh 


PLAY [Generate management configuration files] ******************************** 


TASK: [vlans | Generate VLAN configuration] *********************************** 
changed: [ACCESS-SW2] => {"changed": true, "dest": "./files/ACCESS-SW2.vlans", "gid": 1001, "group": "ansible", "md5sum": "6ab6245f01d5f84ed105366724632c10", "mode": "0664", "owner": "ansible", "size": 208, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007267.61-153911396762400/source", "state": "file", "uid": 1001}
changed: [ACCESS-SW3] => {"changed": true, "dest": "./files/ACCESS-SW3.vlans", "gid": 1001, "group": "ansible", "md5sum": "6ab6245f01d5f84ed105366724632c10", "mode": "0664", "owner": "ansible", "size": 208, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007267.6-4419110684860/source", "state": "file", "uid": 1001}
changed: [ACCESS-SW1] => {"changed": true, "dest": "./files/ACCESS-SW1.vlans", "gid": 1001, "group": "ansible", "md5sum": "6ab6245f01d5f84ed105366724632c10", "mode": "0664", "owner": "ansible", "size": 208, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007267.6-208974451106398/source", "state": "file", "uid": 1001}


PLAY RECAP ******************************************************************** 
ACCESS-SW1                 : ok=1    changed=1    unreachable=0    failed=0   
ACCESS-SW2                 : ok=1    changed=1    unreachable=0    failed=0   
ACCESS-SW3                 : ok=1    changed=1    unreachable=0    failed=0   




PLAY [Generate access switchports configuration files] ************************ 


TASK: [switchports | Generate switch ports configuration] ********************* 
changed: [ACCESS-SW2] => {"changed": true, "dest": "./files/ACCESS-SW2.switchports", "gid": 1001, "group": "ansible", "md5sum": "e763486a4359c554c5af4dd92480b088", "mode": "0664", "owner": "ansible", "size": 843, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007268.03-278131952123541/source", "state": "file", "uid": 1001}
changed: [ACCESS-SW1] => {"changed": true, "dest": "./files/ACCESS-SW1.switchports", "gid": 1001, "group": "ansible", "md5sum": "5d9045031ea176dae84f569b19371c58", "mode": "0664", "owner": "ansible", "size": 897, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007268.02-280331391450933/source", "state": "file", "uid": 1001}
changed: [ACCESS-SW3] => {"changed": true, "dest": "./files/ACCESS-SW3.switchports", "gid": 1001, "group": "ansible", "md5sum": "a15ec69de5b999f9feaccbf79980963e", "mode": "0664", "owner": "ansible", "size": 626, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007268.03-190959576835212/source", "state": "file", "uid": 1001}


PLAY RECAP ******************************************************************** 
ACCESS-SW1                 : ok=1    changed=1    unreachable=0    failed=0   
ACCESS-SW2                 : ok=1    changed=1    unreachable=0    failed=0   
ACCESS-SW3                 : ok=1    changed=1    unreachable=0    failed=0   




PLAY [Generate management configuration files] ******************************** 


TASK: [management | Generate management configuration] ************************ 
changed: [ACCESS-SW3] => {"changed": true, "dest": "./files/ACCESS-SW3.mgmt", "gid": 1001, "group": "ansible", "md5sum": "843e979b2dee91022eba29847d2996f2", "mode": "0664", "owner": "ansible", "size": 516, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007268.49-154617469532748/source", "state": "file", "uid": 1001}
changed: [ACCESS-SW1] => {"changed": true, "dest": "./files/ACCESS-SW1.mgmt", "gid": 1001, "group": "ansible", "md5sum": "5103228e29bd53f1305a36a53f322123", "mode": "0664", "owner": "ansible", "size": 547, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007268.47-72849816500810/source", "state": "file", "uid": 1001}
changed: [ACCESS-SW2] => {"changed": true, "dest": "./files/ACCESS-SW2.mgmt", "gid": 1001, "group": "ansible", "md5sum": "c534f2b19f3f79a5fe8da5e5cc050781", "mode": "0664", "owner": "ansible", "size": 547, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1464007268.48-185854201577063/source", "state": "file", "uid": 1001}


PLAY RECAP ******************************************************************** 
ACCESS-SW1                 : ok=1    changed=1    unreachable=0    failed=0   
ACCESS-SW2                 : ok=1    changed=1    unreachable=0    failed=0   
ACCESS-SW3                 : ok=1    changed=1    unreachable=0    failed=0   


### EXAMPLE OUTPUT

ansible@ubuntu-test:~/ansible-cisco-conf$ cat ./files/ACCESS-SW1.config 


hostname ACCESS-SW1
username testuser secret testpassword
enable secret testenable


ip domain-name test.com
no ip domain-lookup


timezone AEST 10 0


login on-failure log
login on-success log


logging trap notifications
logging source-interface vlan2
logging host 10.255.255.1
logging host 10.255.255.2


snmp-server community teststring RO
snmp-server trap-source vlan2
snmp-server contact bender@planetexpress.com
snmp-server host 10.255.255.1 string1
snmp-server host 10.255.255.2 string1
snmp ifmib ifindex persist


ip default-gateway 10.1.1.1


vlan 10
    name data-10
vlan 30
    name data-30
vlan 20
    name data-20
vlan 40
    name voice


spanning-tree mode rapid-pvst
spanning-tree portfast bpduguard default
spanning-tree vlans 1-4094 pri 32768


!!! ETHERCHANNEL MEMBERS
interface range g1/0/24
    description Port-channel 1 member
    channel-group 1 mode active
    speed auto
duplex auto
    no shut
    
interface range g1/0/23
    description Port-channel 1 member
    channel-group 1 mode active
    speed auto
duplex auto
    no shut
    




!!! ACCESS PORTS
interface range g1/0/12-22
    description User VLAN 30 + Voice
    switchport mode access
    switchport access vlan 30
    switchport voice vlan 40
    spanning-tree portfast
    no shut


interface range g1/0/1-11
    description User VLAN 10 + Voice
    switchport mode access
    switchport access vlan 10
    switchport voice vlan 40
    spanning-tree portfast
    no shut






!!! TRUNK PORTS
interface range Po1
    description Uplink to core
    switchport mode trunk
    switchport trunk allowed vlan add 10,20,30,40
    switchport trunk native vlan 999
    no shut
