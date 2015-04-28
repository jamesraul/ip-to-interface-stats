#!/usr/bin/env python
'''
this script depends on the paramiko and netmiko python modules
netmiko https://github.com/ktbyers/netmiko
paramiko https://github.com/paramiko/paramiko

usage:
$ python ip-to-int.py
1Enter the IP Address:10.1.1.11
Querying routers...
Two arp entries found.
Routers see 10.1.1.11 with MAC address 0800.2726.4a23
Querying switches...
IP Address 10.1.1.11 is attached to switch ESW1 interface FastEthernet1/3
FastEthernet1/3 is up, line protocol is up
  Hardware is Fast Ethernet, address is c403.07ca.f103 (bia c403.07ca.f103)
  Description: Host1
  MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 100Mb/s
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input never, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     0 packets input, 0 bytes, 0 no buffer
     Received 0 broadcasts, 0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 input packets with dribble condition detected
     0 packets output, 0 bytes, 0 underruns
     0 output errors, 0 collisions, 2 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier
     0 output buffer failures, 0 output buffers swapped out
Finished querying all switches.
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

SWITCHES = {
          'ESW1': {
          'ip': '10.0.0.11',
          'device_type': 'cisco_ios',
          'username': 'admin',
          'password': 'cisco',
          'secret': 'cisco',
          'verbose': False
          },
          'ESW2': {
          'ip': '10.0.0.12',
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

        # If router does not have ARP table entry continue to the next router
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
        print "IP Address is not seen on any routers. (No ARP entries found)"
        
        return None

def get_switch_interface(mac_address):
    '''
    #
    switch commands used in the function.
    #
    ---- provides the interface the mac was learned on ----
    #
    show mac-address-table address 0800.2726.4a23
    Destination Address  Address Type  VLAN  Destination Port
    -------------------  ------------  ----  --------------------
    0800.2726.4a23    Dynamic     101     FastEthernet1/3
    #
    ---- provides the switching interface attributes of the port ----
    #
    show interface FastEthernet1/3 switchport
    Name: Fa1/3
    Switchport: Enabled
    Administrative Mode: static access
    Operational Mode: static access
    Administrative Trunking Encapsulation: dot1q
    Operational Trunking Encapsulation: native
    Negotiation of Trunking: Disabled
    Access Mode VLAN: 101 (server1)
    #
    ---- provides all the interface statistics of a port (errors, rate, etc)
    #
    FastEthernet1/3 is up, line protocol is up
    Hardware is Fast Ethernet, address is c403.02b0.f103 (bia c403.02b0.f103)
    Description: Host1
    MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,
       reliability 255/255, txload 1/255, rxload 1/255
    Encapsulation ARPA, loopback not se t
 
    Keepalive set (10 sec)
    Full-duplex, 100Mb/s
    ARP type: ARPA, ARP Timeout 04:00:00
    Last input never, output never, output hang never
    Last clearing of "show interface" counters never
    Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
    Queueing strategy: fifo
    Output queue: 0/40 (size/max)
    5 minute input rate 0 bits/sec, 0 packets/sec
    5 minute output rate 0 bits/sec, 0 packets/sec
       0 packets input, 0 bytes, 0 no buffer
       Received 0 broadcasts, 0 runts, 0 giants, 0 throttles
       0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
       0 input packets with dribble condition detected
       0 packets output, 0 bytes, 0 underruns
       0 output errors, 0 collisions, 2 interface resets
       0 unknown protocol drops
       0 babbles, 0 late collision, 0 deferred
       0 lost carrier, 0 no carrier
       0 output buffer failures, 0 output buffers swapped out
    '''
    
    print "Querying switches..."

    # Set mac_found and access_port_int to False (condition checking later)
    mac_found = False
    access_port_int = False

    for switch in SWITCHES:

        # Connect to each switch and find the MAC address entry
        mac_entry = connect_to_device(SWITCHES[switch], "show mac-address-table address {}".format(mac_address))
    
        # Parse the interface ID from the MAC table entry 
        if re.search(r'((FastEth|GigabitEth|TenGigabitEth|Eth)ernet[0-9]/[0-9]|Po[0-9])', mac_entry):

            match = re.search(r'((FastEth|GigabitEth|TenGigabitEth|Eth)ernet[0-9]/[0-9]|Po[0-9])', mac_entry)
            
            # Save the interface found to the interface object
            interface = match.group(0)

            if DEBUG:
                print "Interface parsed data: " + interface

            # Set mac_found to True (condition checking later)
            mac_found = True

            # Connect to the switch and capture the switching attributes of the interface
            switchport_info = connect_to_device(SWITCHES[switch], "show interface {} switchport".format(interface))
    
            # Parse the operation mode of the switchport
            match = re.search(r'Operational Mode: (.*)', switchport_info)
            switchport_mode = match.group(1)

            # Make sure the switchport in access mode (host port)
            if re.search(r'access', switchport_mode):
    
                # Set access_port_mac to True (condition checking later)
                access_port_int = True

                print "IP Address {} is attached to switch {} interface {}".format(IP_ADDRESS, switch, interface)
    
                interface_status = connect_to_device(SWITCHES[switch], "show interface {}".format(interface))
    
                print interface_status

        # If switch does not have MAC table entry print debug info and continue to the next switch    
        else:

            if DEBUG:
                print "Switch: {}\
                \nMAC entry not found.".format(switch)

    print "Finished querying all switches."

    # Condition checking to provide user feedback.
    # Did we find a MAC address, but not a port that was in access mode?
    if mac_found:

        if not access_port_int:

            print "MAC address was found, but the interface was not an access port."

    # Did we check all switches and not find the MAC address?
    elif not mac_found:

        print "MAC address not found on any switches. Ensure host has recently communicated."

    else:
        if DEBUG:
            print "Script completed."

if __name__ == "__main__":

    mac_address = get_mac_from_routers()

    if mac_address:
        get_switch_interface(mac_address)






