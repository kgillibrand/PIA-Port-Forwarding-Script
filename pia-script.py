#!/usr/bin/python3

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
__title__ = 'Private Internet Access Port Forwarding Script'
__author__ = 'Kieran Gillibrand'
__host__ = 'https://github.com/Favorablestream'
__copyright__ = 'Copyright 2016 Kieran Gillibrand'
__credits__ = ['Duncan Gillibrand']
__license__ = 'MIT License (LICENSE.txt)'
__version__ = '1.3'
__date__ = '05/02/2017'
__maintainer__ = 'Kieran Gillibrand'
__email__ = 'Kieran.Gillibrand6@gmail.com'
__status__ = 'Personal Project (released)'

#Imports
import netifaces

import argparse

import hashlib

import urllib.request
import urllib.parse
import urllib.error

import json

import sys
import os

#Global Constants
DEBUG = False
'''Flag for debugging print statements (set by -debug/--debug command line option)'''

DEFAULT_ENCODING = 'utf-8'
'''Default encoding to use for decoding the API response if the server does not give us an encoding header'''
    
#Code
def debug_print (message: str, print_newline: bool = True):
    '''
        Print a message if debugging statements are enabled
        
        message (str): The message to print
        printNewline (bool): Print an additional newline after the message (default True) 
    '''
    if not DEBUG:
        return
        
    print (message)
    
    if print_newline:
        print ()
        
def nondebug_print (message: str, print_newline: bool = True):
    '''
        Print a message if debugging statements are not enabled
        
        message (str): The message to print
        printNewline (bool): Print an additional newline after the message (default True)
    '''
    
    if DEBUG:
        return
    
    print (message)
    
    if print_newline:
        print ()

def append_list_to_string (message: str, elements: list) -> str:
    '''
        Concatenate a message string to a list of elements (str)
        
        Usually used to form an error message to pass to handle_error when a list of addresses, elemts, etc is involved.
        
        message (str): The message before the elements are concatonated to it
        elements (list): The list of elements to concatenate to the message
    '''
             
    string_elements = []
    
    for element in elements:
        string_elements.append (str (element))
        
    return message + ('\n'.join (string_elements)) #Join all elements delimited by a newline to the message and return
    
def handle_error (message: str, exit_code: int, exception: Exception = None):
    '''
        Prints an error message, exception message (if provided), and exits with the given exit code
        
        message (str): The error message to print
        exception (Exception) (optional): The exception used to print the provided esception message
        exit_code (int): The code to exit with
        
        Script Exit Codes
        - 0: main (): Success, normal exit
        - 1: main (): VPN is not connected
        - 2: call_port_api (): Error with get request to API endpoint
        - 3: call_port_api (): API JSON response is malformed
        - 4: main (): API returned an error response
        - 5: main (): API returned an unknown response
    '''
    
    exit_codes = ['main (): Success, normal exit', 'main (): VPN is not connected', 'call_port_api (): Error sending get request to API endpoint', 'call_port_api (): API JSON response is malformed', 'main (): API returned an error response', 'main (): API returned an unknown response']
    
    print (message)
    print ()
    
    if exception != None:
        print (str (exception))
        print ()
        
    print ('Exiting with exit status: %s, %s' %(exit_code, exit_codes [exit_code]))
    
    sys.exit (exit_code)
    
def is_interface_connected (interface: str) -> bool:
    '''
        Checks if the VPN is connected (Boolean)
        
        interface (str): The name of the interface to check
    '''
        
    exists = interface in netifaces.interfaces () #Check if the interface exists
    
    #We cannot be connected if the interface does not exist
    if not exists:
        return False
        
    #Check if IPV4 is contained in the address families for the interface (if it has at least one IPV4 address and therefore is up)
    address_families = netifaces.ifaddresses (interface)
    up = netifaces.AF_INET in address_families
    
    if up:
        debug_print ('Interface: \'%s\' is connected' %interface)

    return up

def generate_client_id (random_bytes_length) -> str:
    '''
        Generates a secure random client id to be used with the port forwarding API (str)
        
        random_bytes_length (int): The number of bytes to read before generating the client id
    '''
    
    random_byte_string = os.urandom (random_bytes_length)
    
    hash_generator = hashlib.sha256 ()
    hash_generator.update (random_byte_string)
    hash_string = hash_generator.hexdigest ()
    
    hash_string = hash_string.replace ('-', ' ')
    
    debug_print ("Generated client ID: %s" %hash_string)
    
    return hash_string
    
