#!/usr/bin/env python3

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
    
__author__ = "Kieran Gillibrand: https://github.com/Favorablestream"
__copyright__ = "Copyright 2016, Kieran Gillibrand"
__credits__ = ["Duncan Gillibrand"]
__license__ = "GNU GPL Version 3 (LICENSE)"
__version__ = "1.3"
__date__ = "08/08/2016"
__maintainer__ = "Kieran Gillibrand"
__email__ = "Kieran.Gillibrand6@gmail.com"
__status__ = "Personal Project (finished I think)"

import sys

from argparse import ArgumentParser

import urllib.request
import urllib.parse

import json

import netifaces
from netifaces import AF_INET


PIA_ENDPOINT = "https://www.privateinternetaccess.com/vpninfo/port_forward_assignment"
"""API endpoint URL"""

INTERFACE = "tun0"
"""Network interface for VPN"""

DEBUG = False
"""Flag for debugging statements (set by -debug/--debug command line option)"""
    
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

    ip = netifaces.ifaddresses (interface) [AF_INET] [0] ['addr']

    if DEBUG:
        print ("Local IP for VPN interface: %s is %s" %(interface, ip))
        print ()

    return ip

def getCredentials (credentialsPath: str) -> dict:
        """
            Retrieves PIA API credentials (Dictionary)
            
            credentialsPath (String): The path to the credentials file
        """
        
        credentials = None
        
        try:
            credentials = open (credentialsPath, "r")
            
            username = credentials.readline ().rstrip ("\n")
            password = credentials.readline ().rstrip ("\n")
            clientID = credentials.readline ().rstrip ("\n")
            localIP = getIPAddress (INTERFACE)
            
            credentials.close ()

            if DEBUG:
                print ("Using credentials file: %s" %credentialsPath)
                print ()
                print ("Username: %s" %username)
                print ("Password: %s" %password)
                print ("Client ID: %s" %clientID)
                print ()

            return {"user": username, "pass": password, "client_id": clientID, "local_ip": localIP}

        except (IOError, OSError):
                print ("Credentials file: %s does not exist or cannot be opened" %credentialsPath)
                print ()
                
                if not credentials == None:
                    credentials.close ()
                    
                sys.exit ()
                        
def forwardPort (credentials: dict, endpointURL: str) -> dict:
    """
        Contacts the PIA API to enable port forwarding and returns the API response (Dictionary)

        credentials (Dictionary): The credentials extracted from a file by getPIACredentials ()
        url (String): The endpoint URL
    """

    if DEBUG:
        print ("Posting to endpoint: %s " % endpointURL)
        print ()

    parameters = urllib.parse.urlencode (credentials)
    response =  urllib.request.urlopen (endpointURL, str.encode (parameters)).read ()
    responseString = response.decode ("utf-8")

    if DEBUG:
        print ("API response JSON: %s" %responseString)
        print ()

    return json.loads (responseString)

def main ():
    """Main method that takes the PIA credentials file as a command line argument"""
    
    print ()
    print ("Private Internet Access Port Forwarding Script - Copyright Kieran Gillibrand, 2016 (see license)")
    print ("https://github.com/Favorablestream")
    print ()
    
    parser = ArgumentParser (description = "Configures Transmission and UFW with the forwarded port from a PIA vpn")
    parser.add_argument ("-debug", "--debug", help = "Display debugging print statements", action = "store_true")
    parser.add_argument ("credentialsfile", help = "The PIA API credentials file, see the GitHub readme for details")
    args = parser.parse_args ()

    global DEBUG
    DEBUG = args.debug

    if DEBUG:
        print ("Debugging print statements enabled")
        print ()

    if not isConnected (INTERFACE):
        print ("VPN on interface: %s is not connected, please connect it first" %INTERFACE)
        sys.exit ()

    credentials = getCredentials (args.credentialsfile)
    
    response = forwardPort (credentials, PIA_ENDPOINT)

    print ("Response recieved")
    print ()

    if "port" in response:
        print ("Forwarded port: %s" %response ["port"])

    elif "error" in response:
        print ("API returned an error: %s" %response ["error"])
        sys.exit ()

    else:
        for key, value in response.items ():
            print ("API returned unknown value: %s: %s" %(key, value))

        sys.exit ()

    print ()

    print ("Make sure to allow this port in your firewall and configure your applications to use it.")
    print ("Have a nice day =)")
    
if  __name__ == "__main__":
    main ()
