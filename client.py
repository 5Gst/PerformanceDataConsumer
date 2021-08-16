#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import asn1tools
import configparser
import datetime
from time import sleep
import json
from dateutil import parser
import os

config = configparser.ConfigParser()
config.read('settings.ini')
defconf = config['DEFAULT']

def set_variable(name):
    env_var = os.environ.get(name)
    if env_var:
        return env_var
    else:
        return defconf[name]

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
            input()
            s.sendall(payload[:10])
            sleep(2)
            s.sendall(payload[10:] + payload)



def main():
    cli = Client()
    cli.run()


if __name__ == '__main__':
    main()
