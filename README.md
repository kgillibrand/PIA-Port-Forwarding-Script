# PIAScript
Small Python script forwards a port for a Private Internet Access vpn and prints the forwarded port.

Now finished but not perfect, personal project, etc.

Usage
- -h, --help: Show help
- credentialsfile: Mandatory first argument, file that contains PIA API credentials (see PIA link below).

Credentials File:
- See: https://www.privateinternetaccess.com/forum/discussion/180/port-forwarding-without-the-application-advanced-users to create a client id and for API documentation
- Expected file format:
    Line 1: [PIA username]

    Line 2: [PIA password]
    
    Line 3: [PIA client id]
    
This script will:
- Check if the VPN is connected (tun0 interface exists).
- Read PIA API credentials from a file (path provided as a command line parameter).
- Post to the PIA API endpoint in order to forward a port.
- Print the forwarded port number. 
 
Notes and issues:
- Finding your local ip in Python is troublesome without libraries, the method I found online and used is very flaky (https://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/).
- This script calls some Linux command line functions and is not portable.
- This is my first Python program and first use of JSON, made in my spare time.
- This script will not work for other VPN providers as is
- This script will kill Transmission to update it's settings file, it will not restart it (the script reminds you).
- API erros are checked in a very basic way, true JSON parsing for the response would be better.
- Exception handling with file I/O could be better but I had issues with "with using" and "try/catch/finally"
- The PIA API seems to return an out of date port number sometimes. The API documentation is very threadbare but there seems to be no way for me to fix this. Try running it again.
- I removed ufw firewall and transmission functionality since I switched to Fedora from Mint and qbittorrent from transmission

Other steps:
- I use an iptables based vpn kill-switch script: http://forum.ibvpn.com/topic/9-vpn-openvpn-firewall-killswitch-for-linux-users/ , https://gist.github.com/adrelanos/10565852

