

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


Run MTR in report mode , wide , resolve ips , dns and ASN 
```commandline
mtr -bwrz -c 10 8.8.8.8

Start: 2023-03-09T20:39:33+0000
HOST: cloudmon-ctr-manilla                                                         Loss%   Snt   Last   Avg  Best  Wrst StDev
  1. AS140599 103.150.221.7                                                         0.0%    10    0.4   1.6   0.3   4.6   1.6
  2. AS140599 103.150.220.2                                                         0.0%    10    0.1   0.1   0.1   0.1   0.0
  3. AS9658   225.176.50.116.ids.service.static.eastern-tele.com (116.50.176.225)   0.0%    10    2.3   2.3   2.2   2.7   0.1
  4. AS9658   210.7.89.120.corenet.static.eastern-tele.com (120.89.7.210)           0.0%    10    3.6   2.4   2.2   3.6   0.4
  5. AS15169  72.14.195.70                                                          0.0%    10   31.5  32.4  31.5  35.4   1.3
  6. AS15169  108.170.240.161                                                       0.0%    10   31.9  31.9  31.8  32.0   0.0
  7. AS15169  142.251.241.1                                                         0.0%    10   32.0  31.9  31.8  32.0   0.0
  8. AS15169  dns.google (8.8.8.8)                                                  0.0%    10   31.8  31.8  31.8  31.9   0.0
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
