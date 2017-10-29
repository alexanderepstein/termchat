#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2017 Alex Epstein

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import threading
from sys import stdout
from time import time as pingTime

try:
    import websocket
    getattr(websocket, 'create_connection')
except AttributeError:
    print("Error: you must uninstall websocket to use websocket-client due to naming conflicts")
except ImportError:
    print("You must have websocket-client installed to use tchat")
    exit(1)

class HChat:

    def __init__(self, nick, channel):
        """Connects to a channel on https://hack.chat.
        Keyword arguments:
        nick -- <str>; the nickname to use upon joining the channel
        channel -- <str>; the channel to connect to on https://hack.chat
        """
        self.nick = nick
        self.channel = channel
        self.online_users = []
        self.on_message = []
        self.user_message = []

    def send_message(self, msg):
        """Sends a message on the channel."""
        self._send_packet({"cmd": "chat", "text": msg})
        stdout.flush()

    def _send_packet(self, packet):
        """Sends <packet> (<dict>) to https://hack.chat."""
        encoded = json.dumps(packet)
        if self.ws.connected:
            self.ws.send(encoded)

    def run(self):
        print("Connecting...", end = "")
        try:
            self.ws = websocket.create_connection("wss://hack.chat/chat-ws")
            self.pingDelay = pingTime()
            self.pingThread = threading.Thread(target=self.pingThread)
            self.chatThread = threading.Thread(target=self.chatThread)
            self._send_packet({"cmd": "join", "channel": self.channel, "nick": self.nick})
            self.chatThread.start()
            self.pingThread.start()
            print("Success!")
        except Exception as err:
            print("Failure!")
            print(err)
            exit(1)



    def chatThread(self):
        while self.ws.connected:
            try:
                result = json.loads(self.ws.recv())
            except  websocket._exceptions.WebSocketConnectionClosedException:
                exit(0)
            if result["cmd"] == "chat" and not result["nick"] == self.nick:
                self.user_message.append(result["nick"])
                self.on_message.append(result["text"])
            elif result["cmd"] == "onlineAdd":
                self.online_users.append(result["nick"])
            elif result["cmd"] == "onlineRemove":
                self.online_users.remove(result["nick"])
            elif result["cmd"] == "onlineSet":
                for nick in result["nicks"]:
                    self.online_users.append(nick)

    def pingThread(self):
        """Retains the websocket connection."""
        try:
            while self.ws.connected:
                tempTime = pingTime()
                if tempTime - self.pingDelay >= 60:
                    self.pingDelay = pingTime()
                    self._send_packet({"cmd": "ping"})
        except websocket._exceptions.WebSocketConnectionClosedException:
            exit(1)
