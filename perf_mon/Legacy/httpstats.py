#!/python
import json
import sys

def plot_httpstat(httpjson):
	with open(httpjson, "r") as file:
		total_time=[]
		download_speeds=[]
		download_sizes=[]
		download_times=[]
		for line in file:
			data = json.loads(line)
			dl_convert = (data['speed_download'])
			dl_size = (data["size_download"])
			dl_time = (data["time_connect"])
			times = (data["total_time"])
			download_speeds.append(dl_convert)
			download_sizes.append(dl_size)
			download_times.append(dl_time)
			total_time.append(times)
		#Convert String to floats
		download_times = [float(x) for x in download_times]
		total_time = [float(x) for x in total_time]
		#Convert Bytes to Bits
		download_speeds = [x/125000 for x in download_speeds]
		#Perform Average
		avgTT = sum(total_time) / len(total_time)
		avgConn = sum(download_times) / len(download_times)
		avgDown = sum(download_speeds) / len(download_speeds)
		print (f"Avg Conn {avgConn} Seconds")
		print (f"Avg Speed  {avgDown} Mbps")
		print(f"Avg Total Time  {avgTT} Seconds")

if __name__ == "__main__":
	httpjson = sys.argv[1]
	plot_httpstat(httpjson)
