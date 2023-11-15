#Python3
#Louis DeVictoria
import requests
from shodan import Shodan
from config import config


def get_pub_ip():
	url = (f"http://ip.me")
	ip_me = requests.get(url)
	if ip_me.ok is True:
		ip = ip_me.text.strip()
		return ip
	else:
		return KeyError

ip = get_pub_ip()
print(ip)

api = Shodan(config.api_sh)

# Lookup an IP
ipinfo = api.host(ip)
print(ipinfo)

# Search for websites that have been "hacked"
for banner in api.search_cursor('http.title:"hacked by"'):
    print(banner)

# Get the total number of industrial control systems services on the Internet
ics_services = api.count('tag:ics')
print('Industrial Control Systems: {}'.format(ics_services['total']))
