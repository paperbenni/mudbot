import telnetlib
import time
import threading
import discord
import re

class Mud:

    def __init__(self):
        self.logged_in = False
        self.messages = ''

    def connect(self, host=False, port=False):
        if host:
            if not port:
                port = 23
        else:
            host = 'aardmud.org'
            port = 4000
        self.host = host
        self.port = port
        self.username = b'discorder'
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
        execommand = bytes(command, encoding='utf8')
        if command == '!':
            return
        if command == '!!':
            execommand = b'\n'
        else:
            execommand = execommand + b'\n'
        try:
            self.tn.write(execommand)
        except:
            self.connect(self.host, self.port)
            time.sleep(0.2)
            print(self.username.decode('utf-8'), 'reconnecting')
            self.execute(command)

    def read(self, mudd, mudlist):
        def reader():
            while True:

                try:
                    output = re.sub(
                        '\\n$', '', mudd.tn.read_until(b'\n').decode('utf-8'))
                    self.messages += output
                except:
                    print("mud removed")
                    mudlist.remove(mudd)
                    break
        return threading.Thread(target=reader)

    def getstring(self):
        return self.messages

    def resetmsg(self):
        self.messages = ''

    def setchannel(self, channel):
        self.channel = channel

    def getchannel(self):
        return self.channel
