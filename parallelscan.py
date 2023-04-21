# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 08:33:35 2022

@author: jtrex
"""
# Sanity test
from multiprocessing import Process

import socket
# Handles network ping

from datetime import datetime
# For stopwatch

import time
# For sleep


custom_ip = "192.168.1.103"
scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.setdefaulttimeout(1)


def ip_scan(ip):
    try:
        socket.setdefaulttimeout(1)
        if scan_socket.connect_ex((ip, 135)) == 0:
            print("_____________________________________________________________________")
            print("Alive: ", ip)
            print("_____________________________________________________________________")
        else:
            print("Timed out: ", ip)
    except:
        print("Connection failed")


def parallel_scan(ip_prefix, i):
    print('Process: ', i)
    custom_ip = ip_prefix + str(i-1)
    try:
        ip_scan(custom_ip)
    except:
        print("Scan failed for ", custom_ip)


# Referencing https://www.tutorialspoint.com/python_penetration_testing/python_penetration_testing_network_scanner.htm

#Scan portion of sequential_scan, for every custom_ip, checks to see if it responds to a ping. Display alive if alive.
#Declares socket, sets timeout to 1 instead of 20 seconds, uses socket to connect to ip
def sequential_scan(custom_ip):
    print("scanning ", custom_ip)
    sequential_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    if sequential_socket.connect_ex((custom_ip, 135)) == 0:
        print("_____________________________________________________________________")
        print("Alive: ", custom_ip)
        print("_____________________________________________________________________")
    else:
        print("Sequential Timed Out")


# For speedup result reference
#Iterates through every ip in last octet, runs sequential_scan
#Also records start and stop time at start and end. 
def initiate_sequential_scan(ip_prefix):
    # Record start time
    time_start = datetime.now()
    # Iterate through entire ipv4 range
    for j in range(1, 255):
        custom_ip = ip_prefix + str(j-1)
        # MUST be in seperate function, will hang / take 20 seconds each instance
        if (sequential_scan(custom_ip)):
            print(custom_ip, "Sequential Success, ", j)
        else:
            print(custom_ip, "Sequential Failure, ", j)
    # Take finish time, difference is time it took
    time_finish = datetime.now()
    time_total = time_finish - time_start
    print("Sequential final time: ", time_total)

#Generates processes for every ip in last quartet, starts them, waits for them to join and briefly pauses 
if __name__ == '__main__':
    time_start = datetime.now()
    # https: // stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished
    # Great way to manage threads
    scan_node = []
    ip_prefix = "192.168.1."
    for i in range(1, 255):
        print("Generating process: ", i)
        scan_node.append(Process(target=parallel_scan, args=(ip_prefix, i,)))
    for i in scan_node:
        i.start()
    for i in scan_node:
        i.join(500)
    # If something gets hung up clean it up after a few minutes, should be changed for slower hardware
    # Wrap up loose processes, wait till they're done to finish exectuion
    time_finish = datetime.now()
    time.sleep(1)
    time_total = time_finish - time_start
    print("Parallel final time: ", time_total)
    print("Test for sequential? y/n")
    user_input = input()
    #Test for sequential scan given user input y
    if user_input == "y":
        initiate_sequential_scan("192.168.1.")
    else:
        print("Happy trails.")
