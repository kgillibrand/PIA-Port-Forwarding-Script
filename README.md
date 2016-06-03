# PIAScript
Python script which updates firewall and torrent client ports based on a VPN forwarded port

Currently unfinished, personal project that is a work in progress.

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
