import paramiko
import time
from optparse import OptionParser

# Option Parer Menu
parser = OptionParser(usage="useage: %prog -o (check|assign) -H (IP Address) -u (Username) -p (Password) -x (Port) -n (VLAN Number)",
                      version="VLAN Swap 1.0")

parser.add_option("-o", "--option",
                  action="store",
                  dest="option",
                  help="Select (assign|check) depending if you are assigning or checking a port's vlan.")
parser.add_option("-H", "--hostname",
                  action="store",
                  dest="ipAddr",
                  help="Enter the IP Address or Hostname of the switch.")
parser.add_option("-u", "--username",
                  action="store",
                  dest="username",
                  help="Enter the username for the SSH connection to the switch.")
parser.add_option("-p", "--password",
                  action="store",
                  dest="password",
                  help="Enter the password for the SSH connection to the switch.")
parser.add_option("-x", "--port",
                  action="store",
                  dest="switchPort",
                  help="Enter the port of the switch. i.e. FastEthernet0/1")
parser.add_option("-n", "--vlan-number",
                  action="store",
                  dest="switchVLAN",
                  help="Enter the VLAN number of the switch. i.e. '30'")
parser.add_option("-s", "--speed",
                  action="store",
                  dest="portSpeed",
                  help="Enter the speed for the port. Options: (100|1000|auto)")
parser.add_option("-d", "--duplex",
                  action="store",
                  dest="portDuplex",
                  help="Enter the duplex for the port. Options: (half|full|auto)")

(options, args) = parser.parse_args()

class Port(object):
    def __init__(self, port, vlan, speed, duplex):
        self.port = port
        self.vlan = vlan
        self.speed = speed
        self.duplex = duplex

    def check(self):
        remote_conn.send("\n")
        remote_conn.send("show interface " + self.port + " status\n")

    def focus(self):
        remote_conn.send("\n")
        remote_conn.send("configure terminal\n")
        remote_conn.send("interface " + self.port + "\n")

    def assignVLAN(self):
        remote_conn.send("switchport access vlan " + self.vlan + "\n")
        remote_conn.send("spanning-tree portfast\n")

    def assignSpeed(self):
        remote_conn.send("speed " + self.speed + "\n")

    def assignDuplex(self):
        remote_conn.send("duplex " + self.duplex + "\n")

def disable_paging(remote_conn):
    # Disable paging on a Cisco router

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

if __name__ == '__main__':
    # VARIABLES THAT NEED CHANGED
    option = options.option
    ip = options.ipAddr
    username = options.username
    password = options.password
    switchPort = options.switchPort
    vlanNumber = options.switchVLAN
    speed = options.portSpeed
    duplex = options.portDuplex

    # Variable for the Port class
    port = Port(switchPort, vlanNumber, speed, duplex)

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print("SSH connection established to %s" %ip)

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print("Interactive SSH session established")

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    print(output)

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    if option == "check":
        port.check()
    elif option == "assign":
        if vlanNumber != None or speed != None or duplex != None:
            port.focus()
            if vlanNumber != None:
                port.assignVLAN()
            if speed != None:
                port.assignSpeed()
            if duplex != None:
                port.assignDuplex()
        else:
            print ("Nothing was selected to assign. Choose a VLAN number, port speed, or port duplex option.")
            remote_conn_pre.close()
    else:
        print("Unknown -o switch option. Use the -h switch to see additionl help on the script.")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(5000)
    print(output)