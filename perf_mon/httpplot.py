#!/python
import json
import sys
import matplotlib.pyplot as plt
import numpy as np


def plot_http(httpjson):
	with open(httpjson, "r") as file:
		urls=[]
		download_speeds=[]
		download_sizes=[]
		download_times=[]
		for line in file:
			data = json.loads(line)
			dl_convert = (data['speed_download'])
			dl_size = (data["size_download"])
			dl_time = (data["total_time"])
			url = (data["url"])
			urls.append(url)
			download_speeds.append(dl_convert)
			download_sizes.append(dl_size)
			download_times.append(dl_time)
		# Create a line graph for download sizes
		plt.figure(figsize=(12, 7))
		plt.plot(urls, download_sizes, color='blue', marker='o', label='Download Size (KB)')

		# Create a line graph for total times
		plt.plot(urls, download_times, color='green', marker='x', label='Total Time (s)')

		# Add title, labels, and legend
		plt.title('Download Size vs. Total Time for Different URLs')
		plt.xlabel('URLs')
		plt.ylabel('Size and Time')
		plt.legend()
		plt.grid(True, which="both", ls="--", linewidth=0.5)
		plt.tight_layout()

		plt.savefig('http_graph.png', dpi=300)
		return plt.show()

if __name__ == "__main__":
	httpjson = sys.argv[1]
	plot_http(httpjson)
