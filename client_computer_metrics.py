#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from time import sleep
import configparser
import datetime
import os
from random import randint
import signal
import sys
import psutil
import asn1tools

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
        signal.signal(signal.SIGINT, self.signal_handler)
        self.HOST = HOST  # The remote host
        self.PORT = PORT  # The same port as used by the server

        self.dat = asn1tools.compile_files(SCHEMA_PATH, codec=CODEC_TYPE)

    def signal_handler(self, sig, frame):
        sys.exit(0)

    def run(self):
        data = [
            {
                "streamId": randint(1, 100000000000),
                "granularityPeriodEndTime": str(datetime.datetime.now()),
                "measInfo": [
                    {
                        "measObjLdn": "cpu",
                        "measResults": [
                            {
                                "measId": 0,
                                "measValue": ""
                            }
                        ]
                    },
                    {
                        "measObjLdn": "virtual_memory",
                        "measResults": [
                            {
                                "measId": 0,
                                "measValue": ""
                            }
                        ]
                    },
                    {
                        "measObjLdn": "temperature",
                        "measResults": [
                            {
                                "measId": 0,
                                "measValue": ""
                            },
                            {
                                "measId": 1,
                                "measValue": ""
                            },
                            {
                                "measId": 2,
                                "measValue": ""
                            },
                            {
                                "measId": 3,
                                "measValue": ""
                            },
                        ]
                    },
                    {
                        "measObjLdn": "cpu_frequency",
                        "measResults": [
                            {
                                "measId": 0,
                                "measValue": ""
                            },
                            {
                                "measId": 1,
                                "measValue": ""
                            },
                            {
                                "measId": 2,
                                "measValue": ""
                            },
                        ]
                    },
                ]
            }
        ]
        cpu_measValue = 0
        virtual_memory_measValue = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            while True:
                data[0]['granularityPeriodEndTime'] = datetime.datetime.now()

                cpu_measValue = psutil.cpu_percent()
                virtual_memory_measValue = psutil.virtual_memory().percent
                data[0]['measInfo'][0]['measResults'][0]['measValue'] = str(cpu_measValue)
                data[0]['measInfo'][1]['measResults'][0]['measValue'] = str(virtual_memory_measValue)

                temp = psutil.sensors_temperatures()
                num = -1
                for core in temp['coretemp']:
                    if num == -1:
                        num += 1
                        continue
                    data[0]['measInfo'][2]['measResults'][num]['measValue'] = str(core.current)
                    num += 1
                
                cpu_freq = psutil.cpu_freq()
                data[0]['measInfo'][3]['measResults'][0]['measValue'] = str(cpu_freq.current)
                data[0]['measInfo'][3]['measResults'][1]['measValue'] = str(cpu_freq.min)
                data[0]['measInfo'][3]['measResults'][2]['measValue'] = str(cpu_freq.max)
                
                payload = self.dat.encode(ASN_TYPE_NAME, data)
                print('Payload: ' + str(data))
                print('Encoded payload: ' + str(payload))

                s.sendall(payload)
                sleep(1)



def main():
    cli = Client()
    cli.run()


if __name__ == '__main__':
    main()
