import curses

class ccurses(object):

    def __init__(self, screen):
        self.screen = curses.initscr()
        self.screenHeight,self.screenWidth = self.screen.getmaxyx()
        curses.cbreak()
        curses.curs_set(0)
        curses.noecho()
        #self.screen.scrollok(1)
        self.drawInfoBox()
        self.refresh()

    def refresh(self):
        self.screen.refresh()

    def drawInfoBox(self):
        self.infoBox = curses.newwin(int(self.screenHeight/10), int(self.screenWidth)-1, 0, 0)
        self.infoBox.immedok(True)
        self.infoBox.box()
        self.infoBox.addstr("name")

    def clearScreen(self):
        self.screen.clear()

    def checkResize(self):
        tempHeight, tempWidth = self.screen.getmaxyx()
        if self.screenWidth != tempWidth or self.screenHeight != tempHeight:
            self.screenHeight, self.screenWidth = self.screen.getmaxyx()
            self.screen.clear()
            self.infoBox.clear()
            self.drawInfoBox()
            self.refresh()


    def destruct(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

def main():
    from curses import wrapper as wrapper
    chatCurses = wrapper(ccurses)
    chatCurses.refresh()
    try:
        while True:
            chatCurses.checkResize()
    except KeyboardInterrupt:
        chatCurses.destruct()


main()
