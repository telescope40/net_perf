#Louis DeVictoria
# 2023 Script to run whois over list of address and check if a service port is open
from ipwhois import IPWhois
import socket
import threading


def wholook(address):
	obj = IPWhois(address)
	response = obj.lookup_whois()
	asn = response['asn']
	asn_desc = response['asn_description']
	ip = obj.address_str
	details = response['nets'][0]
	descrip = details['description']
	print({'Address': ip , "Announced By": asn , "ASN Description": asn_desc, "IP Owned": descrip })
	final = {f'Address: {ip} ,Announced By: {asn} , ASN Description: {asn_desc}, IP Owned: {descrip}'}
	a = open("../Txt_files/whois_post.txt", "a+")
	a.writelines(final)
	a.writelines("\n")

def port_knock(address):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 53
	result = sock.connect_ex((address,port))
	if result == 0:
		print(f"TCP port {port} open ")
	else:
		print(f"TCP port {port}  down ")
	sock.close()

if __name__ == "__main__":
	f = open("../Txt_files/whois.txt", "r")
	for x in f:
		x = x.strip()
		wholook(x)
		port_knock(x)


