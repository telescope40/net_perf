# Louis DeVictoria
#!/python
# Performance Measurement Script

# Import Sensative Info
# from config.config import google_api, google_cse_id

# Import other Libraries
import os
import time
import json
import requests
import subprocess
import geoip2.database
import pandas as pd
import matplotlib.pyplot as plt

from netutils import dns
from haversine import haversine


def convert_bytes(number):
    # number is bytes#
    number = float(number)
    bits = number * 8
    kbits = bits / 1000
    mbits = kbits / 1000
    results = f" {bits} bps | {kbits} kbps | {mbits} mbps "
    return results


# Basic Ping Function
def ping_host(host):
    # For UNIX & Linux
    command = ["ping", "-c", "5", host]
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout


# MaxMing DB Lookup
def gps_location(address):
    path = "/Users/louis.devictoria/Desktop/MaxMind/GeoLite2-City.mmdb"
    with geoip2.database.Reader(path) as reader:
        response = reader.city(address)
        gps = (response.location.latitude, response.location.longitude)
        return gps


# Ping Parse Function
def parse_ping_output(output):
    lines = output.splitlines()
    data = {
        #'time': [],
        "host": [],
        "packets_transmitted": [],
        "packets_received": [],
        "packet_loss": [],
        "round_trip_avg": [],
        "stddev": [],
        #'percent': [],
        "max": [],
        "min": [],
    }

    for line in lines:
        if "PING" in line:
            host = line.split()[1]
        elif "packets transmitted" in line:
            packet_info = line.split(",")
            packets_transmitted = float(packet_info[0].split()[0])
            packets_received = float(packet_info[1].split()[0])
            packet_loss = packet_info[2].split()[0]
        elif "round-trip" in line:
            rtt_info = line.split("/")
            min_rtt = float(rtt_info[3].split("=")[1])
            avg_rtt = float(rtt_info[4])
            max_rtt = float(rtt_info[5])
            stddev = float(rtt_info[6].split()[0])
            percent = round((stddev / avg_rtt) * 100, 1)

            # Append to data
            # data['time'].append(time)
            data["host"].append(host)
            data["packets_transmitted"].append(packets_transmitted)
            data["packets_received"].append(packets_received)
            data["packet_loss"].append(packet_loss)
            data["round_trip_avg"].append(avg_rtt)
            data["stddev"].append(stddev)
            # data["percent"].append(percent)
            data["max"].append(max_rtt)
            data["min"].append(min_rtt)

    # Create DataFrame
    df = pd.DataFrame(data)
    # df = pd.DataFrame.from_dict(data, orient='index')
    return df


# API IP Query
def get_pub_ip():
    url = "http://ip.me"
    ip_me = requests.get(url, timeout=5)
    if ip_me.ok is True:
        ip = ip_me.text.strip()
        return ip
    else:
        return KeyError


# Query Geographical Location Info based on your IP
def geo_loc(ip):
    url = f"https://ipapi.co/{ip}/json"
    get_location = requests.get(url, timeout=5)
    return get_location.json()


# Create Google Search Function
# def search_google(api_key, cse_id, query):
#     url = "https://www.googleapis.com/customsearch/v1"
#     params = {"key": api_key, "cx": cse_id, "q": query}
#     response = requests.get(url, params=params, verify=False, timeout=5)
#
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None
#
#
# def result_google(city, region):
#     # You did need to create a custom Programmable search engine + API Key
#     # https://programmablesearchengine.google.com/controlpanel/all
#     jsonfile = "results/search.json"
#     API_KEY = google_api
#     CSE_ID = google_cse_id
#     QUERY = f"Closest pizza to {city} {region}."
#     results = search_google(API_KEY, CSE_ID, QUERY)
#     final = []
#
#     if results:
#         for item in results["items"]:
#             final.append((item["title"], item["link"]))
#         df = pd.DataFrame(final)
#         print(final)
#         df.to_json(jsonfile, orient="records", lines=True)
#         return final
#     else:
#         print("Error fetching results")
#         return "Error fetching results"


