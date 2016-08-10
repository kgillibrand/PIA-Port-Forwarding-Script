#!/usr/bin/env python3

#License
""" 
    piascript: A small script which forwards a port and prints the forwarded port for a Private Internet Access VPN
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
    
#Metadata
__author__ = "Kieran Gillibrand: https://github.com/Favorablestream"
__copyright__ = "Copyright 2016, Kieran Gillibrand"
__credits__ = ["Duncan Gillibrand"]
__license__ = "GNU GPL Version 3 (LICENSE)"
__version__ = "1.4"
__date__ = "09/08/2016"
__maintainer__ = "Kieran Gillibrand"
__email__ = "Kieran.Gillibrand6@gmail.com"
__status__ = "Personal Project (finished I think)"

#Imports
import netifaces
from netifaces import AF_INET

from argparse import ArgumentParser

import urllib.request
import urllib.parse

import json

import sys

#Constants
PIA_ENDPOINT = "https://www.privateinternetaccess.com/vpninfo/port_forward_assignment"
"""API endpoint URL"""

INTERFACE = "tun0"
"""Network interface for VPN"""

DEBUG = False
"""Flag for debugging statements (set by -debug/--debug command line option)"""

ENCODING = "utf-8"
"""Text encoding to use for decoding API response"""

#Code
def isConnected (interface: str) -> bool:
    """
        Checks if the client is connected to a PIA VPN (Boolean)
        
        interface (String): The name of the interface to check
    """

    connected = interface in netifaces.interfaces ()

    if DEBUG:
        if connected:
            print ("Interface: %s is connected" %interface)
            print ()

    return connected

def getIPAddress (interface: str) -> str:
    """
        Returns the IP address (String)
        
        interface (String): The name of the interface to get the ip for
    """

    ip = netifaces.ifaddresses (interface) [AF_INET] [0] ["addr"]

    if DEBUG:
        print ("Local IP for VPN interface %s: %s" %(interface, ip))
        print ()

    return ip

def getCredentials (credentialsPath: str) -> dict:
        """
            Retrieves PIA API credentials (Dictionary)
            
            credentialsPath (String): The path to the credentials JSON file
        """
        
        try:
            with open (credentialsPath) as credentialsFile:
                credentials = json.loads (credentialsFile.read ())
                
                credentials ["local_ip"] = getIPAddress (INTERFACE)
                
                if DEBUG:
                    print ("Using credentials file: %s" %credentialsPath)
                    print ()
                    print ("Username: %s" %credentials ["user"])
                    print ("Password: %s" %credentials ["pass"])
                    print ("Client ID: %s" %credentials ["client_id"])
                    print ()

                return credentials

        except (IOError, OSError):
            print ("Credentials file: %s does not exist or cannot be opened" %credentialsPath)
            print ()
                
            sys.exit (1)
                        
def forwardPort (credentials: dict, endpointURL: str) -> dict:
    """
        Contacts the PIA API to enable port forwarding and returns the API response (Dictionary)

        credentials (Dictionary): The credentials extracted from a JSON file by getPIACredentials ()
        url (String): The endpoint URL
    """

    if DEBUG:
        print ("Posting to endpoint: %s " % endpointURL)
        print ()

    parameters = urllib.parse.urlencode (credentials)
    response =  urllib.request.urlopen (endpointURL, str.encode (parameters)).read ()
    responseString = response.decode (ENCODING)

    if DEBUG:
        print ("API response JSON: %s" %responseString)
        print ()

    return json.loads (responseString)

def main ():
    """Main method that takes command line arguments"""
    
    print ()
    print ("Private Internet Access Port Forwarding Script - Copyright Kieran Gillibrand, 2016 (see license)")
    print ("https://github.com/Favorablestream")
    print ()
    
    parser = ArgumentParser (description = "Enables port forwarding for a Private Internet Access VPN and displays the forwarded port")
    parser.add_argument ("-debug", "--debug", help = "Display debugging print statements", action = "store_true")
    parser.add_argument ("credentialsfile", help = "The PIA API JSON credentials file, see README.md for details")
    args = parser.parse_args ()

    #Override global debug flag if -debug/--debug command line flag is used
    global DEBUG
    DEBUG = args.debug

    if DEBUG:
        print ("Debugging print statements enabled")
        print ()

    if not isConnected (INTERFACE):
        print ("VPN on interface: %s is not connected, please connect it first" %INTERFACE)
        
        sys.exit (1)

    credentials = getCredentials (args.credentialsfile)
    
    response = forwardPort (credentials, PIA_ENDPOINT)

    print ("Response recieved")
    print ()

    if "port" in response:
        print ("Forwarded port: %s" %response ["port"])

    elif "error" in response:
        print ("API returned an error: %s" %response ["error"])
        
        sys.exit (1)

    else:
        for key, value in response.items ():
            print ("API returned unknown value: %s: %s" %(key, value))

        sys.exit (1)

    print ()

    print ("Make sure to allow this port in your firewall and configure your applications to use it.")
    print ("Have a nice day =)")
    
if  __name__ == "__main__":
    main ()
