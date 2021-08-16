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

config = configparser.ConfigParser()
config.read('settings.ini')
defconf = config['DEFAULT']

def set_variable(name):
    env_var = os.environ.get(name)
    if env_var is not None:
        return env_var
    else:
        return defconf[name]

SCHEMA_PATH = set_variable('PDC_SCHEMA_PATH')
CODEC_TYPE = set_variable('PDC_CODEC_TYPE').lower()
TELEGRAF_ADDRESS = set_variable('PDC_TELEGRAF_ADDRESS')
HOST = set_variable('PDC_HOST')
PORT = int(set_variable('PDC_PORT'))
ASN_TYPE_NAME = set_variable('PDC_ASN_TYPE_NAME')
BUFFER_SIZE = int(set_variable('PDC_BUFFER_SIZE'))

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
                    full_data = full_data[len(check_encode):]   #if data has more information
                    self.logger.info('payload: ' + str(decoded))
                except:
                    self.logger.info('Decoding failed')
                    break
                try:
                    r = requests.post(TELEGRAF_ADDRESS, json=str(decoded))
                except:
                    self.logger.error('Receive to telegraf failed')

    async def run(self):
        server = await asyncio.start_server(self.receive_data, self.HOST, self.PORT)
        self.logger.info('Server started at {}:{}'.format(self.HOST, self.PORT))
        async with server:
            await server.serve_forever()

def main():
    srv = Server()
    asyncio.run(srv.run())
    
if __name__ == '__main__':
    main()
