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
import curses
import curses.textpad
import locale
import threading

from time import sleep

from termchatUtils.HChat import HChat as chat



locale.setlocale(locale.LC_ALL, "")


def set_color_pairs():
    # based on the colors of pyradio
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)


class interface(object):
    startPos = 0
    # proportion of the left panel body, to the chat panel
    body_proportion = 0.20
    # proportion of textarea vertically to the chat panel
    text_area_proportion = 0.20

    def __init__(self, screen):
        self.stdscr = screen
        self.nickname = ""
        self.channel = ""
        # instantiate a Hackchat client
        self.showing = 0
        self.selection = 0
        self.messageNumber = 0
        self.amountOfUsers = 1

    def setup(self):
        """
        Method to run once that initializes a hackchat connection and the
        curses interface
        """
        self.chatter = chat(self.nickname, self.channel)
        #self.stdscr = curses.initscr()
        # define curses color pairs
        set_color_pairs()
        # set getch to blocking
        self.stdscr.nodelay(0)
        # don't echo key strokes on the screen
        curses.noecho()
        # read keystrokes instantly, without waiting for enter to be pressed
        curses.cbreak()
        # enable keypad mode
        self.stdscr.keypad(1)
        # draw the main frame
        self.setup_draw()
        curses.curs_set(0)
        # find what's the erase character
        self.del_char = curses.erasechar()
        self.chatter.run()
        self.backspace()
        self.refresh_body()

    def setup_draw(self):
        """
        Draws all of the windows for the curses interface
        """
        # get screen dimensions
        self.maxY, self.maxX = self.stdscr.getmaxyx()
        # n_lines, n_cols, begin_y, begin_x
        self.head_win = curses.newwin(1, self.maxX, 0, 0)
        # left panel, contacts
        self.body_win = curses.newwin(
            self.maxY - 1,
            int(self.maxX * self.body_proportion),
            1,
            0)
        # chat frame
        self.chat_win = curses.newwin(
            self.maxY - 1 - int(self.maxY * self.text_area_proportion),
            self.maxX - int(self.maxX * self.body_proportion),
            1,
            int(self.maxX * self.body_proportion))

        self.chatareaHeight = self.maxY - 1 - int(self.maxY * self.text_area_proportion) - 2
        # chat window (displays text)
        self.chatarea = curses.newwin(
            self.chatareaHeight,
            self.maxX - int(self.maxX * self.body_proportion) - 2,
            2,
            int(self.maxX * self.body_proportion) + 1)
        # bottom frame window
        self.text_win = curses.newwin(
            int(self.maxY * self.text_area_proportion),
            self.maxX - int(self.maxX * self.body_proportion),
            self.maxY - int(self.maxY * self.text_area_proportion),
            int(self.maxX * self.body_proportion))
        # bottom textarea
        self.textarea = curses.newwin(
            int(self.maxY * self.text_area_proportion) - 2,
            self.maxX - int(self.maxX * self.body_proportion) - 2,
            self.maxY - int(self.maxY * self.text_area_proportion) + 1,
            int(self.maxX * self.body_proportion) + 1)

        self.init_head()
        self.init_body()
        self.init_chat()
        self.init_chatarea()
        self.init_textbox()
        self.init_textarea()
        self.body_win.keypad(1)
        curses.doupdate()


    def init_head(self):
        name = "Channel: " + self.channel
        middle_pos = int(self.maxX/2 - len(name)/2)
        self.head_win.addstr(0, middle_pos, name, curses.color_pair(2))
        self.head_win.bkgd(' ', curses.color_pair(7))
        self.head_win.noutrefresh()

    def init_body(self):
        """
        Initializes the body/story window
        """
        self.bodyMaxY, self.bodyMaxX = self.body_win.getmaxyx()
        self.body_win.noutrefresh()
        self.refresh_body()

    def init_chat(self):
        """
        Draws the chat frame
        """
        self.chat_max_y, self.chat_max_x = self.chat_win.getmaxyx()
        self.chat_win.box()
        self.chat_win.refresh()

    def init_chatarea(self):
        """
        Draws the chat area to display chat text
        """
        self.chatarea.refresh()
        # represents the y position where to start writing chat
        self.chat_at = 0

    def init_textbox(self):
        """
        Draws the textbox under the chat window
        """
        self.text_win.box()
        self.text_win.refresh()

    def init_textarea(self):
        """
        Creates/refreshes the area for user input
        """
        # the current displayed text
        self.char_pos = [0, 0]
        self.text = ""
        self.textarea.refresh()
        self.refresh_textarea()

    def set_body_selection(self, number):
        """
        Select chat
        """
        self.selection = number
        maxDisplayedItems = self.bodyMaxY - 2
        if self.selection - self.startPos >= maxDisplayedItems:
            self.startPos = self.selection - maxDisplayedItems + 1
        elif self.selection < self.startPos:
            self.startPos = self.selection

    def refresh_body(self):
        """
        Sets the new selection on the body and clears the chat
        """
        if len(self.chatter.online_users) != self.amountOfUsers:
            self.body_win.erase()
            self.body_win.box()
            maxDisplay = self.bodyMaxY - 1
            for lineNum in range(maxDisplay - 1):
                i = lineNum + self.startPos
                if i < len(self.chatter.online_users):
                    self.__display_body_line(
                        lineNum, self.chatter.online_users[i])
            self.amountOfUsers = len(self.chatter.online_users)
            self.body_win.refresh()

    def __display_body_line(self, lineNum, station):
        """
        Highlights the user selection
        """
        col = curses.color_pair(5)

        # if the cursor is on the highligted chat/group
        is_current = self.selection == self.showing

        if lineNum + self.startPos == self.selection and is_current:
            col = curses.color_pair(9)
            self.body_win.hline(lineNum + 1, 1, ' ', self.bodyMaxX - 2, col)
        elif lineNum + self.startPos == self.selection:
            col = curses.color_pair(6)
            self.body_win.hline(lineNum + 1, 1, ' ', self.bodyMaxX - 2, col)
        elif lineNum + self.startPos == self.showing:
            col = curses.color_pair(4)
            self.body_win.hline(lineNum + 1, 1, ' ', self.bodyMaxX - 2, col)
        line = "{0}. {1}".format(lineNum + self.startPos + 1, station)
        self.body_win.addstr(lineNum + 1, 1, line, col)

    def refresh_textarea(self, char=None):
        """
        draws a border on the window
        """
        self.textarea.addstr(0, 0, self.text)
        self.textarea.refresh()

    def update_chat(self):
        """
        clears the chatbox and resets some things
        """
        self.chatarea.clear()
        self.chat_at = 0
        self.chatarea.refresh()

    def backspace(self):
        self.text = self.text[:-1]
        self.textarea.clear()
        self.refresh_textarea()

    def send_text(self):
        """
        Sends the string in textarea and clear the window
        """
        self.chatter.send_message(self.text)
        self.char_pos = [1, 1]
        self.text = ""
        self.textarea.clear()
        self.refresh_textarea()

    def push_chat(self,user,chat):
        """
        write the given string at the correct position
        in the chatarea
        """
        if user == self.nickname:
            col = curses.color_pair(8)
        else:
            col = curses.color_pair(1)

        try:
            self.chatarea.addstr(self.chat_at, 0, str(user) + ': ', col)
                # write the actual chat content
            self.chatarea.addstr(chat)
            self.chatarea.refresh()
            # update cursor
            self.chat_at, _ = self.chatarea.getyx()
            self.chat_at += 1
        except Exception:
            self.refreshChat()




    def run(self):
        """
        Method to call inside the main loop that keeps the interface
        """
        while True:
            c = self.body_win.getch()
            self.keypress(c)

    def refreshChat(self):
        self.chatarea.erase()
        self.chat_at = 0
        self.chatarea.refresh()
        self.messageNumber -= 3
        # the latter didn't produce the intended behavior (need to find a way to minimize the size of the array)
        """for i in range(2,0):
            self.push_chat(self.chatter.user_message[self.messageNumber-i], self.chatter.on_message[self.messageNumber-i])
        self.chatter.user_message = []
        self.chatter.on_message = []
        self.messageNumber = 0
        """

    def getMessages(self):
        """

        """
        while self.chatter.ws.connected:
            self.refresh_body()
            while len(self.chatter.on_message) > self.messageNumber:
                    self.push_chat(self.chatter.user_message[self.messageNumber], self.chatter.on_message[self.messageNumber])
                    self.messageNumber += 1
            sleep(60/1000)

    def checkResize(self):
        """
        Determine if the terminal has been resized and redraws the interface
        Fix this
        """
        while self.chatter.ws.connected:
            tempHeight, tempWidth = self.stdscr.getmaxyx()
            if self.maxX != tempWidth or self.maxY != tempHeight:
                self.maxY, self.maxX = self.stdscr.getmaxyx()
                if self.maxY < 5 or self.maxX < 5:
                    self.destruct()
                    print("You cannot make window that small")
                    exit(1)
                self.stdscr.clear()
                self.setup_draw()


    def destruct(self):
        """
        Restores the terminal window back to its original state
        """
        curses.echo()
        curses.curs_set(1)
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.endwin()

    def keypress(self, char):
        """
        Interprets the keypress responds based on the input
        """
        # moves to the user/group below current selection
        if char == curses.KEY_DOWN:
            if self.selection < len(self.chatter.online_users) - 1:
                self.set_body_selection(self.selection + 1)
            self.refresh_body()
            return

        # move cursor one position up
        elif char == curses.KEY_UP:
            if self.selection > 0:
                self.set_body_selection(self.selection - 1)
            self.refresh_body()
            return

        # send the content on the textbox
        elif char == curses.KEY_ENTER or chr(char) == "\n":
            if (self.text.replace(" ", "") != ""):
                self.chatter.on_message.append(self.text)
                self.chatter.user_message.append(self.nickname)
                self.messageNumber += 1
                self.push_chat(self.nickname,self.text)
                self.send_text()
                return
            else:
                self.char_pos = [1, 1]
                self.text = ""
                self.textarea.clear()
                self.refresh_textarea()

        # delete a character (windows, gnu linux, mac)
        elif chr(char) == self.del_char or chr(char) == "ć" or chr(char) == "\x7f":
            self.backspace()
            return

        # send the char to textbox area
        else:
            self.text += chr(char)
            self.refresh_textarea(char)
            return


# This method is callable for testing porpuses only
if __name__ == "__main__":
    ccurses = curses.wrapper(interface)
    ccurses.nickname = "tester"
    ccurses.channel = "testchannel"
    ccurses.setup()
    threading.Thread(target=ccurses.getMessages).start()
    threading.Thread(target=ccurses.checkResize).start()
    while True:
        try:
            ccurses.run()
        except KeyboardInterrupt:
            ccurses.destruct()
            ccurses.chatter.ws.abort()
            ccurses.chatter.ws.close()
            exit(0)
