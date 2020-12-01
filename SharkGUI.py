# Shark Game GUI Handler (Benjamin Antupit)

from graphics import *

from Button import Button

from PIL import ImageTk
import PIL.Image

from time import sleep

class SharkGUI:

    def __init__(self):
        self.animation_fps = 10
        self.win = GraphWin("Water World", 1200, 800, False)
        self.background = Image(Point(600, 399),
                                "gui/fish-grid-01.png").draw(self.win)
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

        self.coordinates = [[-100, -100] * 4]
        self.images = [PIL.Image.open("gui/shark_low_res.png"),
                       PIL.Image.open("gui/orange_fish_low_res.png"),
                       PIL.Image.open("gui/yellow_fish_low_res.png"),
                       PIL.Image.open("gui/purple_fish_low_res.png")]
        self.sprites = [Image(Point(-100, -100), "gui/shark_low_res.png")
                        .draw(self.win),
                        Image(Point(-100, -100),
                              "gui/orange_fish_low_res.png")
                        .draw(self.win),
                        Image(Point(-100, -100),
                              "gui/yellow_fish_low_res.png")
                        .draw(self.win),
                        Image(Point(-100, -100),
                              "gui/purple_fish_low_res.png")
                        .draw(self.win)]

    def disableEntry(self):
        for entry in self.entries:
            entry.entry.config(state=tk.DISABLED, highlightcolor="#B1E5FC")

    def getCoordinates(self) -> list:
        return [self.entries[0].getText().strip("( )").split(",", 1),
                self.entries[1].getText().strip("( )").split(",", 1),
                self.entries[1].getText().strip("( )").split(",", 1)]

    def displayMessage(self, string):
        self.message.setText(string)

    def getStartPressed(self, point) -> bool:
        return self.start_button.clicked(point)

    def getMovePressed(self, point) -> bool:
        return self.move_button.clicked(point)

    def getQuitPressed(self, point) -> bool:
        return self.quit_button.clicked(point)

    def setMoveButtonLabel(self, label):
        self.move_button.setLabel(label)

    def gridToCanvas(self, x, y):
        return [x * 72 + 475, y * 72 + 75]

    def canvasToGrid(self, x, y):
        return [(x - 440) // 72, (y - 40) // 72]

    def spriteMoveTo(self, index: int, canvas_coordinates: list):
        self.sprites[index].move(
            canvas_coordinates[0] - self.sprites[index].getAnchor().getX(),
            canvas_coordinates[1] - self.sprites[index].getAnchor().getY())

    def spriteMoveOverTime(self, index: int, total_time: float,
                           target_position: list):
        current_position = [self.sprites[index].getAnchor().getX(),
                            self.sprites[index].getAnchor().getY()]
        delta_position = [(target_position[0] - current_position[0])
                    // (total_time * self.animation_fps),
                    (target_position[1] - current_position[1])
                    // (total_time * self.animation_fps)]
        print("target", target_position)
        self._continueSpriteMove(
            index, target_position, delta_position, 0,
            int(total_time * self.animation_fps) - 1,
            1000 // self.animation_fps)

    def _continueSpriteMove(self, index: int, target_position: list,
                            delta_position: list, count: int,
                            total_steps: int, delta_ms: int):
        if count < total_steps:
            self.sprites[index].move(delta_position[0], delta_position[1])
            self.win.after(delta_ms, self._continueSpriteMove, index,
                           target_position, delta_position, count + 1,
                           total_steps, delta_ms)
            print(self.sprites[index].getAnchor())
        else:
            self.spriteMoveTo(index, target_position)

    def spriteRotate(self, index: int, abs_rotation_degrees: float):
        self.sprites[index].img = ImageTk.PhotoImage(
            self.images[index].rotate(abs_rotation_degrees, expand=True))
        self.sprites[index].undraw()
        self.sprites[index].draw(self.win)

    def spriteRotateOverTime(self, index: int, total_time: float,
                             target_degrees: int,
                             current_degrees: int):
        self._continueSpriteRotate(
            index, (target_degrees - current_degrees)
            // int(total_time * self.animation_fps), target_degrees,
            (1000 // self.animation_fps), current_degrees)

    def _continueSpriteRotate(self, index: int, delta_degrees: int,
                              target_degrees: int, deltaMs: int,
                              current_degrees: int):
        if current_degrees < target_degrees:
            self.spriteRotate(index, current_degrees + delta_degrees)
            self.win.after(deltaMs, self._continueSpriteRotate, index,
                           delta_degrees, target_degrees,
                           deltaMs, current_degrees + delta_degrees)
        else:
            self.spriteRotate(index, target_degrees)

    def setCoordinates(self, coordinates):
        for i in range(len(coordinates)):
            if self.coordinates[i] != coordinates[i]:
                self.coordinates[i] = coordinates[i]
                self.spriteMoveTo(i, self.gridToCanvas(
                    coordinates[i][0], coordinates[i][1]))
        self.win.flush()


if __name__ == "__main__":
    testGUI = SharkGUI()
    testGUI.win.getMouse()
    testGUI.disableEntry()
    testGUI.win.getMouse()
    testGUI.start_button.deactivate()
    testGUI.move_button.activate()
    testGUI.win.getMouse()
    testGUI.setCoordinates([[9, 9]])
    testGUI.win.getMouse()
    testGUI.spriteRotateOverTime(0, 1, 270, 0)
    testGUI.win.after(1000, testGUI.spriteMoveOverTime, 0, 1,
                      testGUI.gridToCanvas(4, 4))
    testGUI.win.getMouse()
    print(testGUI.getCoordinates())
