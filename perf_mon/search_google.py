# Louis DeVictoria
#!/python
import requests
from config.config import google_api , google_cse_id

def get_pub_ip():
	url = (f"http://ip.me")
	ip_me = requests.get(url)
	if ip_me.ok is True:
		ip = ip_me.text.strip()
		return ip
	else:
		return KeyError

#Get my Public IP Address
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

# Use Public IP Info to determine Geographic Specifics
my_pubic_addr = get_pub_ip()
where_am_i = geo_loc(my_pubic_addr)
city = where_am_i['city']
region = where_am_i['region']

#You did need to create a custome Programmable search engine + API Key
# https://programmablesearchengine.google.com/controlpanel/all

API_KEY = google_api
CSE_ID = google_cse_id
QUERY = (f'Closest Pizza near {city} + ,{region}')



results = search_google(API_KEY, CSE_ID, QUERY)
if results:
	for item in results['items']:
		print(item['title'], item['link'])
else:
	print("Error fetching results")

