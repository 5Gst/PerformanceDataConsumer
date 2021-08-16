#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import asn1tools
import configparser
import datetime

config = configparser.ConfigParser()
config.read('settings.ini')
defconf = config['DEFAULT']
SCHEMA_PATH = defconf['PDC_SCHEMA_PATH']
CODEC_TYPE = defconf['PDC_CODEC_TYPE'].lower()
TELEGRAF_ADDRESS = defconf['PDC_TELEGRAF_ADDRESS']
HOST = defconf['PDC_HOST']
PORT = int(defconf['PDC_PORT'])
ASN_TYPE_NAME = defconf['PDC_ASN_TYPE_NAME']

'''
{
    streamId 0,
    granularityPeriodEndTime 991231235959+0200,
    measInfo [
        {
        measObjLdn "first",
        measResults {
            measId 1,
            measValue "qwerty"
        }
    }
    ]
}

{"streamId":0,"granularityPeriodEndTime":"991231235959","measInfo":[{"measObjLdn":"first","measResults":[{"measId":1,"measValue":"qwerty"}]}]}

{
    "streamId":5,
    "granularityPeriodEndTime":"991231235959",
[{"measObjLdn":"first", "measResults":[{"measId":1,"measValue":"qwerty"}, {"measId":2,"measValue":"abacaba"}]},
 {"measObjLdn":"second", "measResults":[{"measId":3,"measValue":"qwerty3"}, {"measId":4,"measValue":"abacaba4"}]}]
}

{"streamId":5,"granularityPeriodEndTime":datetime.datetime.now(),"measInfo":[{"measObjLdn":"first", "measResults":[{"measId":1,"measValue":"qwerty"}, {"measId":2,"measValue":"abacaba"}]},{"measObjLdn":"second", "measResults":[{"measId":3,"measValue":"qwerty3"}, {"measId":4,"measValue":"abacaba4"}]}]}
'''

class Client:

    def __init__(self):
        self.HOST = HOST  # The remote host
        self.PORT = PORT  # The same port as used by the server

        self.dat = asn1tools.compile_files(SCHEMA_PATH, codec=CODEC_TYPE)

    def run(self):
        print(datetime.datetime.now())
        #data = eval(input())
        data = [
            {
                "streamId": 0,
                "granularityPeriodEndTime": datetime.datetime.now(),
                "measInfo": [
                    {
                        "measObjLdn": "first",
                        "measResults": [
                            {
                                "measId": 1,
                                "measValue": "a"
                            },
                            {
                                "measId": 2,
                                "measValue": "b"
                            }
                        ]
                    },
                    {
                        "measObjLdn": "second",
                        "measResults": [
                            {
                                "measId": 3,
                                "measValue": "cd"
                            },
                            {
                                "measId":4,
                                "measValue": "efg"
                            }
                        ]
                    }
                ]
            },
                        {
                "streamId": 5,
                "granularityPeriodEndTime": datetime.datetime.now(),
                "measInfo": [
                    {
                        "measObjLdn": "third",
                        "measResults": [
                            {
                                "measId": 6,
                                "measValue": "hjklmno"
                            },
                            {
                                "measId": 7,
                                "measValue": "pqrstuvwxyz"
                            }
                        ]
                    },
                    {
                        "measObjLdn": "fourth",
                        "measResults": [
                            {
                                "measId": 8,
                                "measValue": "1asd3"
                            },
                            {
                                "measId": 9,
                                "measValue": "48r3w6e5fs1..../as.d/as.d/as.d````~~~~"
                            }
                        ]
                    }
                ]
            },
        ]
        payload = self.dat.encode(ASN_TYPE_NAME, data)
        print('Encoded payload: ' + str(payload))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            input()
            s.sendall(payload+payload)



def main():
    cli = Client()
    cli.run()


if __name__ == '__main__':
    main()
