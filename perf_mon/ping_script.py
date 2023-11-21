#Louis DeVictoria
import sys
import subprocess
import json
from datetime import datetime


all_servers = ["dallas.testmy.net","co3.testmy.net","fl.testmy.net","ny.testmy.net","sf.testmy.net","lax.testmy.net","toronto.testmy.net","uk.testmy.net","de.testmy.net","jp.testmy.net","sg.testmy.net","in.testmy.net","au.testmy.net","google.com","cloudflare.com","amazon.com"]
#all_servers =["192.168.28.20","172.17.0.28"]
#all_servers = ["3.78.89.137", "52.201.243.188"]
def ping_host(host):
	# For UNIX & Linux
	command = ['ping', '-c', '100', host]
	return subprocess.run(command, capture_output=True, text=True).stdout


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


if __name__ == "__main__":
	for server in all_servers:
		host = server
		response = ping_host(host)
		parsed_response = parse_ping_output(response)
		json_output = json.dumps(parsed_response, indent=4)
		with open("results/latency_results.json", "a") as json_file:
			json_file.write(json_output + "," + "\n")

