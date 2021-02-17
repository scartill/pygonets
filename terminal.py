import logging
import xml.etree.ElementTree as ET

import requests


MAX_TEXT_LEN = 1024


class Priority:
    NORMAL = 0
    HIGH = 1


class CommType:
    HYBRID = 0
    SATCOM = 1
    GSM = 2


class GonetsException(ValueError):
    pass


class Terminal:
    def __init__(self, host: str, port: int, user: str, passwd: str, this_id: int):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.this_id = this_id

    def send_message(self, to_id: str, priority: int, comm_type: int, subject: str, text: str) -> bool:
        if len(text) > MAX_TEXT_LEN:
            raise ValueError("Text is too long")

        message = {
            'from': self.this_id,
            'to': to_id,
            'priority': priority,
            'chSv': comm_type,
            'subj': subject,
            'msg': text
        }

        url = f'http://{self.host}:{self.port}/sendmsg.htm'
        r = requests.post(url, params=message, auth=(self.user, self.passwd))

        logging.debug(f'Received {r.text}')
        if 'OK' not in r.text:
            raise GonetsException('Unable tot send')

    def get_status(self):
        return self._postforxml('status.xml')

    def get_rssi(self):
        return self._postforxml('statusg.xml')

    def get_geoposition(self):
        return self._postforxml('status2.xml')

    def get_counters(self):
        return self._postforxml('statusc.xml')

    def _postforxml(self, path):
        return ET.fromstring(self._post(path))

    def _post(self, path, params=None):
        with requests.Session() as s:
            logging.debug(f'Requesting status for {self.user} with {self.passwd[0:2]}')
            s.auth = (self.user, self.passwd)
            url = f'http://{self.host}:{self.port}/{path}'
            r = s.post(url, params=params)
            r.encoding = 'windows-1251'
            return r.text
