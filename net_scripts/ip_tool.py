# Louis DeVictoria
import socket
import json
import ipaddress
from ipwhois import IPWhois
import requests
from config import config
import geoip2
from haversine import haversine, Unit
impport numpy

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

	def search_google(api_key, cse_id, query):
		url = "https://www.googleapis.com/customsearch/v1"
		params = {
			'key': api_key,
			'cx': cse_id,
			'q': query
		}

		response = requests.get(url, params=params, verify=False)

		if response.status_code == 200:
			return response.json()
		else:
			return None


	def _gps_location(self):
		address = self.address
		with geoip2.database.Reader('Desktop/MaxMind/GeoLite2-City.mmdb') as reader:
			response = reader.city(address);
			gps = (response.location.latitude, response.location.longitude)
			return gps


    - 159.89.177.46
    - 157.245.83.95
    - 128.199.198.194
    - 143.110.242.25
    - 170.64.216.139

geoip2.models.City({'city': {'geoname_id': 5393015, 'names': {'de': 'Santa Clara', 'en': 'Santa Clara', 'es': 'Santa Clara', 'fr': 'Santa Clara', 'ja': 'サンタクララ', 'pt-BR': 'Santa Clara', 'ru': 'Санта-Клара', 'zh-CN': '圣克拉拉'}}, 'continent': {'code': 'NA', 'geoname_id': 6255149, 'names': {'de': 'Nordamerika', 'en': 'North America', 'es': 'Norteamérica', 'fr': 'Amérique du Nord', 'ja': '北アメリカ', 'pt-BR': 'América do Norte', 'ru': 'Северная Америка', 'zh-CN': '北美洲'}}, 'country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'Vereinigte Staaten', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États Unis', 'ja': 'アメリカ', 'pt-BR': 'EUA', 'ru': 'США', 'zh-CN': '美国'}}, 'location': {'accuracy_radius': 20, 'latitude': 37.3931, 'longitude': -121.962, 'metro_code': 807, 'time_zone': 'America/Los_Angeles'}, 'postal': {'code': '95054'}, 'registered_country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'Vereinigte Staaten', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États Unis', 'ja': 'アメリカ', 'pt-BR': 'EUA', 'ru': 'США', 'zh-CN': '美国'}}, 'subdivisions': [{'geoname_id': 5332921, 'iso_code': 'CA', 'names': {'de': 'Kalifornien', 'en': 'California', 'es': 'California', 'fr': 'Californie', 'ja': 'カリフォルニア州', 'pt-BR': 'Califórnia', 'ru': 'Калифорния', 'zh-CN': '加州'}}], 'traits': {'ip_address': '164.92.114.110', 'prefix_len': 19}}, ['en'])
