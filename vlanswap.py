import paramiko
import time
from optparse import OptionParser

# Option Parer Menu
parser = OptionParser(usage="useage: %prog -o (check|assign) -H (IP Address) -u (Username) -p (Password) -x (Port) -n (VLAN Number)",
                      version="VLAN Swap 1.0")
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
parser.add_option("-o", "--option",
                  action="store",
                  dest="option",
                  help="Select if you are assigning or checking a port's vlan.")

(options, args) = parser.parse_args()



def disable_paging(remote_conn):
    # Disable paging on a Cisco router

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

# Assign the VLAN on called network port
def changePort(defPort, defVlan):
    remote_conn.send("\n")
    remote_conn.send("configure terminal\n")
    remote_conn.send("interface " + defPort + "\n")
    remote_conn.send("switchport access vlan " + defVlan + "\n")
    remote_conn.send("spanning-tree portfast\n")

# Check VLAN status on called network port
def checkPort(defPort):
    remote_conn.send("\n")
    remote_conn.send("show interface " + defPort + " status\n")


if __name__ == '__main__':
    # VARIABLES THAT NEED CHANGED
    option = options.option
    ip = options.ipAddr
    username = options.username
    password = options.password
    switchPort = options.switchPort
    vlanNumber = options.switchVLAN


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
        checkPort(switchPort)
    elif option == "assign":
        changePort(switchPort, vlanNumber)
    else:
        print("Unknown option")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(5000)
    print(output)