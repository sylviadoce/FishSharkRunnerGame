# Shark Game GUI Handler (Benjamin Antupit)

from graphics import GraphWin, tk, Image, Point, Entry, Text

from Button import Button

import PIL.Image
import PIL.ImageTk


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

        self.rotations = [-90, 0, 0, 0]
        self.images = [PIL.Image.open("gui/shark_low_res.png"),
                       PIL.Image.open("gui/orange_fish_low_res.png"),
                       PIL.Image.open("gui/yellow_fish_low_res.png"),
                       PIL.Image.open("gui/purple_fish_low_res.png")]
        self.fleeImages = [PIL.Image.open("gui/shark_low_res.png"),
                           PIL.Image.open("gui/orange_fish_flee.png"),
                           PIL.Image.open("gui/yellow_fish_flee.png"),
                           PIL.Image.open("gui/purple_fish_flee.png")]
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
        if self.start_button.clicked(point):
            self.start_button.deactivate()
            self.move_button.activate()
            return True
        else:
            return False

    def getMovePressed(self, point) -> bool:
        return self.move_button.clicked(point)

    def getQuitPressed(self, point):
        if self.quit_button.clicked(point):
            quit("Quit Button Pressed")

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

    def spriteRotate(self, index: int, abs_rotation_degrees: int):
        abs_rotation_degrees %= 360
        self.rotations[index] = abs_rotation_degrees
        direction = 1
        if 180 <= abs_rotation_degrees < 360:
            direction = -1
        self.sprites[index].img = PIL.ImageTk.PhotoImage(
            self.images[index].rotate(
                direction * abs_rotation_degrees, expand=True))
        self.sprites[index].undraw()
        self.sprites[index].draw(self.win)

    def spriteRotateOverTime(self, index: int, total_time: float,
                             target_degrees: int):
        target_degrees %= 360
        delta_sign = 1
        if target_degrees - self.rotations[index] <= 180:
            delta_sign = -1
        # TODO: account for alt. rotation direction in delta_degrees
        #  (makes too small jumps now)
        self._continueSpriteRotate(
            index, delta_sign * (target_degrees - self.rotations[index])
            // int(total_time * self.animation_fps),
            target_degrees, 1000 // self.animation_fps)

    def _continueSpriteRotate(self, index: int, delta_degrees: int,
                              target_degrees: int, delta_ms: int):
        if not((target_degrees - abs(delta_degrees)) <
               self.rotations[index] <
               (target_degrees + abs(delta_degrees))):
            self.spriteRotate(index, self.rotations[index] + delta_degrees)
            self.win.after(delta_ms, self._continueSpriteRotate, index,
                           delta_degrees, target_degrees, delta_ms)
        else:
            self.spriteRotate(index, target_degrees)

    def pointToList(self, point: Point):
        return [point.getX(), point.getY()]

    def setCoordinates(self, coordinates: list,
                       rotation_seconds: float, move_seconds: int):
        rotate = 0
        for i in range(len(coordinates)):
            if (coordinates[i][:2] !=
                    self.pointToList(self.sprites[i].getAnchor())):
                if coordinates[i][2] != self.rotations[i]:
                    rotate += 1
                    self.spriteRotateOverTime(i, rotation_seconds,
                                              coordinates[i][2])
                    self.win.after(
                        rotation_seconds * 1000, self.spriteMoveOverTime,
                        i, move_seconds, self.gridToCanvas(
                            coordinates[i][0], coordinates[i][1]))
                else:
                    self.spriteMoveOverTime(
                        i, move_seconds, self.gridToCanvas(
                            coordinates[i][0], coordinates[i][1]))
        self.win.flush()
        if rotate:
            self.win.mainloop(rotation_seconds)
        self.win.mainloop(move_seconds)


if __name__ == "__main__":
    testGUI = SharkGUI()
    testGUI.win.getMouse()
    testGUI.setCoordinates([[0, 0, 0]], 1, 1)
    testGUI.win.getMouse()
    testGUI.setCoordinates([[0, 9, 180]], 1, 1)
    testGUI.win.getMouse()
    testGUI.setCoordinates([[9, 9, 90]], 1, 1)
    testGUI.win.getMouse()
    testGUI.setCoordinates([[0, 1, -45]], 1, 1)
    testGUI.win.getMouse()
    testGUI.disableEntry()
    testGUI.start_button.deactivate()
    testGUI.move_button.activate()
    print(testGUI.getCoordinates())
