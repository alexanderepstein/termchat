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

from curses import wrapper
from termchatUtils import interface

currentVersion="0.0.4"

def getUser():
    import os
    import pwd
    return pwd.getpwuid(os.getuid())[0]

def parseArgs():
    parser = argparse.ArgumentParser(prog="termchat", description='Chat through the terminal with hack.chat', epilog="By: Alex Epstein https://github.com/alexanderepstein")
    parser.add_argument("-r", "--room", default="", help="Choose the name of the chatroom to enter")
    parser.add_argument("-n", "--nick", default=getUser(), help="Set the username for others to see")
    parser.add_argument("-v", "--version", action="store_true", help="Display the current version of tchat")
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()
    if args.version:
        print(currentVersion)
    elif args.room == "":
        print("You must specify a room name to join")
    else:
        ccurses = wrapper(interface.interface)
        ccurses.nickname = args.nick
        ccurses.channel = args.room
        ccurses.setup()
        threading.Thread(target=ccurses.getMessages).start()
        while True:
            try:
                ccurses.run()
            except KeyboardInterrupt:
                ccurses.destruct()
                ccurses.chatter.ws.abort()
                ccurses.chatter.ws.close()
                exit(0)
            except Exception:
                ccurses.destruct()
                ccurses.chatter.ws.abort()
                ccurses.chatter.ws.close()
                exit(1)
