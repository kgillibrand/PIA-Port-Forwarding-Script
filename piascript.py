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
__license__ = "GNU GPL Version 3 (LICENSE.txt)"
__version__ = "1.2"
__date__ = "07/08/2016"
__maintainer__ = "Kieran Gillibrand"
__email__ = "Kieran.Gillibrand6@gmail.com"
__status__ = "Personal Project (finished I think)"

from argparse import ArgumentParser

import urllib.request
import urllib.parse

import netifaces
from netifaces import AF_INET


PIA_URL = "https://www.privateinternetaccess.com/vpninfo/port_forward_assignment"
"""API endpoint URL"""

INTERFACE = "tun0"
"""Network interface for VPN"""
    
def isConnected (interface):
    """
        Checks if the client is connected to a PIA VPN (Boolean)
        
        interface (String): The name of the interface to check
    """
    
    return interface in netifaces.interfaces ()

def getIPAddress (interface):
    """
        Returns the IP address (String)
        
        interface (String): The name of the interface to get the ip for
    """
    return netifaces.ifaddresses (interface) [AF_INET] [0] ['addr']

def getCredentials (credentialsPath):
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
            localIP = getIPAddress (INTERFACE);
            
            credentials.close ()
            
            return {"user": username, "pass": password, "client_id": clientID, "local_ip": localIP}
        except (IOError, OSError):
                print ("Credentials file: %s does not exist or cannot be opened" %credentialsPath)
                
                if not credentials == None:
                    credentials.close ()
                    
                sys.exit ()
                        
def forwardPort (credentials, url):
    """
        Contacts the PIA API to enable port forwarding and returns the forwarded port number (String)

        credentials (Dictionary): The credentials extracted from a file by getPIACredentials ()
        url (String): The endpoint URL
    """
    
    parameters = urllib.parse.urlencode (credentials)
    response =  urllib.request.urlopen (url, str.encode (parameters)).read ()
    responseString = response.decode ("utf-8"); 
    
    return responseString

def main ():
    """Main method that takes the PIA credentials file as a command line argument"""
    
    print ()
    print ("Private Internet Access Port Forwarding Script - Copyright Kieran Gillibrand, 2016 (see license)")
    print ("https://github.com/Favorablestream")
    print ()

    if not isConnected (INTERFACE):
        print ("PIA VPN is not connected, please connect it first")
        sys.exit ()
    
    parser = ArgumentParser (description = "Configures Transmission and UFW with the forwarded port from a PIA vpn")
    parser.add_argument ("credentialsfile", help = "The PIA API credentials file, see the GitHub readme for details")
    args = parser.parse_args ()
    
    credentials = getCredentials (args.credentialsfile)
    
    response = forwardPort (credentials, PIA_URL)
    
    print ("API response: %s" %response)
    
    if "error" in response:
        print ("API error, check your credentials")
        sys.exit ()
        
    port = response [8:-1]
    
    print ()
    print ("Forwarded port: %s" %port)
    print ()
    
    print ("Have a nice day =)")
    
if  __name__ == "__main__":
    main ()
