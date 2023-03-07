#Louis DeVictoria


#Script takes in a prefix and the amount of subnets you want to carve out
#Libraries

import ipaddress

def Subnetter(prefix,change):
    subnets = list(ipaddress.ip_network(prefix).subnets(prefixlen_diff=change))
    for i in subnets:
        print(i)

##Example Output

Subnetter("10.0.0.0/24",2)
10.0.0.0/26
10.0.0.64/26
10.0.0.128/26
10.0.0.192/26