# Server IPs to GPS Mapping
def icmp_main(my_pubic_addr):
    sourceFile = "../config/ping_servers.json"
    filename = "results/latency_results.csv"
    jsonfile = "results/latency_results.json"
    local = gps_location(my_pubic_addr)

    server_dict = {
        "server_name": [],  # server,
        "ip_address": [],  # host_2_ip,
        "distance": [],  # Distance to me
        'ping':[],
        "packet_loss": [],
        "round_trip_avg": [],
        "stddev": [],
        "max": [],
        "min": [],
    }
    with open(sourceFile, "r", encoding="utf-8") as reader:
        all_servers = json.load(reader)
        for server in all_servers:
            try:
                # Resolve FQDN to IP
                host_2_ip = dns.fqdn_to_ip(server)

                # Resolve GPS Coordinates
                gps_host = gps_location(host_2_ip)

                # Distance from User to Server
                remote = gps_host
                kilos = round(haversine(local, remote))
                # kilos = (f"{kilos} Kilometers")

                # ICMP Testing
                response = ping_host(server)
                parsed_response = parse_ping_output(response)
                print(parsed_response)

                # Create the DataStructure
                server_dict["server_name"].append(server)
                server_dict["ip_address"].append(host_2_ip)
                server_dict["distance"].append(kilos)
                server_dict["packet_loss"].append(parsed_response["packet_loss"])
                server_dict["round_trip_avg"].append(parsed_response["round_trip_avg"])
                server_dict["stddev"].append(parsed_response["stddev"])
                server_dict["max"].append(parsed_response["max"])
                server_dict["min"].append(parsed_response["min"])
                server_dict['ping'].append(parsed_response)

            except Exception as e:
                print(f"Error processing server {server}: {e}")
                raise

        # Format the Dictionary to Pandas DataFrame
        df = pd.DataFrame(server_dict)
        # create json
        df.to_json(jsonfile, orient="records", lines=True)
        data = pd.read_json(jsonfile, lines=True)
        # create csv
        data.to_csv(filename, mode="w+", header=True, index=False)

        # Plot the Results
        # plot_ping()

        # Return the DataFrame
        return df


# Speedtest Python
def run_speedtest():
    try:
        jsonfile = "results/speedtest_results.json"
        results = subprocess.run(["speedtest-cli", "--json", ">>", "results/speedtest_results.json"], check=True)
        plot_speedtest(jsonfile)
        return results
    except ValueError as e:
        print("A ValueError occurred:", e)
        raise
    except TypeError as e:
        print("A TypeError occurred:", e)
        raise


def plot_speedtest(resultsfile):
    resultsfile = "results/speedtest_results.json"
    with open(resultsfile, "r") as file:
        timestamps = []
        download_speeds = []
        upload_speeds = []
        latencies = []
        for line in file:
            data = json.loads(line)
            # convert to Mbps <number> * 1e-6
            dl_convert = data["download"] * 1e-6
            up_convert = data["upload"] * 1e-6
            download_speeds.append(round(dl_convert))
            upload_speeds.append(round(up_convert))
            latencies.append((data["ping"]))
            timestamp = data["timestamp"]
            timestamps.append(timestamp.split("T")[1][0:8])
        plt.figure(figsize=(10, 6))
        plt.plot(
            timestamps, upload_speeds, marker="o", label="Upload (Mbps)", color="r"
        )
        plt.plot(
            timestamps, download_speeds, marker="o", label="Download (Mbps)", color="b"
        )
        # Create a secondary y-axis for latency
        ax2 = plt.gca().twinx()
        ax2.plot(
            timestamps,
            latencies,
            marker="x",
            label="Latency (ms)",
            color="g",
            linestyle="--",
        )
        ax2.set_ylabel("Latency (ms)")
        # Set labels and title
        plt.title("Network Speed and Latency over Time")
        plt.xlabel("Timestamp")
        plt.ylabel("Speed (Mbps)")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        # Combine legends from both axes
        lines, labels = plt.gca().get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc=0)
        plt.tight_layout()
        plt.savefig("results/speedtest_graph.png", dpi=300)


