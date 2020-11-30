# Shark Game GUI Handler (Benjamin Antupit)

from graphics import *

from Button import Button


class SharkGUI:

    def __init__(self):
        self.win = GraphWin("Water World", 1200, 800, False)
        self.background = Image(Point(600, 399),
                                "fish-grid-01.png").draw(self.win)
        self.entries = [Entry(Point(308, 190), 8),
                        Entry(Point(308, 270), 8),
                        Entry(Point(308, 350), 8)]

        for entry in reversed(self.entries):
            entry.draw(self.win).setSize(26)
            entry.setFill("#80A5AF")
            entry.setTextColor("#FFFFFF")
            entry.entry.config(relief=tk.FLAT, borderwidth=3,
                               highlightbackground="#B1E5FC",
                               highlightcolor="#FFFFFF",
                               highlightthickness=3,
                               disabledbackground="#5098B4",
                               disabledforeground="#B1E5FC")

        self.start_button = Button(self.win, Point(215, 430),
                                   316, 48, "Start")
        self.move_button = Button(self.win, Point(212, 664),
                                  316, 48, "Move").deactivate()
        self.quit_button = Button(self.win, Point(212, 736), 320, 48, "")
        self.quit_button.setFill("").setOutline("")
        self.message = Text(Point(212, 568), "Enter Fish Coordinates \n"
                                             "and select Start to begin")
        self.message.draw(self.win).setTextColor("#B1E5FC")
        self.message.setSize(24)

    def disableEntry(self):
        for entry in self.entries:
            entry.entry.config(state=tk.DISABLED, highlightcolor="#B1E5FC")

    def getCoordinates(self) -> list:
        return [self.entries[0].getText().strip("( )").split(",", 1),
                self.entries[1].getText().strip("( )").split(",", 1),
                self.entries[1].getText().strip("( )").split(",", 1)]

    def displayMessage(self, string):
        self.message.setText(string)


if __name__ == "__main__":
    testGUI = SharkGUI()
    testGUI.win.getMouse()
    testGUI.disableEntry()
    testGUI.win.getMouse()
    testGUI.start_button.deactivate()
    testGUI.move_button.activate()
    testGUI.win.getMouse()
    print(testGUI.getCoordinates())
