#!/usr/bin/env python3

#License
'''
    MIT License

    Copyright (c) 2016 Kieran Gillibrand

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the 'Software'), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''
    
#Description
'''
    PIA Port Forwarding Script
    
    A small script which enables port forwarding for a Private Internet Access VPN and displays the forwarded port.
'''

#Metadata
__author__ = 'Kieran Gillibrand: https://github.com/Favorablestream'
__copyright__ = 'Copyright 2016 Kieran Gillibrand'
__credits__ = ['Duncan Gillibrand']
__license__ = 'MIT License (LICENSE.txt)'
__version__ = '1.4'
__date__ = '09/08/2016'
__maintainer__ = 'Kieran Gillibrand'
__email__ = 'Kieran.Gillibrand6@gmail.com'
__status__ = 'Personal Project (finished I think)'

#Imports
import netifaces
from netifaces import AF_INET

from argparse import ArgumentParser

import urllib.request
import urllib.parse

import json

import sys

#Global Constants
DEBUG = False
'''Flag for debugging statements (set by -debug/--debug command line option)'''

#Code
def isConnected (interface: str) -> bool:
    '''
        Checks if the client is connected to a PIA VPN (Boolean)
        
        interface (String): The name of the interface to check
    '''

    connected = interface in netifaces.interfaces ()

    if DEBUG:
        if connected:
            print ('Interface: \'%s\' is connected' %interface)
            print ()

    return connected

def getIPAddress (interface: str) -> str:
    '''
        Returns the IP address (String)
        
        interface (String): The name of the interface to get the ip for
    '''

    ip = netifaces.ifaddresses (interface) [AF_INET] [0] ['addr']

    if DEBUG:
        print ('Local IP for VPN interface \'%s\': %s' %(interface, ip))
        print ()

    return ip

def getCredentials (credentialsPath: str, interface: str) -> dict:
        '''
            Retrieves PIA API credentials (Dictionary)
            
            credentialsPath (String): The path to the credentials JSON file
            interface (String): The VPN interface to get the local IP from
        '''
        
        try:
            with open (credentialsPath) as credentialsFile:
                credentials = json.loads (credentialsFile.read ())
                
                credentials ['local_ip'] = getIPAddress (interface) #Add local VPN IP
                
                if DEBUG:
                    print ('Using credentials file: \'%s\'' %credentialsPath)
                    print ()
                    print ('Username: \'%s\'' %credentials ['user'])
                    print ('Password: \'%s\'' %credentials ['pass'])
                    print ('Client ID: \'%s\'' %credentials ['client_id'])
                    print ()

                return credentials

        except (IOError, OSError) as fileError:
            print ('Credentials file: \'%s\' does not exist or cannot be opened' %credentialsPath)
            print ()
            print (str (fileError))
                
            sys.exit (1)
        
        except (ValueError) as jsonError:
            print ('JSON file: \'%s\' is malformed, refer to the README for the correct format' %credentialsPath)
            print ()
            print (str (jsonError))
            
            sys.exit (1)
                        
def forwardPort (credentials: dict, endpointURL: str, encoding: str) -> dict:
    '''
        Contacts the PIA API to enable port forwarding and returns the API response (Dictionary)

        credentials (Dictionary): The credentials extracted from a JSON file by getPIACredentials ()
        url (String): The endpoint URL
        encoding (String): The text encoding to decode the API response into
    '''

    if DEBUG:
        print ('Posting to endpoint: \'%s\'' % endpointURL)
        print ()

    parameters = urllib.parse.urlencode (credentials)
    
    response =  urllib.request.urlopen (endpointURL, str.encode (parameters)).read ()
    responseString = response.decode (encoding)

    if DEBUG:
        print ('API response JSON: \'%s\'' %responseString)
        print ()

    return json.loads (responseString)

def main ():
    '''Main method that takes command line arguments'''
    
    #Local Constants
    PIA_ENDPOINT = 'https://www.privateinternetaccess.com/vpninfo/port_forward_assignment'
    '''API endpoint URL'''

    INTERFACE = 'tun0'
    '''Network interface for VPN'''

    ENCODING = 'utf-8'
    '''Text encoding to use for decoding API response'''

    print ()
    print ('Private Internet Access Port Forwarding Script - Copyright Kieran Gillibrand, 2016 (MIT License)')
    print ('https://github.com/Favorablestream')
    print ()
    
    parser = ArgumentParser (description = 'Enables port forwarding for a Private Internet Access VPN and displays the forwarded port')
    parser.add_argument ('-debug', '--debug', help = 'Display debugging print statements', action = 'store_true')
    parser.add_argument ('credentialsfile', help = 'The PIA API JSON credentials file, see README.md for details')
    args = parser.parse_args ()

    #Set global debug flag if -debug/--debug command line flag is used
    global DEBUG
    DEBUG = args.debug

    if DEBUG:
        print ('Debugging print statements enabled')
        print ()

    if not isConnected (INTERFACE):
        print ('VPN interface: \'%s\' is not connected, please connect it first' %INTERFACE)
        
        sys.exit (1)

    credentials = getCredentials (args.credentialsfile, INTERFACE)
    
    response = forwardPort (credentials, PIA_ENDPOINT, ENCODING)
    
    print ('Response recieved')
    print ()

    #Standard response
    if 'port' in response:
        print ('Forwarded port: %s' %response ['port'])

    #Error response
    elif 'error' in response:
        print ('API returned an error: %s' %response ['error'])
        
        sys.exit (1)

    #Unknown key
    else:
        print ('API returned unknown key/value pair(s):')
        
        for key, value in response.items ():
            print ('%s: %s' %(key, value))

        sys.exit (1)

    print ()

    print ('Make sure to allow this port in your firewall and configure your applications to use it.')
    print ('Have a nice day =)')
    
if  __name__ == '__main__':
    main ()
