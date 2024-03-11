# Louis DeVictoria
#!/python
# Performance Measurement Script

# Import other Libraries
import os
import time
import json
import requests

requests.packages.urllib3.disable_warnings()
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
        try:
            # Run the ping command
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            # If ping is successful, return the standard output
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            # If ping fails (ICMP does not reply, host is unreachable, etc.)
            # return the standard error output and indicate failure
            return {"success": False, "output": e.stderr if e.stderr else e.stdout}

# MaxMing DB Lookup
def gps_location(address):
    path = "../config/GeoLite2-City.mmdb"
    with geoip2.database.Reader(path) as reader:
        response = reader.city(address)
        gps = (response.location.latitude, response.location.longitude)
        return gps


# Ping Parse Function
def parse_ping_output(output_dict):
    # Extract the output string from the dictionary
    output = output_dict['output']
    lines = output.splitlines()
    data = {
        "host": None,
        "packets_transmitted": None,
        "packets_received": None,
        "packet_loss": None,
        "round_trip_min": None,
        "round_trip_avg": None,
        "round_trip_max": None,
        "round_trip_mdev": None,
    }

    for line in lines:
        if "PING" in line:
            data["host"] = line.split()[2].strip("()")
        elif "packets transmitted" in line:
            packet_info = line.split(", ")
            data["packets_transmitted"] = int(packet_info[0].split()[0])
            data["packets_received"] = int(packet_info[1].split()[0])
            data["packet_loss"] = packet_info[2].split()[0]
        elif "min/avg/max/mdev" in line:
            rtt_info = line.split("=")[1].split("/")
            data["round_trip_min"] = float(rtt_info[0])
            data["round_trip_avg"] = float(rtt_info[1])
            data["round_trip_max"] = float(rtt_info[2])
            data["round_trip_mdev"] = float(rtt_info[3].split()[0])

    # Since the structure expects lists but we have single values, we encapsulate values in lists to maintain consistency
    for key in data:
        data[key] = [data[key]]

    # Create DataFrame
    df = pd.DataFrame(data)
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
        "ping": [],
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
                server_dict["stddev"].append(parsed_response["round_trip_mdev"])
                server_dict["max"].append(parsed_response["round_trip_max"])
                server_dict["min"].append(parsed_response["round_trip_min"])
                server_dict["ping"].append(parsed_response)

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
        plot_ping()

        # Return the DataFrame


# Speedtest Python
def run_speedtest():
    try:
        results = subprocess.run(
            "speedtest-cli --json >> results/speedtest_results.json",
            shell=True,
            check=True,
            capture_output=True,
        )
        jsonfile = "results/speedtest_results.json"
        plot_speedtest(jsonfile)
        return results.stdout
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
    data["round_trip_avg"] = data.ping.apply(
        lambda x: x[0]["round_trip_avg"] if x else None
    )

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
    # plt.show()
    return None


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
    # plt.show()
    return None


def main():
    # Get Public IP Address
    my_pubic_addr = get_pub_ip()

    # Perform Speedtest CLI
    #run_speedtest()

    # Perform Webpage Transaction Loads
    web_load()

    # Servers , Get List from Config , DNS Lookup , PING
    icmp_main(my_pubic_addr)


if __name__ == "__main__":
    main()
