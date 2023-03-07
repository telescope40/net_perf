# Louis DeVictoria
import ipaddress

def basic_subnet_cal(prefix):
	all_hosts = (list(ipaddress.ip_network(prefix).hosts()))
	first_addr = all_hosts[0]
	last_addr = all_hosts[-1]
	broadcast = (ipaddress.ip_network(prefix).broadcast_address)
	net_address = (ipaddress.ip_network(prefix).network_address)
	numb_addrs = (ipaddress.ip_network(prefix).num_addresses)
	result = (f'''
Network Address: {net_address}
First Address: {first_addr}
Last Address {last_addr},  
Broadcast {broadcast}
Available IPs {numb_addrs}''')
	print(result)

