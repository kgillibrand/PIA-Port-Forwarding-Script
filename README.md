# PIAScript
Python script which updates firewall and torrent client ports based on a VPN forwarded port

Currently unfinished, personal project that is a work in progress.

This script will:
- Check if the VPN is connected (tun0 interface exists).
- Reads PIA API credentials from a file (path provided as a command line parameter).
- Queries the PIA API to find the forwarded port. 
- See: https://www.privateinternetaccess.com/forum/discussion/180/port-forwarding-without-the-application-advanced-users.
- Update the Transmission port to the forwarded one.
- Update the ufw open port to the forwarded one.
 
Notes:
- Finding your local ip in Python is troublesome without libraries, the method I found online and used is very flaky.
- This script calls some Linux command line functions and is not portable.
- This is my first Python program, made in my spare time.
- This script will not work for other firewalls, torrent clients, or VPN providers as is
