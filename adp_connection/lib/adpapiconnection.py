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

import requests
import datetime
import uuid
import logging
from connectexceptions import *
from connectionconfiguration import *
from adp_connection import __version__


class ADPAPIConnection(object):
    """ Base class for maintaining ADP connection status and information

    Instance Variables:
    connection: dictionary storing the connection status and access-token information
    connectionConfiguration: instance of the ConnectionConfiguration class
    that was used to instantiate the connection """

    connection = {'status': 'availabe', 'type': 'unknown', 'token': '',
                  'expires': '', 'sessionState': ''}
    connectionConfiguration = None
    userAgent = 'adp-userinfo-python/' + __version__

    def isConnectedIndicator(self):
        """ Returns: a boolen depending on whether the connection
        is 'connected' or not """
        return self.connection['status'] == 'connected'

    def getAccessToken(self):
        """ Returns: the access-token (Bearer Token) that was obtained
        as a result of a successful connection. Returns and empty
        string if no access-token is present """
        return self.connection['token']

    def getExpiration(self):
        """ Returns: the expiration date-time of the access-token
        as a datetime type. Returns an empty string if no
        access-token exists """
        return self.connection['expires']

    def getSessionState(self):
        """ Returns: the session state identifier that may have been
        generated either automatically, or user-defined when the connect()
        is successful """
        return self.connection['sessionState']

    def getConfig(self):
        """ Returns: the Connection Configuration object associated
        with the connection. The object maybe either ClientCredentialsConfiguration
        or AuthorizationCodeConfiguration depending on the type of
        application """
        return self.connectionConfiguration

    def setSessionState(self, sessionState):
        """ Inputs:
        sessionState: a string that uniquely identifies a session (e.g. a UUID) """
        self.connection['sessionState'] = sessionState

    def connect(self):
        """ Sends a POST to the ADP Token Server URL with necessary options and data
        like grant_type, ssl certificates, clientID and clientSecret. Upon a
        successful response, updates the connection information with the appropriate
        status and access-token data. Also sets to sessionState if not already set.
        On an unsuccessful attempt a ConnectError exception is raised """

        if self.getConfig().initDone is False:
            logging.debug('connecting without config init')
            raise ConfigError(self.__class__.__name__, Error.errDict['initBad']['errCode'], Error.errDict['initBad']['errMsg'])
        else:
            formData = {'grant_type': self.getConfig().getGrantType()}
            headers = {'user-agent': self.userAgent}
            r = requests.post(self.getConfig().getTokenServerURL(),
                              headers=(headers),
                              cert=(self.getConfig().getSSLCertPath(),
                                    self.getConfig().getSSLKeyPath()),
                              auth=(self.getConfig().getClientID(),
                                    self.getConfig().getClientSecret()),
                              data=(formData))
            logging.debug(r.status_code)
            logging.debug(r.json())
            if (r.status_code == requests.codes.ok):
                self.connection['status'] = 'connected'
                self.connection['token'] = r.json()['access_token']
                self.connection['expires'] = datetime.datetime.now() + datetime.timedelta(0, r.json()['expires_in'], 0)
                if self.getSessionState() == '':
                    self.setSessionState(str(uuid.uuid1()))
            else:
                raise ConnectError(self.__class__.__name__, str(r.status_code), 'Unable to connect to ADP')

    def disconnect(self):
        """ Sends a logout request to ADP if an access-token is present
        and resets the connection instance variable for the connection """
        if self.getAccessToken() != '':
            headers = {'user-agent': self.userAgent}            
            r = requests.get(self.getConfig().getDisconnectURL() + '?id_token_hint=' + self.getAccessToken(),
                             headers=(headers))
            logging.debug(r.status_code)
        self.connection = {'status': 'ready', 'type': 'unknown', 'token': '',
                           'expires': '', 'state': ''}


class ClientCredentialsConnection(ADPAPIConnection):
    """ Extends the ADPAPIConnection base class for a Client Credentials type application

    Attributes:
    connConfig: instance of ClientCredentialsConfiguration """

    def __init__(self, connConfig):
        """ Initialize the instance variables with client_credentials information """
        if (connConfig.getGrantType() == 'client_credentials'):
            self.connection['type'] = 'client_credentials'
            self.connection['status'] = 'ready'
            self.connectionConfiguration = connConfig


class AuthorizationCodeConnection(ADPAPIConnection):
    """ Extends the ADPAPIConnection base class for an Authorization Code type application

    Attributes:
    connConfig: instance of AuthorizationCodeConfiguration """

    def __init__(self, connConfig):
        """ Initialize the instance variables with authorization_code information """
        if (connConfig.getGrantType() == 'authorization_code'):
            self.connection['type'] = 'authorization_code'
            self.connection['status'] = 'ready'
            self.connectionConfiguration = connConfig

    def getAuthorizationURL(self):
        """ Generates a URL that must be used for redirecting the user's browser to
        for allowing them to login into ADP. The query parameters of the url are
        client_id, response_type, redirect_uri, scope and state. All the parameters
        except for state are obtained from the configuration object that was used for
        creating the connection.
        The state parameter is meant for allowing tracking of the session between the
        stateless http calls. If it has not been previously set to a user-defined
        value, it is set to a UUID when this method is called

        Returns: string representing the URL for redirecting the browser """
        authorizationURL = self.getConfig().getBaseAuthorizationURL() + '?client_id=' + self.getConfig().getClientID()
        authorizationURL = authorizationURL + '&response_type=' + self.getConfig().getResponseType()
        authorizationURL = authorizationURL + '&redirect_uri=' + self.getConfig().getRedirectURL()
        authorizationURL = authorizationURL + '&scope=' + self.getConfig().getScope()
        if self.getSessionState() == '':
            authorizationURL = authorizationURL + '&state=' + str(uuid.uuid1())
        else:
            authorizationURL = authorizationURL + '&state=' + self.getSessionState()
        return authorizationURL

    def connect(self):
        """ Sends a POST to the ADP Token Server URL with necessary options. These
        options are a little different from those sent for the client_credentials app.
        These include client_id, client_secret, grant_type, code (authorization_code),
        redirect_uri, and SSL certificates. Upon a successful response, updates the
        connection information with the appropriate status and access-token data.
        Also sets to sessionState if not already set.
        On an unsuccessful attempt a ConnectError exception is raised """

        if self.getConfig().initDone is False:
            logging.debug('connecting without config init')
            raise ConfigError(self.__class__.__name__, Error.errDict['initBad']['errCode'], Error.errDict['initBad']['errMsg'])

        headers = {'user-agent': self.userAgent}
        formData = {'client_id': self.getConfig().getClientID(),
                    'client_secret': self.getConfig().getClientSecret(),
                    'grant_type': self.getConfig().getGrantType(),
                    'code': self.getConfig().getAuthorizationCode(),
                    'redirect_uri': self.getConfig().getRedirectURL()}
        r = requests.post(self.getConfig().getTokenServerURL(),
                          headers=(headers),
                          cert=(self.getConfig().getSSLCertPath(),
                                self.getConfig().getSSLKeyPath()),
                          data=(formData))
        logging.debug(r.status_code)
        logging.debug(r.json())
        if (r.status_code == requests.codes.ok):
            self.connection['status'] = 'connected'
            self.connection['token'] = r.json()['access_token']
            self.connection['expires'] = datetime.datetime.now() + datetime.timedelta(0, r.json()['expires_in'], 0)
            if self.getSessionState() == '':
                self.setSessionState(str(uuid.uuid1()))
        else:
            raise ConnectError(self.__class__.__name__,  str(r.status_code), 'Unable to connect to ADP')
