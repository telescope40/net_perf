import json
import matplotlib.pyplot as plt
from geopy.distance import geodesic

def pingplot():
    # Read ping test results from the JSON file
    with open("results/latency_results.json", "r") as json_file:
        ping_results = json.load(json_file)

    # Extract relevant data for plotting
    timestamps = [result["time"] for result in ping_results]
    rtt_values = [result["round-trip"] for result in ping_results]
    distances = []

    # Source GPS coordinates (change these to your source coordinates)
    source_coordinates = (latitude_source, longitude_source)

    # Calculate distances for each destination
    for result in ping_results:
        dest_coordinates = (result["latitude"], result["longitude"])
        distance = geodesic(source_coordinates, dest_coordinates).kilometers
        distances.append(distance)

    # Create a scatter plot of ping results vs. distances
    plt.figure(figsize=(10, 6))
    plt.scatter(distances, rtt_values, c='b', marker='o', label='Ping Results')
    plt.xlabel('Distance (Kilometers)')
    plt.ylabel('Round-Trip Time (ms)')
    plt.title('Ping Test Results vs. Distance')
    plt.grid(True)
    plt.savefig('pingplot.png', dpi=300)

    # Annotate data points with host names
    for i, host in enumerate(ping_results):
        plt.annotate(host["host"], (distances[i], rtt_values[i]))



    plt.legend()
    plt.show()

if __name__ == "__main__":
	pingplot()
