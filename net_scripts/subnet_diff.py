#Louis DeVictoria


#Script takes in a prefix and the amount of subnets you want to carve out
#Libraries

import ipaddress

def Subnetter(prefix,change):
    subnets = list(ipaddress.ip_network(prefix).subnets(prefixlen_diff=change))
    for i in subnets:
        print(i)

##Example Output

Subnetter("10.255.0.0/16",6)
