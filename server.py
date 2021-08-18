#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys
import os
import asn1tools
import logging
import requests
import configparser
from datetime import datetime
import asyncio
import time

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
TELEGRAF_HOST = set_variable('PDC_TELEGRAF_HOST')
TELEGRAF_PORT = set_variable('PDC_TELEGRAF_PORT')
TELEGRAF_ADDRESS = "http://" + TELEGRAF_HOST + ":" + TELEGRAF_PORT + '/telegraf'
HOST = set_variable('PDC_HOST')
PORT = int(set_variable('PDC_PORT'))
ASN_TYPE_NAME = set_variable('PDC_ASN_TYPE_NAME')
BUFFER_SIZE = int(set_variable('PDC_BUFFER_SIZE'))
DEMO = set_variable('PDC_DEMO_MODE').lower() in ('true', '1', 't')

class Server:

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.HOST = HOST
        self.PORT = PORT

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger('server')
        try:
            self.dat = asn1tools.compile_files(SCHEMA_PATH, codec=CODEC_TYPE)
        except:
            self.logger.error("Can't compile schema {} for codec {}".format(SCHEMA_PATH, CODEC_TYPE))
            sys.exit(1)

    def signal_handler(self, sig, frame):
        self.logger.info('Got signal {}. Server Stopped.'.format(sig))
        sys.exit(0)

    async def receive_data(self, reader, writer):
        client_host, client_port = writer.get_extra_info('peername')
        client_addr = str(client_host) + ":" + str(client_port)
        self.logger.info('Connected to client {}'.format(client_addr))
        full_data = bytearray(b'')
        while True:
            data = await reader.read(BUFFER_SIZE)
            full_data += data
            self.logger.info('Server received {} from {}'.format(str(full_data), client_addr))
            if not data:
                if full_data != bytearray(b''):
                    self.logger.warning('Decoding failed')
                self.logger.info('Breaking connection with {}'.format(client_addr))
                break
            while True:
                try:
                    decoded = self.dat.decode(ASN_TYPE_NAME, full_data)
                    check_encode = self.dat.encode(ASN_TYPE_NAME, decoded)
                    full_data = full_data[len(check_encode):]   # if data has more information
                    self.logger.info('Payload: ' + str(decoded))
                except:
                    self.logger.info('Decoding failed')
                    break
                try:
                    message = []
                    if DEMO:
                        for pdsu in decoded:
                            for objldn in pdsu['measInfo']:
                                for meas in objldn['measResults']:
                                    pdsu_new = {
                                        'streamId': pdsu['streamId'],
                                        'granularityPeriodEndTime': int(time.mktime(pdsu['granularityPeriodEndTime'].timetuple())),
                                        'measObjLdn': objldn['measObjLdn'],
                                        'measId': meas['measId'],
                                        'measValue': int(meas['measValue']),
                                    }
                                    message.append(pdsu_new)
                        # In demo mode server sends arrray of metrics in this format: 
                        # {
                        #    'streamId': 5,
                        #    'granularityPeriodEndTime': 1629233240,
                        #    'measObjLdn': 'third',
                        #    'measId': 6,
                        #    'measValue': 4
                        # }
                    else:
                        if ASN_TYPE_NAME == 'PDSUs':    # Convert time in this schema to suitable format for telegraf
                            for i in range(len(decoded)):
                                decoded[i]['granularityPeriodEndTime'] = int(time.mktime(decoded[i]['granularityPeriodEndTime'].timetuple()))
                        message = decoded

                    r = requests.post(TELEGRAF_ADDRESS, json=message)
                except Exception as e:
                    self.logger.error('Send to telegraf failed: {}'.format(e))

    async def run(self):
        # sudo docker build . -t server
        # sudo docker run -p 50007:50007 --env PDC_DEMO_MODE=true server
        server = await asyncio.start_server(self.receive_data, self.HOST, self.PORT)
        self.logger.info('Server started at {}:{}'.format(self.HOST, self.PORT))
        if DEMO:
            self.logger.info('Server run in demo mode')
        async with server:
            await server.serve_forever()

def main():
    srv = Server()
    asyncio.run(srv.run())
    
if __name__ == '__main__':
    main()
