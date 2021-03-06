#!/usr/bin/env python
'''
this script depends on the paramiko and netmiko python modules
netmiko https://github.com/ktbyers/netmiko
paramiko https://github.com/paramiko/paramiko

usage:
$ python ex1.py
Enter the IP Address: 10.1.1.11
Querying routers...
Two arp entries found.
Routers see 10.1.1.11 with MAC address 0800.2726.4a23
'''
import re
import netmiko

# Turn on verbose screen output
DEBUG = False

# Ask the user the IP address of the host to search/display
IP_ADDRESS = raw_input('Enter the IP Address: ')

# Define the routers that route host networks (access routers)
# Nested dictionary defining the router paramters to pass into 
# the netmiko-paramiko module to establish an SSH connection
ROUTERS = {
          'R1': {
          'ip': '10.0.0.2',
          'device_type': 'cisco_ios',
          'username': 'admin',
          'password': 'cisco',
          'secret': 'cisco',
          'verbose': False
          },
          'R2': {
          'ip': '10.0.0.3',
          'device_type': 'cisco_ios',
          'username': 'admin',
          'password': 'cisco',
          'secret': 'cisco',
          'verbose': False
          }
}
def connect_to_device(device_params, command):
    '''
    create a function to utilize the netmiko python module
    pass in the device paramaters (ip, username, password)
    issue the command passed into the function
    set DEBUG to true to get entire command output
    '''
    SSHClass = netmiko.ssh_dispatcher(device_type=device_params['device_type'])
    
    net_connect = SSHClass(**device_params)
    
    output = net_connect.send_command(command)

    # print the output of the command if DEBUG is enabled.
    if DEBUG:
        print "-" * 20 + "[Command Output Debug]" + "-" * 20
        print output
        print "-" * 62 + "\n"
    
    return output

def get_mac_from_routers():
    '''
    show ip arp 10.0.0.5
    Protocol  Address          Age (min)  Hardware Addr   Type   Interface
    Internet  10.0.0.5                5   0800.2725.d985  ARPA   FastEthernet0/0
    '''    
    # Create a list to store all the MAC addresses found.
    macs_found = []

    # Connect to each router, issue show ip arp {ip_address}
    print "Querying routers..."

    for router in ROUTERS:

        arp_entry = connect_to_device(ROUTERS[router], "show ip arp {}".format(IP_ADDRESS))

        # Find the MAC address in the screen output
        if re.search(r'(..............)  ARPA', arp_entry):

            match = re.search(r'(..............)  ARPA', arp_entry)

            # Save the MAC address found to the mac_address object
            mac_address = match.group(1)
            
            # DEBUG: Print the information found for this router.
            if DEBUG:
                print "\nRouter: {}\
                \nIP Address {} has MAC address {}\n".format(router, IP_ADDRESS, mac_address)

            # Add the MAC addres found to the macs_found list
            macs_found.append(mac_address)

        else:

            if DEBUG:
                print "\nRouter: {}\
                \nMAC address not found.".format(router)
    
    # Determine how many MAC addresses are found and compare results   
    if len(macs_found) == 2:

        print "Two arp entries found."
        
        if macs_found[0] == macs_found[1]:

            print "Routers see {} with MAC address {}".format(IP_ADDRESS, mac_address)
            
            return macs_found[0]
        else:
            print "[WARNING] Two different MAC addresses found! {}".format(macs_found)
           
            return None
    
    elif len(macs_found) == 1:
        
        print "One arp entry found.\
        \nRouter sees {} with MAC address {}".format(IP_ADDRESS, mac_address)
        
        return macs_found[0]
    
    else:
        print "IP Address is not seen on the network. (No ARP entries found)"
        
        return None


if __name__ == "__main__":

    get_mac_from_routers()

