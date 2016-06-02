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
import socket
import fcntl
import struct
from collections import OrderedDict

PIA_URL = "https://www.privateinternetaccess.com/vpninfo/port_forward_assignment"
"""API endpoint URL"""

TRANSMISSION_CONFIG_PATH = "/home/kieran/.config/transmission/settings.json"
"""Transmission settings file default location, ~/ would not open correctly for me in python"""

INTERFACE = "tun0"
"""Network interface for VPN"""
    
def isConnected ():
    """Checks if the client is connected to a PIA VPN, returns a boolean."""

    return (os.system ("ifconfig %s" %INTERFACE) == 0)

def getIPAddress (interface):
    """
        Supremely ghetto code to find local ip address.
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
    
    localIP = getIPAddress ("%s" %INTERFACE)
    
    credentials = open (credentialsPath, "r")

    jsonData = None
    
    try:
        jsonData = json.dumps (OrderedDict([("user", credentials.readline ().rstrip ("\n")), ("pass", credentials.readline ().rstrip ("\n")), ("client_id", credentials.readline ().rstrip ("\n")), ("local_ip", localIP)]))
        
    except (IOError, OSError, FileNotFoundError):
        print ("File: %s cannot be read or does not exist (credentials file)" %credentialsPath)
    finally:
        credentials.close()

    return jsonData

def getPIAPort (jsonData, url):
    """
        Contacts the PIA API at the given URL with the given JSON payload to find the currently forwarded port.
        Returns the port number as JSON.
    """
    
    request = urllib.request.Request (url)
    request.add_header ("Content-Type", "application/json")
    
    return urllib.request.urlopen (request, str.encode (json.dumps (jsonData)))


def updateTransmissionConfig (configPath, port):
    """
        Updates Transmission's config file at the given path with the given port number.
        Transmission is killed and restarted in the process.
    """
    
    settings = open (configPath, "r+")
    
    try:
        jsonSettings = json.load (settings)
        jsonSettings ["peer-port"] = port  
        settings.seek (0)
        settings.write (json.dumps (jsonSettings, sort_keys = True))
        settings.truncate ()
    except (IOError, OSError, FileNotFoundError):
        print ("File: %s cannot be read or does not exist (transmission settings)" %configPath)
    finally:
        settings.close()

def addUFWPort (port):
    """Adds the given port to the ufw firewall (opens it)."""
    
    print ("Root access is required to update the firewall configuration:")
    os.system ("su")
    
    try:
        os.system ("ufw allow %s" %port)
    except (IOError, OSError):
        print ("Error writing firewall rules (Was your root password correct?)")
        sys.exit ()

def main ():
    """Main method that takes the PIA credentials file as a command line argument"""
    
    if not isConnected ():
        print ("PIA VPN is not connected, please connect it first")
        sys.exit ()
    
    parser = ArgumentParser (description = "Configures Transmission and UFW with the forwarded port from a PIA vpn")
    
    parser.add_argument ("credentialsFile", help = "The PIA API credentials file, see the GitHub repository for details")
    
    args = parser.parse_args ()
    
    jsonData = getPIACredentials (args.credentialsFile)
    
    print ("Encoded JSON: %s" %jsonData)
        
    port = getPIAPort (jsonData, PIA_URL)

    print ("API return JSON: %s" %port.read ())
    
    updateTransmissionConfig (TRANSMISSION_CONFIG_PATH, port)
    
    addUFWPort (port)
    
if  __name__ == "__main__":
    main ()