def web_load():
    filename = "results/website.csv"
    jsonfile = "results/website.json"
    all_sites = [
        "http://edition.cnn.com",
        "http://www.cloudflare.com",
        "http://www.github.com",
    ]
    # Log details
    log_details = {
        "http_code": [],  # response.status_code,
        "url": [],  # response.url,
        "size_download": [],  # len(response.content),
        "speed_download": [],  # len(response.content) / (end_time - start_time),
        "total_time": [],  # end_time - start_time
    }
    for url in all_sites:
        try:
            # Making the request
            start_time = time.time()
            response = requests.get(
                url, verify=False, timeout=5
            )  # `verify=False` is used for insecure requests
            end_time = time.time()

            # Log details
            log_details["http_code"].append(response.status_code)
            log_details["url"].append(response.url)
            log_details["size_download"].append(len(response.content))
            log_details["speed_download"].append(
                len(response.content) / (end_time - start_time)
            )
            log_details["total_time"].append(end_time - start_time)

        except ValueError as e:
            print("A ValueError occurred:", e)
        except TypeError as e:
            print("A TypeError occurred:", e)

    # Format the Dictionary to Pandas DataFrame
    print(log_details)
    df = pd.DataFrame(log_details)
    # create csv
    df.to_csv(filename, mode="w+", header=True, index=False)

    # Create json file
    df.to_json(jsonfile, orient="records", lines=True)
    # Create the Graph
    plot_http()
    # Return the DataFrame
    return df


def plot_ping():
    # Read the JSON file
    file_path = "results/latency_results.json"  # Replace with your file path
    data = pd.read_json(file_path, lines=True)

    # Extract round_trip_avg as it's nested in a list
#    data['round_trip_avg'] = data.ping.apply(lambda x: x[0][0]['round_trip_avg'] if x else None)
    data['round_trip_avg'] = data.ping.apply(lambda x: x[0]['round_trip_avg'] if x else None)

    # Sort the DataFrame based on 'distance'
    data_sorted = data.sort_values(by="distance")

    # Create the bar chart
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    plt.bar(data_sorted["server_name"], data_sorted["round_trip_avg"], color="skyblue")

    # Add labels and title
    plt.xlabel("Server Name")
    plt.ylabel("Round Trip Average (ms)")
    plt.title("Round Trip Average by Server Name Sorted by Distance")
    plt.xticks(rotation=45)  # Rotate the X-axis labels for better readability

    # Show the plot
    plt.tight_layout()
    plt.savefig("results/ping_graph.png", dpi=300)
    plt.show()


def plot_http():
    # Read the JSON file
    file_path = "results/website.json"  # Replace with your file path
    data = pd.read_json(file_path, lines=True)

    # Extract round_trip_avg as it's nested in a list
    # data['round_trip_avg'] = data['round_trip_avg'].apply(lambda x: x[0] if x else None)

    # Sort the DataFrame based on 'distance'
    data_sorted = data.sort_values(by="total_time")

    # Create the bar chart
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    plt.bar(data_sorted["url"], data_sorted["speed_download"], color="skyblue")

    # Add labels and title
    plt.xlabel("Site")
    plt.ylabel("Speed Download (ms)")
    plt.title("Download Speed by Site Sorted by total time")
    plt.xticks(rotation=45)  # Rotate the X-axis labels for better readability

    # Show the plot
    plt.tight_layout()
    plt.savefig("results/website_graph.png", dpi=300)
    plt.show()


def main():
    # Get Public IP Address
    my_pubic_addr = get_pub_ip()

    # Perform Speedtest CLI
    run_speedtest()

    # Perform Webpage Transaction Loads
    web_load()

    # Servers , Get List from Config , DNS Lookup , PING
    icmp_main(my_pubic_addr)

    # Plot Tests
    plot_ping()

    # Obtain GeoLocation on IP
    # where_am_i = geo_loc(my_pubic_addr)
    #
    # # City & Region
    # city = where_am_i["city"]
    # region = where_am_i["region"]
    #
    # # Run Google Query
    # result_google(city, region)

if __name__ == "__main__":
    main()
