import logging
import json
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
    def __init__(self, host: str, port: int, user: str, passwd: str):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def send_message(self, to_id: str, priority: int, comm_type: int, text: str):
        if len(text) > MAX_TEXT_LEN:
            raise ValueError("Text is too long")

        message = {
            'to': to_id,
            'urgency': priority,
            'chSv': comm_type,
            'subj': 'msg',
            'kvs': '000',  # Undocumented
            'msg': text
        }

        with requests.Session() as s:
            url = f'http://{self.host}:{self.port}/sendmsg2.xip'
            logging.debug(f'Sending message with {text}')
            s.auth = (self.user, self.passwd)

            # ND: not using standard urlencode
            payload_str = '&' + '&'.join('%s=%s' % (k,v) for k,v in message.items())
            logging.debug(f'Raw data {payload_str}')

            r = requests.post(url, data=payload_str, auth=(self.user, self.passwd)).json()

            logging.debug(f'Received {json.dumps(r, indent=2)}')
            err = r[0]['err']

            if err != 0:
                raise GonetsException(f'Unable to send ({err})')


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
