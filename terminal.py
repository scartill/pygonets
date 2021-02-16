import logging
import requests


MAX_TEXT_LEN = 1024


class Priority:
    NORMAL = 0
    HIGH = 1


class CommType:
    HYBRID = 0
    SATCOM = 1
    GSM = 2


class Terminal:
    def __init__(self, host: str, port: int, user: str, passwd: str):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def send_message(self, from_id: int, to_id: int, priority: int, comm_type: int, subject: str, text: str):
        if len(text) > MAX_TEXT_LEN:
            raise ValueError("Text is too long")

        message = {
            'from': from_id,
            'to': to_id,
            'priority': priority,
            'chSv': comm_type,
            'subj': subject,
            'msg': text
        }

        url = f'http://{self.host}:{self.port}/sendmsg.htm'
        logging.debug(f'Sending message with {url}')
        r = requests.post(url, params=message, auth=(self.user, self.passwd))

        print(r.text)

    def get_status(self):
        self._post('status.xml')

    def _post(self, path, params=None):
        with requests.Session() as s:
            logging.debug(f'Requesting status for {self.user} with {self.passwd[0:2]}')
            s.auth = (self.user, self.passwd)
            url = f'http://{self.host}:{self.port}/{path}'
            r = s.post(url, params=params)
            return r.text
