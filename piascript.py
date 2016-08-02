#!/usr/bin/env python3

""" 
    piascript: A small script which configures Transmission and UFW based on the forwarded port of a Private Internet Access VPN
    Copyright (C) 2016 Kieran Gillibrand

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
    
__author__ = "Kieran Gillibrand: https://github.com/Favorablestream"
__copyright__ = "Copyright 2016, Kieran Gillibrand"
__credits__ = ["Duncan Gillibrand"]
__license__ = "GNU GPL (LICENSE.txt)"
__version__ = "1.0"
__date__ = "02/06/2016"
__maintainer__ = "Kieran Gillibrand"
__email__ = "Kieran.Gillibrand6@gmail.com"
__status__ = "Personal Project"

from argparse import ArgumentParser
import os
import sys
import json
import urllib.request
import urllib.parse
import socket
import fcntl
import struct
import time

PIA_URL = "https://www.privateinternetaccess.com/vpninfo/port_forward_assignment"
"""API endpoint URL"""

INTERFACE = "tun0"
"""Network interface for VPN"""
    
def isConnected ():
    """Checks if the client is connected to a PIA VPN, returns a boolean."""

    #Checks exit status of ifconfig INTERFACE (0 for success, non 0 for error)
    return (os.system ("ifconfig %s" %INTERFACE) == 0)

def getIPAddress (interface):
    """
        Supremely ghetto code to find local ip address, returns the ip for a given interface
        From: https://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
    """
    s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa (fcntl.ioctl
    (
        s.fileno (),
        0x8915, # SIOCGIFADDR
        struct.pack ("256s", str.encode (interface [:15]))
    )[20:24])


def getPIACredentials (credentialsPath):
        """Retrieves PIA API credentials from the file at the given path and returns them in JSON format."""
        
        credentials = None
        
        try:
            credentials = open (credentialsPath, "r")
            
            username = credentials.readline ().rstrip ("\n")
            password = credentials.readline ().rstrip ("\n")
            clientID = credentials.readline ().rstrip ("\n")
            localIP = getIPAddress (INTERFACE);
            
            credentials.close ()
            
            return {"user": username, "pass": password, "client_id": clientID, "local_ip": localIP}
        except (IOError, OSError):
                print ("Credentials file: %s does not exist or cannot be opened" %credentialsPath)
                
                if not credentials == None:
                    credentials.close ()
                    
                sys.exit ()
                        
def getPIAPort (data, url):
    """
        Contacts the PIA API at the given URL with the given payload to find the currently forwarded port.
        Returns the port number as a string.
    """
    
    parameters = urllib.parse.urlencode (data)
    response =  urllib.request.urlopen (PIA_URL, str.encode (parameters)).read ()
    responseString = response.decode ("utf-8"); 
    
    return responseString

def main ():
    """Main method that takes the PIA credentials file as a command line argument"""
    
    print ("Private Internet Access Configuration Script - Copyright Kieran Gillibrand, 2016 (see license)")
    print ("https://github.com/Favorablestream")
    print ()

    if not isConnected ():
        print ("PIA VPN is not connected, please connect it first")
        sys.exit ()
    
    parser = ArgumentParser (description = "Configures Transmission and UFW with the forwarded port from a PIA vpn")
    parser.add_argument ("credentialsfile", help = "The PIA API credentials file, see the GitHub readme for details")
    args = parser.parse_args ()
    
    data = getPIACredentials (args.credentialsfile)
    response = getPIAPort (data, PIA_URL)
    port = response [8:-1]
    
    print ("API response received: %s" %response)
    
    if "error" in response:
        print ("API error, check your credentials")
        sys.exit ()
    
if  __name__ == "__main__":
    main ()
