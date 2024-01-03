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
		# Convert total_times to milliseconds
		# Plot average download speeds
		# Setup figure and subplots
		urls = [x[8:16] for x in urls]
		fig, axs = plt.subplots(3, 1, figsize=(10, 10))

		# Bar positions
		bar_positions = np.arange(len(urls))

		# Plot average download speeds
		axs[0].bar(bar_positions, download_speeds, color='blue', alpha=0.7)
		axs[0].set_title('Average Download Speeds')
		axs[0].set_ylabel('Speed (MB/s)')
		axs[0].set_xticks(bar_positions)
		axs[0].set_xticklabels([])  # Hide x-tick labels for the first two plots

		# Plot file sizes
		axs[1].bar(bar_positions, download_sizes, color='green', alpha=0.7)
		axs[1].set_title('File Sizes')
		axs[1].set_ylabel('Size (MB)')
		axs[1].set_xticks(bar_positions)
		axs[1].set_xticklabels([])

		# Plot time to complete
		axs[2].bar(bar_positions, download_times, color='red', alpha=0.7)
		axs[2].set_title('Time to Complete Downloads')
		axs[2].set_ylabel('Time (s)')
		axs[2].set_xlabel('URLs')
		axs[2].set_xticks(bar_positions)
		axs[2].set_xticklabels(urls, rotation=45)

		plt.savefig('http_graph.png', dpi=300)
		#return plt.show()

if __name__ == "__main__":
	httpjson = sys.argv[1]
	plot_http(httpjson)
