

## Troubleshooting Slow Speeds / Issues 

Get Specific Information 
Source Public IP:
Destination Public IP: 
Protocol / Port: 


### Tools to use: 
- MTR
- iperf3
- scp 

**MTR**
Measure the path and latency to the destination 
```
mtr <destination_ip>
```



**iperf3**
Test the bandwidth between the servers
- One side is server ** <**iperf3 -s -p 5201 **>
- One side is the client <**iperf3 -c <server_ip> -p 5201 -R**>


**Test A Real File Transfer**
- Create a test file 
- SCP from the source -- destination server 
- Watch the transfer speed on the CLI 

```
scp 
 scp test.text root@<destination_ip>:/root/.
scp -6 test.text webair@[2a04:b40:5:101::30]:/root/.
```

#### Disable Firewall 
```
systemctl status firewalld
systemctl stop firewalld
```
