
<div align="center">

# termchat

<img src="http://fc07.deviantart.net/fs71/f/2011/102/f/f/orangutan_logo_by_ohlaso-d3dta8g.png" height="300px" width="300px">

#### Chat through the terminal with hack.chat

![PythonVer](https://img.shields.io/pypi/pyversions/termchat.svg)
[![PyPI](https://img.shields.io/pypi/v/termchat.svg)](https://pypi.python.org/pypi/cryptowatch)![platform](https://img.shields.io/badge/platform-macOS%2C%20Linux%20%26%20Windows-blue.svg) [![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=plastic)]()

</div>

## Usage
[![termchat_1.png](https://s1.postimg.org/6uq7rg3han/termchat_1.png)](https://postimg.org/image/1qej263k23/)
```bash
usage: termchat [-h] [-r ROOM] [-n NICK] [-v]

Chat through the terminal with hack.chat

optional arguments:
  -h, --help            show this help message and exit
  -r ROOM, --room ROOM  Choose the name of the chatroom to enter
  -n NICK, --nick NICK  Set the username for others to see
  -v, --version         Display the current version of tchat
```

## Install
```bash
pip3 install termchat
```

## What's Special
There are a few things that is awesome about this project and [hack.chat](hack.chat) in general the first is they are both open source!

* Open source is love.

* [hack.chat](hack.chat) already never holds onto these chats unlike other services such as Skype as soon as all parties leave the chat all chat history is never again obtainable

* No one needs to sign up for an account, which is always a plus!

* Can be used from the terminal, so no web browser is necessary!

* By utilizing a client to interact with hack.chat we can add things like encryption (soon to come)

* Python and the curses interface go together like two peas in a pod

## Dependencies
  * Python 3
  * websocket-client

## Todo
  - [ ] Add end to end encryption
  - [ ] Check for an active connection status before starting the application
  - [ ] Check if message went through and the ip hasn't been rate limited
  - [ ] If user has left add a message to the chat from System with this info

## Special Thanks

#### Hack.chat
Without the hack.chat [project](https://github.com/AndrewBelt/hack.chat) by [AndrewBelt](https://github.com/AndrewBelt) deployed [here](hack.chat) this project would have been a lot more complicated as most of the heavy lifting is done by it.

#### Hackchat Chatbot Library
The Hchat.py file was largely based on [this project](https://github.com/gkbrk/hackchat/blob/master/hackchat.py) by [gkbrk](https://github.com/gkbrk) which was modified so that it could be used without the need for a bot.

#### Interface
The interface in this project was largely based on [this project](https://github.com/mathiasbc/slacky) by [mathiasbc](https://github.com/mathiasbc) which was modified to integrate with the hackchat library rather than the slack client.

##### Check out these projects because without them this would not have been possible :tada:

## Donate
If this project helped you in any way and you feel like supporting me

[![Donate](https://img.shields.io/badge/Donate-Venmo-blue.svg)](https://venmo.com/AlexanderEpstein)
[![Donate](https://img.shields.io/badge/Donate-SquareCash-green.svg)](https://cash.me/$AlexEpstein)

###### BTC: 1PSVVs6EnhdRGhUFb6Dz6EGWKKyHe3xACe
###### ETH: 0x585c4e1aa22d9Cc92d1a6b3fAe0c4a5274b5a884
###### LTC: Lf3SDjkck7iqy5TGn3wqzNvf5LL97JNhGk

## License

MIT License

Copyright (c) 2017 Alex Epstein

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
