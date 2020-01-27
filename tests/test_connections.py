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

from preggy import expect
from urlparse import urlparse, parse_qs
from adp_connection.lib import *
from tests.base import TestCase


class ClientCredentialsTestCase(TestCase):
    def test_cc_connected_true(self):
        config = dict({})
        config['clientID'] = '88a73992-07f2-4714-ab4b-de782acd9c4d'
        config['clientSecret'] = 'a130adb7-aa51-49ac-9d02-0d4036b63541'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'client_credentials'

        try:
            cconfig = ConnectionConfiguration()
            cconfig.setGrantType('client_credentials')
            ccConnectionBad = ADPAPIConnectionFactory().createConnection(cconfig)
            ccConnectionBad.connect()
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['initBad']['errCode'])

        ClientCredentialsConfiguration = ConnectionConfiguration().init(config)

        ccConnection = ADPAPIConnectionFactory().createConnection(ClientCredentialsConfiguration)

        ccConnection.connect()

        expect(ClientCredentialsConfiguration.getApiRequestURL()).to_equal('https://api.adp.com')
        expect(ClientCredentialsConfiguration.getDisconnectURL()).to_equal('https://accounts.adp.com/auth/oauth/v2/logout')
        expect(ccConnection.isConnectedIndicator()).to_be_true()

    def test_cc_configErr_missing_clientID(self):
        config = dict({})

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['clientID']['errCode'])

    def test_cc_configErr_missing_clientSecret(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['clientSecret']['errCode'])

    def test_cc_configErr_missing_sslCertPath(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['sslCertPath']['errCode'])

    def test_cc_configErr_missing_sslKeyPath(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['sslKeyPath']['errCode'])

    def test_cc_configErr_missing_tokenServerURL(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['tokenServerURL']['errCode'])

    def test_cc_configErr_missing_disconnectURL(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['disconnectURL']['errCode'])

    def test_cc_configErr_missing_apiRequestURL(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['apiRequestURL']['errCode'])

    def test_cc_configErr_missing_grantType(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['grantType']['errCode'])

    def test_cc_configErr_has_badgrantType(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'badgrantType'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['grantTypeBad']['errCode'])


class AuthorizationTestCase(TestCase):
    def test_ac_connected_returns400(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'
        config['baseAuthorizationURL'] = 'https://accounts.adp.com/auth/oauth/v2/authorize'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['redirectURL'] = 'http://localhost:8889/callback'
        config['responseType'] = 'code'
        config['scope'] = 'openid'

        try:
            cconfig = ConnectionConfiguration()
            cconfig.setGrantType('authorization_code')
            ccConnectionBad = ADPAPIConnectionFactory().createConnection(cconfig)
            ccConnectionBad.connect()
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['initBad']['errCode'])

        AuthorizationCodeConfiguration = ConnectionConfiguration().init(config)

        acConnection = ADPAPIConnectionFactory().createConnection(AuthorizationCodeConfiguration)

        authURL = acConnection.getAuthorizationURL()
        state = parse_qs(urlparse(authURL).query)['state'][0]
        acConnection.setSessionState(state)
        authURL = acConnection.getAuthorizationURL()
        acConnection.getConfig().setAuthorizationCode('dummy-auth-code ' + state)
        acConnection.setSessionState('')
        try:
            acConnection.connect()
        except ConnectError as connecterr:
            expect(connecterr.code).to_equal('400')
            expect(acConnection.getExpiration()).to_equal('')
            expect(acConnection.getAccessToken()).to_equal('')
            # set dummy access token to test disconnect
            acConnection.connection['token'] = 'dummy-token'
            acConnection.disconnect()
            expect(acConnection.getAccessToken()).to_equal('')

    def test_ac_configErr_missing_baseAuthorizationURL(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['baseAuthorizationURL']['errCode'])

    def test_ac_configErr_missing_redirectURL(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'
        config['baseAuthorizationURL'] = 'https://accounts.adp.com/auth/oauth/v2/authorize'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['redirectURL']['errCode'])

    def test_ac_configErr_missing_responseType(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'
        config['baseAuthorizationURL'] = 'https://accounts.adp.com/auth/oauth/v2/authorize'
        config['redirectURL'] = 'http://localhost:8889/callback'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['responseType']['errCode'])

    def test_ac_configErr_has_bad_responseType(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'
        config['baseAuthorizationURL'] = 'https://accounts.adp.com/auth/oauth/v2/authorize'
        config['redirectURL'] = 'http://localhost:8889/callback'
        config['responseType'] = 'codex1234'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['responseTypeBad']['errCode'])

    def test_ac_configErr_missing_scope(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'
        config['baseAuthorizationURL'] = 'https://accounts.adp.com/auth/oauth/v2/authorize'
        config['redirectURL'] = 'http://localhost:8889/callback'
        config['responseType'] = 'code'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['scope']['errCode'])

    def test_ac_configErr_has_bad_scope(self):
        config = dict({})
        config['clientID'] = 'e62f181c-3233-4636-bb82-9be5c9f3e3e0'
        config['clientSecret'] = 'fbce97f8-5d3a-42cc-a774-9126c5270625'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://api.adp.com'
        config['grantType'] = 'authorization_code'
        config['baseAuthorizationURL'] = 'https://accounts.adp.com/auth/oauth/v2/authorize'
        config['redirectURL'] = 'http://localhost:8889/callback'
        config['responseType'] = 'code'
        config['scope'] = 'openid121212'

        try:
            ConnectionConfiguration().init(config)
        except ConfigError as conferr:
            expect(conferr.code).to_equal(Error.errDict['scopeBad']['errCode'])
