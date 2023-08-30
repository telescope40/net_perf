#!/python
import json
import sys
import matplotlib.pyplot as plt


def plot_http(httpjson):
	with open(httpjson, "r") as file:
		files = []
		download_speeds=[]
		download_sizes=[]
		download_times=[]
		for line in file:
			data = json.loads(line)
			dl_convert = (data['speed_download'])
			dl_size = (data["size_download"])
			dl_time = (data["total_time"])
			url = (data["url"])
			files.append(url)
			download_speeds.append(dl_convert)
			download_sizes.append(dl_size)
			download_times.append(dl_time)
		# Create bar chart
		plt.figure(figsize=(10, 6))
		plt.bar(download_sizes,download_times, color='blue', label='Download Size (MB)', width=0.4)

		# Create a bar chart for download times, aligning it to the right side of each file's bar
		#plt.bar(files, download_times, color='green', label='Time to Complete (s)', width=0.4)

		# Add title, labels, and legend
		plt.title('Download Size vs. Time to Complete for Different Files')
		plt.xlabel('Files')
		plt.ylabel('Size and Time')
		plt.legend()

		# Show the plot
		plt.tight_layout()
		plt.show()
		plt.savefig('http_graph.png', dpi=300)
		return plt.show()

if __name__ == "__main__":
	httpjson = sys.argv[1]
	plot_http(httpjson)
