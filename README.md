# PIAScript

Small Python script which enables port forwarding for a PIA VPN and prints the forwarded port.

Now finished but not perfect, personal project, etc.

I do not use this for illegal downloading. I don't condone that, don't do that, etc.

Usage
- -h, --help: Show help.
- credentialsfile: Mandatory first argument, file that contains PIA API credentials (see PIA link below).

Credentials File:
- See: https://www.privateinternetaccess.com/forum/discussion/180/port-forwarding-without-the-application-advanced-users to create a client id and for API documentation.
- Expected file format:
- 
    Line 1: [PIA username]

    Line 2: [PIA password]
    
    Line 3: [PIA client id]
    
Dependancies
- Python 3
- The Python 3 netifaces library (look for a package for your distribution or use Python's easy_install).

This script will:
- Check if the VPN is connected (tun0 interface is active).
- Read PIA API credentials from a file (path provided as a command line parameter).
- Post to the PIA API endpoint in order to forward a port.
- Print the forwarded port number. 

Notes and issues:
- This is my first Python program, made in my spare time.
- This script will not work for other VPN providers as is.
- API erros are checked in a very basic way but the API documentation does not list any specific errors.
- Exception handling with file I/O could be better but I had issues with "with using" and "try/catch/finally".
- The PIA API seems to return an out of date port number sometimes. The API documentation is very threadbare but there seems to be no way for me to fix this. Try waiting a few minutes and running it again.
- I removed ufw firewall and transmission functionality to simplify the script's purpose adn because I don't use them anymore.
- This script should be portable now that I changed the network querying to use the netifaces library and removed the use of GNU/Linux command line tools.

Other steps:
- I use an iptables based vpn kill-switch script: http://forum.ibvpn.com/topic/9-vpn-openvpn-firewall-killswitch-for-linux-users/ , https://gist.github.com/adrelanos/10565852 =
- You will have to update the INTERFACE variable if your VPN is using an interface other than tun0 (Open VPN and the official PIA appplication both use tun0 by default).

