from telnetlib import Telnet
import time
import discord
import asyncio
import os
import threading
import re
import mud


def getvar(string, defaultstr='none'):
    sstring = str(string)
    if os.path.exists('.' + sstring):
        return open('.' + sstring, 'r').read()
    else:
        if sstring.upper() in os.environ.keys():
            return os.environ[sstring.upper()]
        else:
            return defaultstr


discordtoken = getvar(discord)


def discordtext(input):
    dstring = re.sub('\[.{,4}m', '', input)
    return '```' + dstring + '```'


def stringsplit(line, length):
    return [line[i:i+length] for i in range(0, len(line), length)]


def splitCount(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


client = discord.Client()
muds = []
mudstring = ''


def mudtext(mud):
    output = re.sub('\[.;36m!', '᥅', mud)  # unkillable mob
    output = re.sub('\[.;34m\+', '🔒', output)  # closed door
    output = re.sub('\[.;33m<', '▼', output)  # closed down exit
    output = re.sub('\[.;33m>', '▲', output)  # closed up exit
    output = re.sub('\[.;35m#', '♥', output)  # you icon
    return output


@client.event
async def on_ready():
    print('Logged in as {} Aardwolf'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global muds

    alreadyadded = False

    for i in muds:
        if message.channel == i.getchannel():
            alreadyadded = True
            activemud = i
            break

    if str(message.content).startswith('!mud'):
        if not alreadyadded:
            msgargs = str(message.content).split(' ')
            thismud = mud.Mud()
            if len(msgargs) >= 3:
                thismud.connect(msgargs[1], msgargs[2])
            else:
                thismud.connect()
            muds.append(thismud)
            thismud.read().start()
        else:
            await message.channel.send('channel already added')
        return

    activemud.execute(message.content)
    await asyncio.sleep(0.5)
    mudstring = activemud.getstring()
    if len(mudstring) >= 1600:
        for u in stringsplit(mudstring, 1000):
            await i.send(discordtext(u))
    else:
        if not discordtext(mudstring) == '``````':
            await i.send(discordtext(mudstring))
    activemud.resetmsg()

client.run(discordtoken)
