#PIA Port Forwarding Script

Copyright Kieran Gillibrand 2016 (MIT License)

Small Python script which enables port forwarding for a PIA VPN and prints the forwarded port.

Now finished but not perfect, personal project, etc.

#Usage
- -h, --help: Show help.
- -debug, --debug: Show debugging print statements.

#Dependancies
- A Python 3 runtime
- The Python 3 netifaces library (look for a package for your distribution or use Python's easy_install).
- Netifaces is licensed under the MIT license: https://pypi.python.org/pypi/netifaces

#Script Operation
- Check if the VPN is connected (the interface is active).
- Generate a random client id
- Send a get request to the PIA API endpoint with the client id in order to forward a port.
- Parse the response and print it (port number or error message).

#Notes and Issues
- This is my first Python program, made in my spare time but updated since.
- This script will not work for other VPN providers.
- Not all PIA gateways support port forwarding, make sure yours does: https://www.privateinternetaccess.com/pages/client-support/#sixth
- This script is written to be portable but it needs the correct interface name which is an issue. Non GNU/Linux OS users might have a different interface name though Windows, Mac, and Debian based distros users can use the official PIA application which offers port forwarding built-in. The default interface is tun0 so update the INTERFACE variable if you are told that tun0 is not connected.
- I've just switched to PIA's new API which allowed me to elimate the config file. The API tends to reset connections or not send responses when errors occur (if you try to port forward a 2nd time or port forward with an unsupported gateway for example).
  Because of that the error handling isn't brilliant right now.

#Downloading and Usage

1. Download piascript.pyc from the releases page or download a source code archive (includes the script source along with the License and Readme files).

2. Make the script/binary executable

3. Connect to your PIA VPN

4. Execute the script

6. Add an exception in your firewall for the port and update the port settings for applications that you are using

#Constants (that you may want to change)
Global
- DEBUG: Flag that enables debugging print statements, set by the -debug/--debug option so you shouldn't need to edit it. Default: False
- DEFAULT_ENCODING: The backup encoding to decode the response with if the API doesn't return a content type header. Default: utf-8

Main Method
- RANDOM_BYTES_LENGTH: The number of bytes to read from os.urandom when generating the client id. The example script uses 100 lines of /dev/urandom instead which seemed excessive to me. Default: 3000
- ENDPOINT: The API endpoint URL. Default: http://209.222.18.222:2000/
- INTERFACE: The network interface that the VPN uses. Default: tun0
- TIMEOUT: The timeout in seconds when calling the API. Default: 10

#License
MIT License

Copyright (c) 2016 Kieran Gillibrand

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
