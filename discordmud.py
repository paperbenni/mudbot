from telnetlib import Telnet
import time
import discord
import asyncio
import os
import threading
import re

if os.path.exists('.token'):
    discordtoken = open('.token', 'r').read()
    print(discordtoken)
else:
    discordtoken = os.environ['DISCORD']


def discordtext(input):
    dstring = re.sub('\[.{,4}m', '', input)
    return '```' + dstring + '```'


def stringsplit(line, length):
    return [line[i:i+length] for i in range(0, len(line), length)]


def splitCount(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


client = discord.Client()
tn = Telnet('aardmud.org', 4000)
tn.read_until(b'adventurer?')
time.sleep(1)
tn.write(b'discorder\n')
time.sleep(1)
tn.write(b'discord\n')
time.sleep(1)
tn.write(b'\n')
mudchannels = []
mudstring = ''


def outputrec():
    global tn
    global mudstring
    print('global outputrec')
    while not client.is_closed():
        output = url = re.sub('\\n$', '', tn.read_until(b'\n').decode(
            'utf-8'))
        # green exclamation marks
        output = re.sub('\[.;36m!', '᥅', output)
        output = re.sub('\[.;34m\+', '🔒', output)
        output = re.sub('\[.;33m<', '▼', output)
        output = re.sub('\[.;33m>', '▲', output)
        print(output)
        mudstring += output


threadd = threading.Thread(name='messager', target=outputrec)
threadd.start()


@client.event
async def on_ready():
    print('Logged in as {} Aardwolf'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global mudchannels
    global mudstring
    if message.content == '!mud':
        print("added new channel")
        if not message.channel in mudchannels:
            mudchannels.append(message.channel)
            await message.channel.send('mud channel {} added'.format(message.channel.name))
        return
    if not message.channel in mudchannels:
        return
    # prevent players crashing the game
    if message.content == 'quit':
        return
    if message.content != '!':
        print('sending command')
        if message.content == '!!':
            tn.write(b'\n')

        tn.write(bytes(message.content, encoding='utf8') + b'\n')
    await asyncio.sleep(0.5)
    for i in mudchannels:
        if len(mudstring) >= 1600:
            for u in stringsplit(mudstring, 1000):
                await i.send(discordtext(u))
        else:
            if not discordtext(mudstring) == '``````':
                await i.send(discordtext(mudstring))
    mudstring = ''
client.run(discordtoken)
