#PIA Port Forwarding Script

Copyright Kieran Gillibrand 2016 (MIT License)

Small Python script which enables port forwarding for a PIA VPN and prints the forwarded port.

Now finished but not perfect, personal project, etc.

#Usage
- -h, --help: Show help.
- -debug, --debug: Show debugging print statements.
- credentialsfile: Mandatory positional argument, JSON file that contains PIA API credentials (see below).

#JSON Credentials File
```
{
    "user": "your PIA username",
    "pass": "your PIA password",
    "client_id": "client id you generated below"
}
```
- See: https://www.privateinternetaccess.com/forum/discussion/180/port-forwarding-without-the-application-advanced-users to create a client ID and for API documentation.
- The order of the values not matter because of the JSON format. Be careful to match the parameter names to what I am using (the API expects them) and make sure to have the correct braces, commas, and double-quotes.
    
#Dependancies
- Python 3
- The Python 3 netifaces library (look for a package for your distribution or use Python's easy_install).

#Script Operation
- Check if the VPN is connected (the interface is active).
- Find the local IP address for that interface.
- Read PIA API credentials from a file (path provided as a command line parameter).
- Add the local IP to the credentials
- Post to the PIA API endpoint in order to forward a port.
- Parse the response and print it (port number or error message).

#Notes and Issues
- This is my first Python program, made in my spare time but updated since.
- This script will not work for other VPN providers.
- Not all PIA gateways support port forwarding, make sure yours does: https://www.privateinternetaccess.com/pages/client-support/#sixth
- The PIA API sometimes returns a port that is closed if you have been reconnecting a lot. Try waiting a few minutes and trying again.
- This script should be portable now that I changed the network querying to use the netifaces library and removed the use of GNU/Linux command line tools.
- This script is written to be portable but it needs the correct interface name which is an issue. Non GNU/Linux OS users might have a different interface name though Windows, Mac, and Debian based distros users can use the official PIA application which offers port forwarding built-in. The default interface is tun0 so update the INTERFACE variable if you are told that tun0 is not connected.
- The API documentation given by PIA is very limited. I have no idea why a client ID is needed (every client will have a unique username) and what the ramifications are if you ever change it or if someone guesses yours (the link above recommends creating a strong random one). PIA limits you to 5 simaltaneous devices so this might be to differentiate them but the API requires you to provide your local VPN IP as well so who knows ¯\\\_(ツ)_/¯.
- PIA claims that you should call their API every hour while you are connected but I haven't had any issues with calling it once after first connecting.

#Downloading and Usage

1. Download piascript.pyc from the releases page or download a source code archive (includes the non-compiled script along with the License and Readme files).

2. Make the script executable

3. Create your API credentials JSON file (see above)

4. Connect to your PIA VPN

5. Execute the script and provide the path to the credentials file

6. Add an exception in your firewall for the port and update the port settings for applications that you are using
