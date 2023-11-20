# Louis DeVictoria
#!/python
# Performance Measurement Script

import requests
from config.config import google_api , google_cse_id
import concurrent.futures
import subprocess
import json
from datetime import datetime
import geoip2.database
from netutils import dns
from haversine import haversine, Unit
from perf_mon.stplot import plot_speedtest
import os

# Basic Ping Function
def ping_host(host):
	# For UNIX & Linux
	command = ['ping', '-c', '10', host]
	return subprocess.run(command, capture_output=True, text=True).stdout


# MaxMing DB Lookup
def gps_location(address):
	path = '/Users/louis.devictoria/Desktop/MaxMind/GeoLite2-City.mmdb'
	with geoip2.database.Reader(path) as reader:
		response = reader.city(address);
		gps = (response.location.latitude, response.location.longitude)
		return gps

# Ping Parse Function
def parse_ping_output(output):
	time = datetime.now().isoformat()
	lines = output.splitlines()
	results = {
		'time': time,
		'host': None,
		'packets_transmitted': None,
		'packets_received': None,
		'packet_loss': None,
		'round-trip': None,
		'stddev': None,
		'percent': None,
		'max': None,
		'min': None
	}

	for line in lines:
		if "PING" in line:
			results['host'] = line.split()[1]
		elif "packets transmitted" in line:
			data = line.split(',')
			results['packets_transmitted'] = float(data[0].split()[0])
			results['packets_received'] = float(data[1].split()[0])
			results['packet_loss'] = data[2].split()[0]
		elif "round-trip" in line:
			data = line.split("/")
			results['min'] = float(data[3].split("=")[1])
			results['round-trip'] = float(data[4])
			rtt = float(data[4])
			std = float(data[6].split()[0])
			results['max'] = float(data[5])
			results['stddev'] = float(data[6].split()[0])
			perc = float((std/rtt) * 100)
			perc = round(perc ,1)
			results['percent'] = perc
			print(f"{rtt} ms Average | {perc}% deviation ({std}ms)")
	return results

# API IP Query
def get_pub_ip():
	url = (f"http://ip.me")
	ip_me = requests.get(url)
	if ip_me.ok is True:
		ip = ip_me.text.strip()
		return ip
	else:
		return KeyError


# Query Geographical Location Info based on your IP
def geo_loc(ip):
	url = (f"https://ipapi.co/{ip}/json")
	get_location = requests.get(url)
	return get_location.json()


#Create Google Search Function
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

def result_google(city,region):
	# You did need to create a custome Programmable search engine + API Key
	# https://programmablesearchengine.google.com/controlpanel/all
	API_KEY = google_api
	CSE_ID = google_cse_id
	QUERY = (f'Closest pizza to {city} + ,{region}')
	results = search_google(API_KEY, CSE_ID, QUERY)
	final = []

	if results:
		for item in results['items']:
			final.append((item['title'], item['link']))
		print(final)
		return final
	else:
		print("Error fetching results")
		return ("Error fetching results")


# Server IPs to GPS Mapping
def servers_gps():
	sourceFile = "../config/ping_servers.json"
	server_list=[]
	with open(sourceFile, "r") as reader:
		all_servers = json.load(reader)
		for server in all_servers:
			try:
				host_2_ip = dns.fqdn_to_ip(server)
				gps_host = gps_location(host_2_ip)
				#server_dict[server] = [host_2_ip,gps_host]
				server_dict = {
					"server_name": server,
					"ip_address": host_2_ip,
					"gps_location": gps_host
				}
				server_list.append(server_dict)
				gps_output = json.dumps(server_list, indent=4)
			except Exception as e:
				print(f"Error processing server {server}: {e}")

		filename = "gps_results.json"
		with open(filename, "w+") as json_file:
			json_file.write(gps_output + "\n")
		return filename

# Get Distnace between Server
def servers_distance(gps_coordinates):
	local = gps_coordinates
	filename = "gps_results.json"
	with open(filename, "r") as json_file:
		data = json.load(json_file)
		for i in range(len(data)):
			try:
				server = (data[i]["server_name"])
				remote = (data[i]["gps_location"])
				distance = haversine(local, remote)
				print(f"My distnace to {server} is {distance} KMs")
			except Exception as e:
				print(f"Error processing server {i}: {e}")
				continue

def ping_pong():
	sourceFile = "../config/ping_servers.json"
	with open(sourceFile, "r") as reader:
		all_servers = json.load(reader)
		filename = "latency_results.json"
		for server in all_servers:
			try:
				host = server
				response = ping_host(host)
				parsed_response = parse_ping_output(response)
				print(parsed_response)
				json_output = json.dumps(parsed_response, indent=4)
				with open(filename, "a+") as json_file:
					json_file.write(json_output + "," + "\n")
					#return(json_output)
			except Exception as e:
				print(f"Error processing server {server}: {e}")
				continue

	return filename


# Speedtest Python
def run_speedtest():
	try:
		st_result = os.system("speedtest --simple --json")
		print(st_result)
		return(st_result)
	except Exception as e:
		print(f"An error occurred: {e}")
		return(f"An error occurred: {e}")


def main():
# Use Public IP Info to determine Geographic Specifics
	my_pubic_addr = get_pub_ip()

# Get GPS of myIP
	gps_coordinates = gps_location(my_pubic_addr)
	print(gps_coordinates)

#Get Servers GPS
	#servers_gps()

# Get Distances between my local IP and the servers
	servers_distance(gps_coordinates)

# Plot Tests
	#pingplot()

#Obtain GeoLocation on IP
	where_am_i = geo_loc(my_pubic_addr)

# City & Region
	city = where_am_i['city']
	region = where_am_i['region']

# Run Google Query
	result_google(city, region)

# Run Speedtest
	run_speedtest()

# Run Ping Testing
	ping_pong()

if __name__ == "__main__":
	main()





