import time
import discord
import asyncio
import os
import threading
import re
import mud


def getvar(string, defaultstr='none'):
    sstring = str(string)
    if os.path.exists('.' + sstring.lower()):
        outstring = open('.' + sstring, 'r').read()
        return outstring
    else:
        if sstring.upper() in os.environ.keys():
            return os.environ[sstring.upper()]
        else:
            return defaultstr


discordtoken = getvar('discord')
print(discordtoken)


def mudtext(mud):
    output = re.sub('\[.;36m!', '᥅', mud)  # unkillable mob
    output = re.sub('\[.;34m\+', '🔒', output)  # closed door
    output = re.sub('\[.;33m<', '▼', output)  # closed down exit
    output = re.sub('\[.;33m>', '▲', output)  # closed up exit
    output = re.sub('\[.;35m#', '♥', output)  # you icon
    return output


def discordtext(input):

    dstring = re.sub('\[.{,4}m', '', mudtext(input))
    return '```' + dstring + '```'


def stringsplit(line, length):
    return [line[i:i+length] for i in range(0, len(line), length)]


def splitCount(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


client = discord.Client()
muds = []
mudstring = ''


@client.event
async def on_ready():
    print('Logged in as {} Aardwolf'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global muds

    alreadyadded = False
    if muds:
        for i in muds:
            if message.channel == i.getchannel():
                alreadyadded = True
                activemud = i
                break

    if message.content.startswith('!mud'):
        print("mud command")
        if not alreadyadded:
            msgargs = str(message.content).split(' ')
            thismud = mud.Mud()
            thismud.setchannel(message.channel)
            if len(msgargs) >= 3:
                thismud.connect(msgargs[1], msgargs[2])
            else:
                thismud.connect()
            muds.append(thismud)
            thismud.read(thismud, muds).start()
            await thismud.getchannel().send('mud channel added')
            alreadyadded = True
            activemud = thismud
        else:
            await message.channel.send('channel already added')
    else:
        if not alreadyadded:
            return
        activemud.execute(message.content)
    mudstring = ''
    while activemud.getstring() == '':
        await asyncio.sleep(0.1)

    mudstring = activemud.getstring()
    if len(mudstring) >= 1600:
        for u in stringsplit(mudstring, 1000):
            await activemud.getchannel().send(discordtext(u))
    else:
        if not discordtext(mudstring) == '``````':
            await activemud.getchannel().send(discordtext(mudstring))
    activemud.resetmsg()

client.run(discordtoken)
