# PIAScript
Python script which updates firewall and torrent client ports based on a VPN forwarded port

Now finished but not perfect, personal project, etc.

Usage
- -h, --help: Show help
- credentialsfile: Mandatory first argument, file that contains PIA API credentials (see PIA link below).
- -apionly, --apionly: Optional flag that only provides the port number but does not update Transmission and UFW configurations.

This script will:
- Check if the VPN is connected (tun0 interface exists).
- Read PIA API credentials from a file (path provided as a command line parameter).
- Query the PIA API to find the forwarded port. 
- See: https://www.privateinternetaccess.com/forum/discussion/180/port-forwarding-without-the-application-advanced-users.
- Update the Transmission port to the forwarded one (kill transmission, update settings file, start transmission).
- Add a ufw rule for the forwarded port
 
Notes and issues:
- Finding your local ip in Python is troublesome without libraries, the method I found online and used is very flaky (https://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/).
- This script calls some Linux command line functions and is not portable.
- This is my first Python program and first use of JSON, made in my spare time.
- This script will not work for other firewalls, torrent clients, or VPN providers as is
- This script adds a firewall rule each time, it will not remove old rules or check if they already exist (adding a rule that already exists does nothing).
- This script will kill Transmission to update it's settings file, it will not restart it (the script reminds you).
- API erros are checked in a very basic way, true JSON parsing for the response would be better.
- Exception handling with file I/O could be better but I had issues with "with using" and "try/catch/finally"
- The script will sleep for 10 seconds after killing Transmission because Transmission will not close right away if torrents are active. A better soloution would be to wait until the process is terminated but I don't know of a simple way to do that in Python when calling linux terminal functions.
- The PIA API seems to return an out of date port number sometimes. The API documentation is very threadbare but there seems to be no way for me to fix this.
