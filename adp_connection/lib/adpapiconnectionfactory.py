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

from adp_connection.lib.adpapiconnection import *

logging.basicConfig(level=logging.DEBUG)


class ADPAPIConnectionFactory():
    """ Creates a connection instance and returns either a
    ClientCredentialsConnection or an AuthorizationCodeConnection
    depending on the initialized connection configuration provided """

    def __init__(self):
        self.connection_objects = {'authorization_code': AuthorizationCodeConnection,
                                   'client_credentials': ClientCredentialsConnection}

    def createConnection(self, connConfig):
        return self.connection_objects[connConfig.getGrantType()](connConfig)