def call_port_api (client_id: str, endpoint_url: str, timeout: int) -> dict:
    '''
        Contacts the PIA API to enable port forwarding and returns the parsed API response (Dictionary)

        client_id (str): The client id generated by generate_client_id       
        endpoint_url (str): The endpoint URL to post to
        timeout (int): The number of seconds before the API connection times out
    '''
        
    debug_print ('Posting to endpoint: \'%s\'' % endpoint_url)

    client_id_dict = {'client_id': client_id}
    encoded_id = urllib.parse.urlencode (client_id_dict)
    get_url = endpoint_url + '?' + encoded_id
    
    try:
        with urllib.request.urlopen (url = get_url, timeout = timeout) as connection:
            response = connection.read ()
            
            #Decode with the given encoding or with the default if none is given
            responseEncoding = connection.headers.get_content_charset ()
            if responseEncoding == None:
                responseEncoding = DEFAULT_ENCODING
        
    except (urllib.error.URLError, urllib.error.HTTPError, ConnectionResetError) as urlError:
        handle_error (message = 'Error with get request to API endpoint with URL: %s' %get_url, exception = urlError, exit_code = 2)
        
    responseString = response.decode (responseEncoding)

    nonHTTPResponse = urllib.parse.unquote (responseString) #Remove URL encoding, doesn't matter for the responses from this API in my experience

    debug_print ('Decoded API response bytes as: \'%s\'' %responseEncoding)
    debug_print ('API response JSON: \'%s\'' %nonHTTPResponse)

    try:
        return json.loads (nonHTTPResponse)
    
    except (ValueError) as jsonError:
        handle_error (message = 'The API response is malformed, refer to the response text and the exception message below\n\nResponse text: %s' %nonHTTPResponse, exception = jsonError, exit_code = 3)

def main ():
    '''Main method that takes command line arguments'''
    
    #Local Constants
    RANDOM_BYTES_LENGTH = 3000
    '''The number of bytes to read when generating a client id'''
    
    ENDPOINT = 'http://209.222.18.222:2000/'
    '''API endpoint URL'''

    INTERFACE = 'tun0'
    '''Network interface for VPN'''
    
    TIMEOUT = 10
    '''Timeout in seconds when connecting to the API endpoint'''

    print ()
    print ('%s - %s, %s' %(__title__, __copyright__, __license__))
    print ('Version: %s, %s' %(__version__, __date__))
    print ('%s' %__host__)
    print ()
    
    parser = argparse.ArgumentParser (description = 'PIA Port Forwarding Script: A small script which enables port forwarding for a Private Internet Access VPN and displays the forwarded port.')
    parser.add_argument ('-debug', '--debug', help = 'Display debugging print statements', action = 'store_true')
    args = parser.parse_args ()

    #Set global debug flag if -debug/--debug command line flag is used
    global DEBUG
    DEBUG = args.debug

    debug_print ('Debugging print statements enabled')

    if not is_interface_connected (INTERFACE):
        handle_error (message = 'VPN interface: \'%s\' is not connected, please connect it first\nBe sure the INTERFACE variable is correctly set if your VPN is actually connected' %INTERFACE, exit_code = 1)
    
    client_id = generate_client_id (RANDOM_BYTES_LENGTH)
    
    response = call_port_api (client_id, ENDPOINT, TIMEOUT)

    nondebug_print ('Response recieved')

    #Standard response
    if 'port' in response:
        print ('Forwarded port: %s' %response ['port'])
        print ()

    #Error response
    elif 'error' in response:
        handle_error (message = 'API returned an error: %s' %response ['error'], exit_code = 4)
        
    #Unknown key
    else:
        key_values = []
        
        for key, value in response.items ():
            key_values.append ('%s: %s' %(str (key), str (value)))
            
        message = append_list_to_string ('API returned unknown key/value pair(s):\n\n', key_values)

        handle_error (message = message, exit_code = 5)

    print ('Make sure to allow this port in your firewall and configure your applications to use it.')
    print ('Have a nice day :)')
    
if  __name__ == '__main__':
    main ()
