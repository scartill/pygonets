import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom

from cmd2 import Cmd

from terminal import Terminal


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def xpprint(elem):
    print(prettify(elem))


def xprintfield(xml, field: str):
    if not field:
        xpprint(xml)
    else:
        children = xml.findall(field) + xml.findall(str.upper(field))
        for elem in children:
            print(elem.text)


class App(Cmd):
    def __init__(self):
        super().__init__()
        self.host = '192.168.1.55'
        self.port = 80
        self.user = 'user'
        self.passwd = 'user'
        self.term = None

    def do_host(self, host):
        logging.debug(f'Setting host to {host}')
        self.host = host

    def do_port(self, port):
        logging.debug(f'Setting port to {port}')
        self.port = port

    def do_init(self, _):
        logging.debug(f'Creating interface {self.host}:{self.port}')
        self.term = Terminal(self.host, self.port, self.user, self.passwd)

    def do_status(self, field):
        xprintfield(self.term.get_status(), field)

    def do_rssi(self, field):
        xprintfield(self.term.get_rssi(), field)

    def do_geoposition(self, field):
        xprintfield(self.term.get_geoposition(), field)

    def do_counters(self, field):
        xprintfield(self.term.get_counters(), field)


def main():
    logging.basicConfig(level=logging.DEBUG)

    print('SS Gonets terminal control')
    app = App()
    app.cmdloop()


if __name__ == '__main__':
    main()
