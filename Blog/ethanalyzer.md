



### Brief Backstory 
What attracted me into technology is the problem solving aspect of it. It's a personal driver that has sustained me in my profession. 
Using the proper tools is a great way to help solve a mystery. In this particular instance , my colleague and I were reviewing something simple ... The network was not learning any Layer 2 Addressing from the new storage boxes trunked over. 
Seems like a really easy item to configure right? 
Since the links did show multicast traffic across it and Refusing to give us , I decided to revisit **Ethanalyzer**

### Technical Description 
Ethanalyzer is the NX-OS flavor of Tshark , which is the terminal version of Wireshark.  Ethanalyzer can capture inband and management traffic and filter packets. What is interesting is you can use both tcpdump or wireshark capture syntax . 

### Hurry up ! I need to troubleshoot !
Yes , I wrote this because I could not figure out how to filter results quickly. 
Filtering packets is where I got stopped briefly because there is 
- **display-filter**
	- *display-filter == wireshark*
- **capture-filter**
	- *capture-filter == tcpdump* 



##### Wireshark Display Filter  
```
Wireshark / Display Filter 

nxos# ethanalyzer local interface inband display-filter "tcp.port == 179" limit-captured-frames 400
Capturing on inband
2022-08-13 12:44:42.153103    10.1.1.53 -> 10.1.1.52    BGP KEEPALIVE Message
2022-08-13 12:44:42.153116    10.1.2.53 -> 10.1.2.52    BGP KEEPALIVE Message


Filter by MAC Address 
```ethanalyzer local interface inband display-filter "eth.addr eq 00:50:56:01:0a:a8" ```

Filter by Vlan ID 
``` ethanalyzer local interface inband display-filter "vlan.id eq 3902" limit-captured-frames 400```

- Filter by IP Address
``` ethanalyzer local interface inband display-filter "ip.addr eq 192.168.21.160" limit-captured-frames 400```


```

##### TCPDUMP Capture Filter  
```
TCPDUMP / Display Filter 
nxos# ethanalyzer local interface inband capture-filter "tcp port 179" 
Capturing on inband
2022-08-13 12:46:13.741855    10.1.3.52 -> 10.1.3.53    BGP KEEPALIVE Message
2022-08-13 12:46:13.741916  10.200.0.15 -> 10.200.200.27 BGP KEEPALIVE Message
```

##### Capture Output to a file
The display at the end will output the content while capturing 
```
ethanalyzer local interface inband write bootflash:///20220813.pcap display 
Capturing on inband
2022-08-13 13:22:27.280908    10.1.1.52 -> 10.1.1.53    BGP KEEPALIVE Message
2022-08-13 13:22:27.280972    10.1.1.53 -> 10.1.1.52    TCP bgp > 55311 [ACK] Seq=1 Ack=20 Win=7280 Len=0 TSV=931077017 TSER=2303421976
```

##### Read the output of the pcap 
```
nxos# ethanalyzer local read bootflash:///20220813.pcap
2022-08-13 13:22:27.280908    10.1.1.52 -> 10.1.1.53    BGP KEEPALIVE Message
2022-08-13 13:22:27.280972    10.1.1.53 -> 10.1.1.52    TCP bgp > 55311 [ACK] Seq=1 Ack=20 Win=7280 Len=0 TSV=931077017 TSER=2303421976
2022-08-13 13:22:27.280986  10.200.0.13 -> 10.200.200.27 BGP KEEPALIVE Message
2022-08-13 13:22:27.281002 10.200.200.27 -> 10.200.0.13  TCP 39174 > bgp [ACK] Seq=1 Ack=20 Win=30477 Len=0 TSV=931077017 TSER=2303421976
2022-08-13 13:22:27.343513 00:35:1a:9d:ab:ef -> 01:80:c2:00:00:00 STP RST. Root = 32768/1/00:23:04:ee:be:64  Cost = 0  Port = 0x9063
2022-08-13 13:22:27.343566 00:35:1a:9d:ab:ef -> 01:00:0c:cc:cc:cd STP RST. Root = 32768/1/00:23:04:ee:be:64  Cost = 0  Port = 0x9063
2022-08-13 13:22:27.343601 00:35:1a:9d:ab:ef -> 01:00:0c:cc:cc:cd STP RST. Root = 32768/745/00:23:04:ee:be:64  Cost = 0  Port = 0x9063
2022-08-13 13:22:27.674072    10.1.3.52 -> 10.1.3.53    BGP KEEPALIVE Message
2022-08-13 13:22:27.674138    10.1.3.53 -> 10.1.3.52    TCP bgp > 33813 [ACK] Seq=1 Ack=20 Win=7280 Len=0 TSV=931077135 TSER=2303326167
2022-08-13 13:22:27.674151  10.200.0.15 -> 10.200.200.27 BGP KEEPALIVE Message
```

### Ultimately 
The root cause of the issue ended up being a misconfigured route map which prevented traffic between the overlays.  While Ethanalyzer did not directly solve the problem , where I found this helpful was in using to troubleshoot connectivity in my new overlay networks. 
In my previous experience with *Ethanalyzer* , I was reluctant to use it because I did not know to filter. Even in one of the Cisco press books . 
```
While using Ethanalyzer, specifying the filters is easier for someone who is familiar with Wireshark filters. The syntax for both the capture filter and the display filter is different. Table 2-1 lists some of the common filters and their syntax with the **capture-filter** and **display-filter** options.
```

While the author does explain great technical material its the above paragraph that I wish contained the terse point of *display-filter == wireshark* , *capture-filter == tcpdump*.

I want to thank Ivan Shirshin who wrote a community blog post in **2013** that made this information clear as day to me. This allowed me to use Ethanalyzer effectively. 


### Citing my sources / links 
- Wireshark Display Filters Man Page
	- https://www.wireshark.org/docs/man-pages/wireshark-filter.html
- Cisco Community Post from Ivan Shirshin 
	- https://community.cisco.com/t5/networking-knowledge-base/using-ethanalyzer-on-nexus-platform-for-control-plane-and-data/ta-p/3142665
- TCPDUMP Man Page 
	- https://www.tcpdump.org/manpages/tcpdump.1.html
- Cisco NX-OS Troubleshooting 
	- https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/troubleshooting/guide/b_Cisco_Nexus_9000_Series_NX-OS_Troubleshooting_Guide/b_Cisco_Standalone_Series_NX-OS_Troubleshooting_Guide_chapter_010000.html#reference_EF208AE32A30415F8F172A5E417868A8
- Cisco Press Books 
	- https://www.ciscopress.com/articles/article.asp?p=2928194&seqNum=2
