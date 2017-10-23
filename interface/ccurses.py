import curses

class ccurses(object):

    def __init__(self, screen, channel="chan", nickname="nick"):
        self.screen = curses.initscr()
        self.channel = channel
        self.nickname = nickname
        self.screenHeight,self.screenWidth = self.screen.getmaxyx()
        curses.cbreak()
        curses.curs_set(0)
        curses.noecho()
        self.screen.scrollok(1)
        self.drawSkeleton()
        self.refresh()

    def refresh(self):
        self.screen.refresh()

    def drawInfoBox(self):
        self.infoBox = curses.newwin(int(self.screenHeight/10), int(self.screenWidth), 0, 0)
        self.infoBox.immedok(True)
        self.infoBox.box()
        self.infoBox.addstr(int(self.screenHeight/20), int(self.screenWidth/8)-5, "Username: " + self.nickname)
        self.infoBox.addstr(int(self.screenHeight/20), int(self.screenWidth/2)-5, "Channel: " + self.channel)

    def clearScreen(self):
        self.screen.clear()

    def checkResize(self):
        tempHeight, tempWidth = self.screen.getmaxyx()
        if self.screenWidth != tempWidth or self.screenHeight != tempHeight:
            self.screenHeight, self.screenWidth = self.screen.getmaxyx()
            self.clearScreen()
            self.refresh()
            self.drawSkeleton()

    def drawChatBox(self):
        self.padHeight = int(self.screenHeight) - int(self.screenHeight/20) - int(self.screenHeight/4)
        self.padWidth = self.screenWidth-1
        self.chatBox = curses.newwin(self.padHeight+2, self.padWidth+1, int(self.screenHeight/10), 0)
        self.chatBox.immedok(True)
        self.chatBox.box()
        self.pad = curses.newpad(self.padHeight, self.padWidth)
        self.pad.addstr(0,0,"hello")
        self.pad.refresh(0,0, 5,5, 20,75)

    def drawTextField(self):
        self.tBoxHeight = int(self.screenHeight - self.padHeight - self.screenHeight/10) - 1
        self.tBoxWidth = int(self.screenWidth)
        self.tBox = curses.newwin(self.tBoxHeight, self.tBoxWidth, int(self.screenHeight/10) + self.tBoxHeight*3 + 5, 0)
        self.tBox.immedok(True)
        self.tBox.box()

    def drawSkeleton(self):
        self.drawInfoBox()
        self.drawChatBox()
        #self.drawTextField()

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
            chatCurses.refresh()
            chatCurses.checkResize()
    except KeyboardInterrupt:
        chatCurses.destruct()


main()
