#!/python
import json
import sys
import matplotlib.pyplot as plt


def plot_speedtest(resultsfile):
	with open(resultsfile, "r") as file:
		timestamps=[]
		download_speeds=[]
		upload_speeds=[]
		latencies=[]
		for line in file:
			data = json.loads(line)
			#convert to Mbps <number> * 1e-6
			dl_convert = ((data['download'] * 1e-6))
			up_convert = ((data['upload'] * 1e-6))
			download_speeds.append(round(dl_convert))
			upload_speeds.append(round(up_convert))
			latencies.append((data['ping']))
			timestamp = ((data['timestamp']))
			timestamps.append(timestamp.split("T")[1][0:8])
		plt.figure(figsize=(10, 6))
		plt.plot(timestamps, upload_speeds, marker='o', label='Upload (Mbps)', color='r')
		plt.plot(timestamps, download_speeds, marker='o', label='Download (Mbps)', color='b')
		# Create a secondary y-axis for latency
		ax2 = plt.gca().twinx()
		ax2.plot(timestamps, latencies, marker='x', label='Latency (ms)', color='g', linestyle='--')
		ax2.set_ylabel('Latency (ms)')
		# Set labels and title
		plt.title('Network Speed and Latency over Time')
		plt.xlabel('Timestamp')
		plt.ylabel('Speed (Mbps)')
		plt.grid(True, which='both', linestyle='--', linewidth=0.5)
		# Combine legends from both axes
		lines, labels = plt.gca().get_legend_handles_labels()
		lines2, labels2 = ax2.get_legend_handles_labels()
		ax2.legend(lines + lines2, labels + labels2, loc=0)
		plt.tight_layout()
		plt.savefig('speedtest_graph.png', dpi=300)
		#return plt.show()

if __name__ == "__main__":
	resultsfile = sys.argv[1]
	plot_speedtest(resultsfile)
