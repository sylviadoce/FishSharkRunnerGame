# Button class: Displays a customizable and toggle-able button
# Benjamin Antupit

from graphics import Rectangle, Point, Text, GraphWin


class Button:

    def __init__(self, window: GraphWin, center: Point,
                 width: int, height: int, label_text: str):
        """Create new button.
        (e.g. Button(win, center_point, width,height, label_text)"""
        self.win = window
        self.rect = Rectangle(
            Point(center.getX() - width / 2, center.getY() - height / 2),
            Point(center.getX() + width / 2, center.getY() + height / 2))
        self.enabled_background = "#1AB0D3"
        self.disabled_background = "#5098B4"
        self.rect.draw(window).setFill(self.enabled_background)
        self.rect.setOutline("#B1E5FC")
        self.rect.setWidth(3)
        self.label = Text(center, label_text)
        self.label.draw(window).setTextColor("#B1E5FC")
        self.label.setSize(36)
        self.active = True

    def __str__(self):
        return "Button ('" + str(self.label) + "')"

    def activate(self):
        """Allow button click to be processed"""
        self.active = True
        self.setFill(self.enabled_background)
        return self

    def deactivate(self):
        """Prevent button click from being processed"""
        self.active = False
        self.setFill(self.disabled_background)
        return self

    def getLabel(self) -> str:
        """Get button label"""
        return self.label.getText()

    def setLabel(self, label_text):
        """Set new button label"""
        self.label.setText(label_text)
        return self

    def clicked(self, pt) -> bool:
        """Return whether click is on button"""
        return (self.active and
                (self.rect.getP1().getX() < pt.getX() <
                 self.rect.getP2().getX()) and
                (self.rect.getP1().getY() < pt.getY() <
                 self.rect.getP2().getY()))

    def waitUntilClicked(self) -> Point:
        """Pauses execution until button is clicked"""
        wait_point = Point(-1, -1)
        while not self.clicked(wait_point):
            wait_point = self.win.getMouse()
        return self.win.checkMouse()

    def getActive(self) -> bool:
        """Get whether button clicks will be processed"""
        return self.active

    def setFill(self, color):
        """Sets fill of button background"""
        self.rect.setFill(color)
        return self

    def setTextSize(self, size):
        """Set size of label text"""
        self.label.setSize(size)
        return self

    def moveText(self, dx, dy):
        """Move label around button"""
        self.label.move(dx, dy)
        return self

    def setTextColor(self, color):
        """Set color of label text"""
        self.label.setTextColor(color)
        return self

    def setTextStyle(self, style):
        """Set label to be bold or italic"""
        self.label.setStyle(style)
        return self

    def setOutline(self, color):
        """Set outline color"""
        self.rect.setOutline(color)
        return self

    def setWidth(self, width):
        """Set outline thickness"""
        self.rect.setWidth(width)
        return self

    def alignLeft(self):
        """Align label text to the left.
           Anchor point will also be on left"""
        self.label.config["justify"] = "left"
        self.label.config["anchor"] = "w"
        self.label.canvas.itemconfig(self.label.id, self.label.config)

    def draw(self):
        """Show button"""
        if not self.label.canvas:
            self.label.draw(self.win)
            self.rect.draw(self.win)
        return self

    def undraw(self):
        """Hide button"""
        self.label.undraw()
        self.rect.undraw()
        return self


# Test case: Run module to run test.
if __name__ == "__main__":
    from graphics import GraphWin

    win = GraphWin("Button test", 200, 100)
    test_button = Button(win, Point(50, 50), 80, 20, "Test Button")
    quit_button = Button(win, Point(150, 50), 50, 20, "Quit")

    while True:
        point = win.getMouse()
        if test_button.clicked(point):
            print(test_button)
        elif quit_button.clicked(point):
            break
