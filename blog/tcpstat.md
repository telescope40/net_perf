Recently I was troubleshooting some performance issues for a VPN setup. 
What I observed was a gateway with multiple IPSEC tunnels having slow speeds. 
Investigation of the issue demonstrated monitoring that as VPN traffic increases , CPU on the gateway spiked. 
The bandwidth itself was not the underlyinng cause 
Investigating the issues I needed some real time monitoring and after a long career of using Cisco boxes I was left with 
needing to see output on a Linux box in term of bits per second in order to understand the correct load in real time 
tcpstat 

TCPSTAT Written by  Paul Herman in 1998 was a nice quick tool to pull this data . I was able to quickly download and 
set up some familar output 
``` tcpstat -i eth0 -o "Intf Load=%l | avg_packet_size_bytes=%a | bps=%b | tcp=%T | udp=%U  | num_packets=%n | pps=%p```
https://manpages.ubuntu.com/manpages/trusty/man1/tcpstat.1.html

This information helped me confirm that a VPN running at 30 Mbps was triggering a container CPU to spike . Next step 
investigate 


https://infosecmonkey.com/what-diffie-hellman-dh-group-should-i-use/
