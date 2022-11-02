# How to programatically connect to a RTSP camera URL remotely with OpenCV-Python

Accessing a RTSP cam stream from a remote site with ````opencv````, requires two basic computers, e.g. rpi3s, one in each LAN.

[Remote RTSP LAN access setup](https://www.sensoranalytics.com.au/misc/Sof.jpg)

A serial vpn link is setup between the two rpis with the following commands on the remote rpi.

Install ````ppp```` package on both the rpis:
````
sudo apt update
sudo apt upgrade
sudo apt install ppp
````

````vpn-s````

````
#/bin/bash
# vpn-s script sets up a point-to-point vpn between remote computer 
# and home LAN. The usrname should be usrname of a computer on home
# LAN with sudo access.
# Run this script on remote computer
sudo /usr/sbin/pppd updetach connect-delay 60000 noauth pty\
 "sudo -u usrname /usr/bin/ssh -t -t home_router_ip -l usrname\
  -p home_router_port_no_fwd_to_ipcam\
  sudo /usr/sbin/pppd noauth 192.168.186.2:192.168.186.1"
````

````fwdonremote````
````
#!/bin/bash
# Edit in below your actual local, i.e. home, LAN address (as provided by ISP).
#start ssh vpn first (vpn-s) then run this script on remote computer.
sudo ip r add 192.168.1.0/24 dev ppp0
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
````

```` fwdonlocal ````
````
#!/bin/bash
# Edit in below your actual remote LAN address (as provided by ISP).
#After ssh vpn has been established by remote run this script here on
#the local computer.
sudo ip route add 192.168.0.0/24 dev ppp0
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
````

Install the following ````python```` packages if not previously installed on remote rpi.

````
pip install --upgrade pip
pip install numpy
pip install opencv-python
````

Running ```` open_uri.py```` with your own camera rtsp://url edited in should connect to the ipcam on home LAN and open a display window in the remote rpi. 

**Note:** If remote rpi is running in headless mode, connection to it should be made with X forwarding enabled to access the display say with ````ssh -XY rpi3-remote````.

### Troubleshooting
````vpn-s```` requires the ````ssh```` login from remote rpi to local rpi is passwordless with no keyboard interaction. The ````sudo```` command on local rpi is also passwordless with no keyboard interacion.

````fwdon```` scripts require the ````iptables```` on both the rpis are in their default setting before use, which can be set as:
```` 
sudo iptables -F
sudo -t nat -F
````

