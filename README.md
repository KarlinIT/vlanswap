# VLAN Swap
The purpose of the project is to allow the ablity to easily change VLANs for host devices within a 
switch/router based on the Cisco IOS commands. This is based on Python using Paramiko.The framework
of the code is based off of Kirk Byers' code from his "Python, Paramiko SSH, and Network Devices" blog 
(https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html) and tweaked to fit my needs.

The future plans of this project, besides cleaning up the code, is to incorpoate the code in a web front 
end and possibly a database that'll match VLAN Name (FE) to the VLAN number and Wall port location (FE) 
to the switch port.

# Motivation
There were a few motivating factors invovled on this project. First, I wanted to get more familiar with 
Paramiko. Paramiko can be a very powerful tool for my job as a Systems Engineer and incorporating it within
my scripts this can save both time and quality issues for my customers. Second, with a recent acquisition of
my division the support of a current tool very simliar to this one was in question so this was a means to 
prepare for the worse outcome.

# How to use
This tool is based on Python 2.7.5 and Paramiko 2.2.1. 

Review the usage output and the required switches below:

>Usage: useage: vlanswap.py -o (check|assign) -H (IP Address) -u (Username) -p (Password) -x (Port) -n (VLAN Number)
>
>Options:
>  --version             show program's version number and exit
>  
>  -h, --help            show this help message and exit
>  
>  -H IPADDR, --hostname=IPADDR
>                        Enter the IP Address or Hostname of the switch.
>                        
>  -u USERNAME, --username=USERNAME
>                        Enter the username for the SSH connection to the
>                        switch.
>                        
>  -p PASSWORD, --password=PASSWORD
>                        Enter the password for the SSH connection to the
>                        switch.
>                        
>  -x SWITCHPORT, --port=SWITCHPORT
>                        Enter the port of the switch. i.e. FastEthernet0/1
>                        
>  -n SWITCHVLAN, --vlan-number=SWITCHVLAN
>                        Enter the VLAN number of the switch. i.e. '30'
>                        
>  -o OPTION, --option=(check|assign)
>                        Select if you are assigning or checking a port's vlan.

# Test Example
The project was tested on CentOS 7.

>[root@localhost vlanswap]# **python vlanswap.py -H 192.168.1.150 -u cisco -p cisco -x FastEthernet0/1 -n 30 -o check**
>
>SSH connection established to 192.168.1.150
>
>Interactive SSH session established
>
>Baker-Switch-01#
>
>Baker-Switch-01#show interface FastEthernet0/1 status
>
>Port      Name               Status       Vlan       Duplex  Speed Type
>Fa0/1                        connected    30         a-full  a-100 10/100BaseTX
>Baker-Switch-01#
>[root@localhost vlanswap]#
