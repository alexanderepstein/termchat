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
import argparse
import threading

import hackchat.HChat as chat

currentVersion="0.0.1"

def getUser():
    import os
    import pwd
    return pwd.getpwuid(os.getuid())[0]

def parseArgs():
    parser = argparse.ArgumentParser(prog="tchat", description='Chat through the terminal with hack.chat', epilog="By: Alex Epstein https://github.com/alexanderepstein")
    parser.add_argument("-r", "--room", default="", help="Choose the name of the chatroom to enter")
    parser.add_argument("-n", "--nick", default=getUser(), help="Set the username for others to see")
    parser.add_argument("-v", "--version", action="store_true", help="Display the current version of tchat")
    args = parser.parse_args()
    return args

def getUserInput(nick, chatter):
    while chatter.ws.connected:
        message = input()
        chatter.send_message(message)

def main():
    args = parseArgs()
    if args.version and not (args.curses or args.room or args.nick):
        print(currentVersion)
    elif args.room == "":
        print("You must specify a room name to join")
        exit(1)
    else:
        chatter = chat.HChat(args.nick, args.room)
        try:
            chatter.run()
            threading.Thread(target=getUserInput(args.nick,chatter)).start()
        except KeyboardInterrupt:
            chatter.ws.abort()
            chatter.ws.close()
            print("\nChat exited")
            exit(0)


main()
