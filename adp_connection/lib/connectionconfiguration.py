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

import logging
from adp_connection.lib.connectexceptions import *


class ConnectionConfiguration(object):
    """ Base class for the connection configuration object.

    Instance Variables:
    config: a dictionary of all the configuration
    parameters required for setting up a connection
    initDone: tracks whether the configuration has been
    initialized """

    config = dict({})
    initDone = False

    def __init__(self):
        """ Initialize the dictionary keys:
        clientID, clientSecret, sslCertPath, sslKeyPath, tokenServerURL,
        apiRequestURL, baseAuthorizationURL, redirectURL, responseType,
        scope, grantType, authorizationCode, disconnectURL """
        logging.debug('creating base config class')
        self.config['clientID'] = ''
        self.config['clientSecret'] = ''
        self.config['sslCertPath'] = ''
        self.config['sslKeyPath'] = ''
        self.config['tokenServerURL'] = ''
        self.config['apiRequestURL'] = ''
        self.config['baseAuthorizationURL'] = ''
        self.config['redirectURL'] = ''
        self.config['responseType'] = ''
        self.config['scope'] = ''
        self.config['grantType'] = ''
        self.config['authorizationCode'] = ''
        self.config['disconnectURL'] = ''

    def setClientID(self, clientID):
        self.config['clientID'] = clientID

    def setClientSecret(self, clientSecret):
        self.config['clientSecret'] = clientSecret

    def setSSLCertPath(self, sslCertPath):
        self.config['sslCertPath'] = sslCertPath

    def setSSLKeyPath(self, sslKeyPath):
        self.config['sslKeyPath'] = sslKeyPath

    def setTokenServerURL(self, tokenServerURL):
        self.config['tokenServerURL'] = tokenServerURL

    def setApiRequestURL(self, apiRequestURL):
        self.config['apiRequestURL'] = apiRequestURL

    def setDisconnectURL(self, disconnectURL):
        self.config['disconnectURL'] = disconnectURL

    def setGrantType(self, grantType):
        self.config['grantType'] = grantType

    def getClientID(self):
        return self.config['clientID']

    def getClientSecret(self):
        return self.config['clientSecret']

    def getSSLCertPath(self):
        return self.config['sslCertPath']

    def getSSLKeyPath(self):
        return self.config['sslKeyPath']

    def getTokenServerURL(self):
        return self.config['tokenServerURL']

    def getApiRequestURL(self):
        return self.config['apiRequestURL']

    def getDisconnectURL(self):
        return self.config['disconnectURL']

    def getGrantType(self):
        return self.config['grantType']

    def init(self, configObj):
        """ Method to initialize the common config parameters:
        clientID, clientSecret, sslCertPath, sslKeyPath,
        tokenServerURL, apiRequestURL, disconnectURL and grantType.

        Attributes:
        configObj: dictionary containing the config values to be
        initialized. """

        logging.debug('Initializing Config Object')
        if ('clientID' in configObj):
            self.setClientID(configObj['clientID'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['clientID']['errCode'] + ': ' + Error.errDict['clientID']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['clientID']['errCode'], Error.errDict['clientID']['errMsg'])
        if ('clientSecret' in configObj):
            self.setClientSecret(configObj['clientSecret'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['clientSecret']['errCode'] + ': ' + Error.errDict['clientSecret']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['clientSecret']['errCode'], Error.errDict['clientSecret']['errMsg'])
        if ('sslCertPath' in configObj):
            self.setSSLCertPath(configObj['sslCertPath'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['sslCertPath']['errCode'] + ': ' + Error.errDict['sslCertPath']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['sslCertPath']['errCode'], Error.errDict['sslCertPath']['errMsg'])
        if ('sslKeyPath' in configObj):
            self.setSSLKeyPath(configObj['sslKeyPath'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['sslKeyPath']['errCode'] + ': ' + Error.errDict['sslKeyPath']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['sslKeyPath']['errCode'], Error.errDict['sslKeyPath']['errMsg'])
        if ('tokenServerURL' in configObj):
            self.setTokenServerURL(configObj['tokenServerURL'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['tokenServerURL']['errCode'] + ': ' + Error.errDict['tokenServerURL']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['tokenServerURL']['errCode'], Error.errDict['tokenServerURL']['errMsg'])
        if ('disconnectURL' in configObj):
            self.setDisconnectURL(configObj['disconnectURL'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['disconnectURL']['errCode'] + ': ' + Error.errDict['disconnectURL']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['disconnectURL']['errCode'], Error.errDict['disconnectURL']['errMsg'])
        if ('apiRequestURL' in configObj):
            self.setApiRequestURL(configObj['apiRequestURL'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['apiRequestURL']['errCode'] + ': ' + Error.errDict['apiRequestURL']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['apiRequestURL']['errCode'], Error.errDict['apiRequestURL']['errMsg'])
        if ('grantType' in configObj):
            self.setGrantType(configObj['grantType'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['grantType']['errCode'] + ': ' + Error.errDict['grantType']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['grantType']['errCode'], Error.errDict['grantType']['errMsg'])
        if (configObj['grantType'] == 'client_credentials'):
            ccConfig = ClientCredentialsConfiguration()
            ccConfig.initDone = True
            return ccConfig
        elif (configObj['grantType'] == 'authorization_code'):
            acConfig = AuthorizationCodeConfiguration()
            acConfig.init(configObj)
            acConfig.initDone = True
            return acConfig
        else:
            logging.debug('Conf Error: ' + Error.errDict['grantTypeBad']['errCode'] + ': ' + Error.errDict['grantTypeBad']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['grantTypeBad']['errCode'], Error.errDict['grantTypeBad']['errMsg'])


class ClientCredentialsConfiguration(ConnectionConfiguration):
    """ Client credentials sub class of the ConnectionConfiguration object """

    def __init__(self):
        pass


class AuthorizationCodeConfiguration(ConnectionConfiguration):
    """ Authorization Code sub class of the ConnectionConfiguration object """

    def __init__(self):
        pass

    def init(self, configObj):
        """ Method to initialize additional configuration parameters
        specific to the Authorization Code type application

        Attributes:
        configObj: dictionary containing the Authorization Code specific
        config values to be initialized. """

        logging.debug('Initializing config object for Authorization Code type application')
        if ('baseAuthorizationURL' in configObj):
            self.setBaseAuthorizationURL(configObj['baseAuthorizationURL'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['baseAuthorizationURL']['errCode'] + ': ' + Error.errDict['baseAuthorizationURL']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['baseAuthorizationURL']['errCode'],
                              Error.errDict['baseAuthorizationURL']['errMsg'])
        if ('redirectURL' in configObj):
            self.setRedirectURL(configObj['redirectURL'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['redirectURL']['errCode'] + ': ' + Error.errDict['redirectURL']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['redirectURL']['errCode'], Error.errDict['redirectURL']['errMsg'])
        if ('responseType' in configObj):
            if (configObj['responseType'] == 'code'):
                self.setResponseType(configObj['responseType'])
            else:
                logging.debug('Conf Error: ' + Error.errDict['responseTypeBad']['errCode'] + ': ' + Error.errDict['responseTypeBad']['errMsg'])
                raise ConfigError(self.__class__.__name__, Error.errDict['responseTypeBad']['errCode'], Error.errDict['responseTypeBad']['errMsg'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['responseType']['errCode'] + ': ' + Error.errDict['responseType']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['responseType']['errCode'], Error.errDict['responseType']['errMsg'])
        if ('scope' in configObj):
            if (configObj['scope'] == 'openid'):
                self.setScope(configObj['scope'])
            else:
                logging.debug('Conf Error: ' + Error.errDict['scopeBad']['errCode'] + ': ' + Error.errDict['scopeBad']['errMsg'])
                raise ConfigError(self.__class__.__name__, Error.errDict['scopeBad']['errCode'], Error.errDict['scopeBad']['errMsg'])
        else:
            logging.debug('Conf Error: ' + Error.errDict['scope']['errCode'] + ': ' + Error.errDict['scope']['errMsg'])
            raise ConfigError(self.__class__.__name__, Error.errDict['scope']['errCode'], Error.errDict['scope']['errMsg'])

    def getBaseAuthorizationURL(self):
        return self.config['baseAuthorizationURL']

    def getRedirectURL(self):
        return self.config['redirectURL']

    def getResponseType(self):
        return self.config['responseType']

    def getScope(self):
        return self.config['scope']

    def getAuthorizationCode(self):
        return self.config['authorizationCode']

    def setBaseAuthorizationURL(self, baseAuthorizationURL):
        self.config['baseAuthorizationURL'] = baseAuthorizationURL

    def setRedirectURL(self, redirectURL):
        self.config['redirectURL'] = redirectURL

    def setResponseType(self, responseType):
        self.config['responseType'] = responseType

    def setScope(self, scope):
        self.config['scope'] = scope

    def setAuthorizationCode(self, authorizationCode):
        self.config['authorizationCode'] = authorizationCode
