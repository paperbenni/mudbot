import telnetlib
import time


class Mud:
    def __init__(self):
        self.logged_in = False

    def connect(self, host='aardmud.org', port='4000'):
        self.tn = telnetlib.Telnet(host, port)

    def login(self, username=b'discorder', password=b'discord'):
        self.username = username
        self.password = password
        if self.logged_in:
            print(username, 'already logged in')
        else:
            self.tn.read_until(b'adventurer?')
            time.sleep(1)
            self.tn.write(self.username + b'\n')
            time.sleep(1)
            self.tn.write(self.password + b'discord\n')
            time.sleep(0.5)
            self.tn.write(b'\n')

    def execute(self, command):
        try:
            self.tn.write(bytes(command, encoding='utf8'))
        except:
            self.login(self.username, self.password)
            time.sleep(0.2)
            print(self.username, 'reconnecting')
            self.execute(command)
