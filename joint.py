#!/usr/bin/env python
'''
this script depends on the paramiko and netmiko python modules
netmiko https://github.com/ktbyers/netmiko
paramiko https://github.com/paramiko/paramiko

usage:
$ python joint.py
Enter the command to send: show version | inc uptime
ESW1 uptime is 2 hours, 55 minutes
R1 uptime is 1 hour, 18 minutes
R2 uptime is 1 hour, 17 minutes
ESW2 uptime is 3 hours, 3 minutes
'''
import netmiko

# Turn on verbose screen output
DEBUG = False

# Ask the user which command issue to the devices
COMMAND = raw_input('Enter the command to send: ')

# Define the devices to connnect to
# Nested dictionary defining the device paramters to pass into 
# the netmiko-paramiko module to establish an SSH connection
ALL_DEVICES = {
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
          },
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

def run_command(COMMAND):

    for device in ALL_DEVICES:

        output = connect_to_device(ALL_DEVICES[device], COMMAND)
        
        print output

if __name__ == "__main__":

    run_command(COMMAND)


