# Louis DeVictoria
import socket
import json
import ipaddress
from ipwhois import IPWhois
import requests

class loud_iptools:
	def __init__(self, address):
		self.address = address
		if self._isIP() == True:
			return address
		elif self._isNet() == True:
			return address

	# Check if the address is valid
	def _isIP(self):
		address = self.address
		try:
			valid_ip = ipaddress.ip_address(address)
			return address
		except:
			return False
	def _isNet(self):
		prefix = self.address
		try:
			valid_net = ipaddress.ip_network(prefix)
			return prefix
		except:
			return False

	def _revdns(self):
		address = self.address
		try:
			domain = socket.getfqdn(address)
			if domain != address:
				return domain
			else:
				domain = (address + " no revdns ")
				return domain
		except:
			return "Error with _revdns"

	def _wholook(self):
		address = self.address
		obj = IPWhois(address)
		response = obj.lookup_whois()
		asn = response['asn']
		asn_desc = response['asn_description']
		ip = obj.address_str
		details = response['nets'][0]
		descrip = details['description']
		return({'Address': ip , "Announced By": asn , "ASN Description": asn_desc, "IP Owned": descrip })

	def _port_knock(self):
		address = self.address
		ports = [53,80,443,22]
		for port in ports:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((address,port))
			if result == 0:
				print(f"TCP port {port} open ")
			else:
				print(f"TCP port {port}  down ")
			sock.close()

	def _geo_loc(self):
		address = self.address
		url = (f"https://ipapi.co/{address}/json")
		get_location = requests.get(url)
		return get_location.json()

	def basic_subnet_cal(self):
		prefix = self.address
		all_hosts = (list(ipaddress.ip_network(prefix).hosts()))
		first_addr = all_hosts[0]
		last_addr = all_hosts[-1]
		broadcast = (ipaddress.ip_network(prefix).broadcast_address)
		net_address = (ipaddress.ip_network(prefix).network_address)
		numb_addrs = (ipaddress.ip_network(prefix).num_addresses)
		return (f'''First IP {first_addr},
		              Last IP {last_addr},  
		              Avaliable IPs {numb_addrs}''')

	def convert_bytes(number):
		#number is bytes#
		number = float(number)
		bits = number * 8
		kbits = bits / 1000
		mbits = kbits / 1000
		results = (f" {bits} bps | {kbits} kbps | {mbits} mbps ")
		return results
