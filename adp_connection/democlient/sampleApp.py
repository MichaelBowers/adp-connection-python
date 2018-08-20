#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of adp-api-client.
# https://github.com/adplabs/adp-connection-python

# Copyright © 2015-2016 ADP, LLC.

# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

import sys

try:
    import BaseHTTPServer, SimpleHTTPServer
except Exception:
    from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    from urlparse import urlparse, parse_qs
except Exception:
    from urllib.parse import urlparse, parse_qs

from os import curdir, sep

from adp_connection.lib import *
from adp_connection import __version__

PORT_NUMBER = 8889

# This class will handles any incoming request from the browser


class httpHandler(BaseHTTPRequestHandler):
    """ Base class for handling HTTP Requests.
    Extends BaseHTTPRequestHandler """

    # Global connections dictionary
    connectionDict = dict({})

    # Handler for the GET requests
    def do_GET(self):
        """ Handle GET Requests """

        parsed_url = urlparse(self.path)
        real_path = parsed_url.path
        query = parsed_url.query
        query_components = parse_qs(query)

        if self.path == '/':
            self.path = 'index.html'

        try:

            # Handle request for a Client Credentials App
            if self.path == '/client_credentials':
                config = dict({})
                config['clientID'] = '88a73992-07f2-4714-ab4b-de782acd9c4d'
                config['clientSecret'] = 'a130adb7-aa51-49ac-9d02-0d4036b63541'
                config['sslCertPath'] = 'certs/cert.pem'
                config['sslKeyPath'] = 'certs/cert.key'
                config['tokenServerURL'] = 'https://iat-api.adp.com/auth/oauth/v2/token'
                config['disconnectURL'] = 'https://iat-accounts.adp.com/auth/oauth/v2/logout'
                config['apiRequestURL'] = 'https://iat-api.adp.com'
                config['grantType'] = 'client_credentials'

                # Initialize the Connection Configuration Object.
                # Since the grant type is client_credentials a
                # ClientCredentialsConfiguration object is returned
                try:
                    ClientCredentialsConfiguration = ConnectionConfiguration().init(config)

                    # Using the new configuration object create a connection
                    ccConnection = ADPAPIConnectionFactory().createConnection(ClientCredentialsConfiguration)

                    resp = ''

                    # try to connect and send the response back
                    ccConnection.connect()
                    if (ccConnection.isConnectedIndicator()):

                        # A successful connection generates a UUID as a session identifier
                        # which can be retrieved using the getSessionState() method call on
                        # the connection. There is also provision to set a user-defined
                        # session identifier using the setSessionState(string) method call on
                        # the connection. This should be done after a connection has been
                        # obtained from the connection factory, but before calling connect()
                        #
                        # We can use the session identifier as a key to store the connection
                        # into the global connection dictionary for later retrieval on
                        # subsequent requests
                        self.connectionDict[ccConnection.getSessionState()] = ccConnection
                        resp = '<b>Connected!</b>'
                        resp = resp + '<br>access token: ' + ccConnection.getAccessToken()
                        resp = resp + '<br>expiration: ' + ccConnection.getExpiration().strftime("%Y-%m-%d %H:%M:%S")
                        resp = resp + '<br>session state:' + ccConnection.getSessionState()
                    else:
                        resp = '<b>Not Connected!</b>'
                except ConfigError as conferr:
                    print(conferr.msg)
                except ConnectError as connecterr:
                    resp = '<b>Connection Error</b>'
                    resp = resp + '<br>Class: ' + connecterr.cname
                    resp = resp + '<br>Error: ' + connecterr.code
                    resp = resp + '<br>Message: ' + connecterr.msg
                finally:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(resp)
                    return

            # Handle request for an Authorization Code App
            if self.path == '/authorization_code':
                config = dict({})
                config['clientID'] = 'ec762f06-7410-4f6d-aa82-969902c1836a'
                config['clientSecret'] = '6daf2cd7-4604-46c0-ab43-a645a6571d34'
                config['sslCertPath'] = 'certs/cert.pem'
                config['sslKeyPath'] = 'certs/cert.key'
                config['tokenServerURL'] = 'https://iat-api.adp.com/auth/oauth/v2/token'
                config['apiRequestURL'] = 'https://iat-api.adp.com'
                config['grantType'] = 'authorization_code'
                config['baseAuthorizationURL'] = 'https://iat-accounts.adp.com/auth/oauth/v2/authorize'
                config['disconnectURL'] = 'https://iat-accounts.adp.com/auth/oauth/v2/logout'
                config['redirectURL'] = 'http://localhost:8889/callback'
                config['responseType'] = 'code'
                config['scope'] = 'openid'

                # Initialize the Connection Configuration Object.
                # Since the grant type is client_credentials an
                # AuthorizationCodeConfiguration object is returned
                try:
                    AuthorizationCodeConfiguration = ConnectionConfiguration().init(config)

                    # Using the new configuration object create a connection
                    acConnection = ADPAPIConnectionFactory().createConnection(AuthorizationCodeConfiguration)

                    # Authorization Code Apps require a user to login to ADP
                    # So obtain the authorization URL to redirect the user's
                    # browser to so that they can login
                    authURL = acConnection.getAuthorizationURL()

                    # The url returned by the getAuthorizationURL() method contains a 'state'
                    # query parameter. This is a session identifier that can be used in later
                    # requests to maintainconnection and session information.
                    # The session identifier can also be set to a user-defined value by calling
                    # the setSessionState() method on the connection right after the connection
                    # is created
                    state = parse_qs(urlparse(authURL).query)['state'][0]

                    # Here we set the session identifier to the value provided by the
                    # call to the getAuthroizationURL() method of the connection
                    acConnection.setSessionState(state)

                    # Store the connection object in the global connections dictionary using
                    # 'state' as the key
                    self.connectionDict[state] = acConnection

                    # Send the 302 temporary redirect response to the browser
                    self.send_response(302)
                    self.send_header("Location", authURL)
                    self.end_headers()
                    return
                except ConfigError as conferr:
                    print(conferr.msg)
                    raise
                except ConnectError as connecterr:
                    print(connecterr.msg)
                    raise

            # Handle the callback request after a login attempt for an
            # Authorization Code App. The path being checked must be
            # the same as that was registered for the App with ADP and
            # specified during the initialzation of the connection config object
            if real_path == '/callback':

                # A successful login returns an Authorization Code in the 'code'
                # query parameter
                try:
                    code = query_components['code'][0]
                except KeyError:
                    code = ''
                if (code == ''):
                    self.send_error(401, 'Unauthorized')
                    return
                resp = ''

                # The 'state' query parameter that as sent as part of the 302
                # redirect url is returned back. Use this to find the connection
                # from the global connection dictionary
                try:
                    state = query_components['state'][0]
                    acConnection = self.connectionDict[state]
                except KeyError:
                    # Send the 302 temporary redirect response to the browser
                    self.send_response(302)
                    self.send_header("Location", '/authorization_code')
                    self.end_headers()
                    return
                # Save the authorization code in the connection config
                acConnection.getConfig().setAuthorizationCode(code)

                # try to connect and handle exceptions
                # and send the response back
                try:
                    acConnection.connect()
                    if (acConnection.isConnectedIndicator()):
                        self.connectionDict[state] = acConnection
                        resp = '<b>Connected!</b>'
                        resp = resp + '<br>access token: ' + acConnection.getAccessToken()
                        resp = resp + '<br>expiration: ' + acConnection.getExpiration().strftime("%Y-%m-%d %H:%M:%S")
                        resp = resp + '<br>session state:' + acConnection.getSessionState()
                    else:
                        resp = '<b>Not Connected!</b>'
                except ConnectError as connecterr:
                    resp = '<b>Connection Error</b>'
                    resp = resp + '<br>Error Code: ' + connecterr.code
                    resp = resp + '<br>Error Message: ' + connecterr.msg
                    resp = resp + '<br>API Class: ' + connecterr.cname
                except:
                    print("Unexpected error:", str(sys.exc_info()))
                finally:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(resp)
                    return

            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith('.html'):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith('.jpg'):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith('.gif'):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith('.js'):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith('.css'):
                mimetype = 'text/css'
                sendReply = True

            if sendReply is True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), httpHandler)
    print('adp-connection-python version ' + __version__ + ' started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
