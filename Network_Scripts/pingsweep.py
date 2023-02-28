#Louis DeVictoria
import ipaddress
import os
import socket
import subprocess
from timeit import default_timer as timer

#Original PingSweep Script
def pingsweep_original(prefix):
    start = timer()
    prefix = (list(ipaddress.ip_network(prefix).hosts()))
    #The format function pulls the ip to be used in the function
    format(prefix)
    for i in prefix:
        ip = (format(i))
        result = (os.system("ping -c 1 " + ip ))
        print(f"{result}")
        stop = timer()
        time = (stop - start)
        print(f"{time} seconds" )

#pingsweeper old but faster
def pingsweepold(prefix):
    start = timer()
    prefix = (list(ipaddress.ip_network(prefix).hosts()))
    #The format function pulls the ip to be used in the function
    format(prefix)
    for i in prefix:
        ip = (format(i))
        result = (os.system("ping -c 1 -n -W 2 " + ip ))
        if result:
            print (ip, 'inactive')
        else:
            print (ip, 'active')
    stop = timer()
    time = (stop - start)
    print(f"{time} seconds" )


#PingSweep2 is faster
def pingsweep(prefix):
    start = timer()
    with open(os.devnull, 'wb') as limbo:
        prefix = (list(ipaddress.ip_network(prefix).hosts()))
        format(prefix)
        for i in prefix:
            ip = (format(i))
            result=subprocess.Popen(['ping', '-c', '1', '-n', '-W', '2', ip], stdout=limbo, stderr=limbo).wait()
            if result:
                print (ip, 'active')
            else:
                print (ip, 'inactive')
        stop = timer()
        time = (stop - start)
        print(f"{time} seconds" )


#PingSweeper with timer
def pingsweep(prefix):
#Start a timer
    start = timer()
#This line uses a "special file" which redirects to discard
    with open(os.devnull, 'wb') as limbo:
#This line iterates over a prefix and returns all the hosts
        prefix = (list(ipaddress.ip_network(prefix).hosts()))
#Format returns the host ip address without the method attached
        format(prefix)
        for i in prefix:
            ip = (format(i))
#Ping , Count 1 , Numeric Output Only , Wait 2 Seconds
            result=subprocess.Popen(['ping', '-c', '1', '-n', '-W', '2', ip], stdout=limbo, stderr=limbo).wait()
            if result:
                print (ip, 'inactive')
            else:
                print (ip, 'active')
        stop = timer()
        time = (stop - start)
        print(f"{time} seconds" )










#Script to get  a reverse DNS record
def revdns(address):
    # Address = addr varable
    addr = address
    domain = socket.getfqdn(addr)
    if domain != addr:
        print (domain)
        return domain
    else:
        domain = (addr + " no revdns ")
        print (domain)
        return domain


#Check is an address is part of a network or supernet
def isSuperset(address,network):
    #Script checks is the supplied IP address is within a network checked against it
    try:
        a = ipaddress.ip_network(address)
        b = ipaddress.ip_network(network)
        result = a.subnet_of(b)
        return result
    except:
        #Issue with Supernet Check
        return False

#Subnetter Script
#Input a prefix and the number of subnet changes
#Subnetter("10.0.0.0/24",2)
def Subnetter(prefix,change):
    subnets = list(ipaddress.ip_network(prefix).subnets(prefixlen_diff=change))
    for i in subnets:
        print(i)