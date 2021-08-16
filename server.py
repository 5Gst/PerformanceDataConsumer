#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys
import asn1tools
import logging
import requests
import configparser
from datetime import datetime
import asyncio

'''
UTCTime - datetime.datetime
'''

# environment; if not -> config
# add prefix [PDC]
config = configparser.ConfigParser()
config.read('settings.ini')
defconf = config['DEFAULT']
SCHEMA_PATH = defconf['SCHEMA_PATH']
CODEC_TYPE = defconf['CODEC_TYPE'].lower()
TELEGRAF_ADDRESS = defconf['TELEGRAF_ADDRESS']
HOST = defconf['HOST']
PORT = int(defconf['PORT'])
ASN_TYPE_NAME = defconf['ASN_TYPE_NAME']
LISTEN_SOCKETS_NUM = int(defconf['LISTEN_SOCKETS_NUM'])
BUFFER_SIZE = int(defconf['BUFFER_SIZE'])

class Server:

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.HOST = HOST
        self.PORT = PORT

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger('server')
        try:
            self.dat = asn1tools.compile_files(SCHEMA_PATH, codec=CODEC_TYPE)   #cache
        except:
            self.logger.error("Can't compile schema {} for codec {}".format(SCHEMA_PATH, CODEC_TYPE))
            sys.exit(1)

    def signal_handler(self, sig, frame):
        self.logger.info('Got signal {}. Server Stopped.'.format(sig))
        sys.exit(0)

    async def receive_data(self, reader, writer):
        self.logger.info('Connected to client')
        full_data = bytearray(b'')
        while True:
            data = await reader.read(BUFFER_SIZE)
            full_data += data
            self.logger.info('Server received: {}'.format(str(full_data)))
            if not data:
                if full_data != bytearray(b''):
                    self.logger.warning('Decoding failed')
                self.logger.info('Breaking connection')
                break
            while True:
                try:
                    decoded = self.dat.decode(ASN_TYPE_NAME, full_data)
                    check_encode = self.dat.encode(ASN_TYPE_NAME, decoded)
                    full_data = full_data[len(check_encode):]   #if data has more information
                    self.logger.info('payload: ' + str(decoded))
                except Exception as e:
                    self.logger.info('Decoding failed')
                    break
                try:
                    r = requests.post(TELEGRAF_ADDRESS, json=str(decoded))
                except:
                    self.logger.error('Receive to telegraf failed')

    async def run(self):
        server = await asyncio.start_server(self.receive_data, self.HOST, self.PORT)
        async with server:
            await server.serve_forever()

def main():
    srv = Server()
    asyncio.run(srv.run())
    
if __name__ == '__main__':
    main()
