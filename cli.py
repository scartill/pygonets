import argparse
import logging

from cmd2 import Cmd


from terminal import Terminal


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

    def do_status(self, _):
        print(self.term.get_status())

    def do_rssi(self, _):
        print(self.term.get_rssi())


def main():
    logging.basicConfig(level=logging.DEBUG)

    print('SS Gonets terminal control')
    app = App()
    app.cmdloop()


if __name__ == '__main__':
    main()
