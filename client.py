#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import configparser
import json
import asn1tools
from dateutil import parser

CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read('settings.ini')
DEFAULT_CONFIG = CONFIG_PARSER['DEFAULT']

def set_variable(name):
    env_var = os.environ.get(name)
    if env_var:
        return env_var
    return DEFAULT_CONFIG[name]

SCHEMA_PATH = set_variable('PDC_SCHEMA_PATH')
CODEC_TYPE = set_variable('PDC_CODEC_TYPE').lower()
HOST = set_variable('PDC_HOST')
PORT = int(set_variable('PDC_PORT'))
ASN_TYPE_NAME = set_variable('PDC_ASN_TYPE_NAME')
CLIENT_DATA = set_variable('PDC_CLIENT_DATA_PATH')

class Client:

    def __init__(self):
        self.HOST = HOST  # The remote host
        self.PORT = PORT  # The same port as used by the server

        self.dat = asn1tools.compile_files(SCHEMA_PATH, codec=CODEC_TYPE)

    def run(self):
        with open(CLIENT_DATA) as file:
            data = json.load(file)
        for i in range(len(data)):
            data[i]['granularityPeriodEndTime'] = parser.parse(data[i]['granularityPeriodEndTime'])
        payload = self.dat.encode(ASN_TYPE_NAME, data)
        print('Encoded payload: ' + str(payload))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(payload)



def main():
    cli = Client()
    cli.run()


if __name__ == '__main__':
    main()
