# Shark Game GUI Handler (Benjamin Antupit)

from Button import Button
from graphics import GraphWin, tk, Image, Point, Entry, Text
import PIL.Image
import PIL.ImageTk
import math


class SharkGUI:
    def __init__(self):
        self.animation_fps = 10
        self.animation_status = [True] * 8
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

        self.start_button = Button(Point(215, 430), 316, 48, "Start")
        self.move_button = Button(Point(212, 664),
                                  316, 48, "Move").deactivate()
        self.quit_button = Button(Point(212, 736), 320, 48, "Quit")
        self.quit_button.setFill("").setOutline("")
        for e in (self.start_button.getElements() +
                  self.move_button.getElements() +
                  self.quit_button.getElements()):
            e.draw(self.win)

        self.message = Text(Point(212, 568), "Enter Fish Coordinates \n"
                                             "and select Start to begin")
        self.message.draw(self.win).setTextColor("#B1E5FC")
        self.message.setSize(24)

        self.rotations = [361] * 4
        self.regular_images = [
            PIL.Image.open("gui/orange_fish_low_res.png"),
            PIL.Image.open("gui/yellow_fish_low_res.png"),
            PIL.Image.open("gui/purple_fish_low_res.png"),
            PIL.Image.open("gui/shark_low_res.png")]
        self.flee_images = [PIL.Image.open("gui/orange_fish_flee.png"),
                            PIL.Image.open("gui/yellow_fish_flee.png"),
                            PIL.Image.open("gui/purple_fish_flee.png"),
                            PIL.Image.open("gui/shark_low_res.png")]
        self.images = self.regular_images[:]
        self.sprites = [Image(Point(1300, 400),
                              "gui/orange_fish_low_res.png")
                        .draw(self.win),
                        Image(Point(1300, 400),
                              "gui/yellow_fish_low_res.png")
                        .draw(self.win),
                        Image(Point(1300, 400),
                              "gui/purple_fish_low_res.png")
                        .draw(self.win),
                        Image(Point(1300, 400), "gui/shark_low_res.png")
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

    def getQuitPressed(self, point) -> bool:
        if self.quit_button.clicked(point):
            quit("Quit Button Pressed")
        return False

    def setMoveButtonLabel(self, label):
        self.move_button.setLabel(label)

    def gridToCanvas(self, xy: list):
        return [xy[0] * 72 + 475, xy[1] * 72 + 75]

    def canvasToGrid(self, xy: list):
        return [(xy[0] - 440) // 72, (xy[1] - 40) // 72]

    def spriteMoveTo(self, index: int, canvas_coordinates: list):
        self.sprites[index].move(
            canvas_coordinates[0] - self.sprites[index].getAnchor().getX(),
            canvas_coordinates[1] - self.sprites[index].getAnchor().getY())

    def spriteMoveOverTime(self, index: int, total_time: float,
                           target_position: list, current_position=False):
        self.animation_status[index + 4] = False
        if not current_position:
            current_position = [self.sprites[index].getAnchor().getX(),
                                self.sprites[index].getAnchor().getY()]
        delta_position = [(target_position[0] - current_position[0])
                          // (total_time * self.animation_fps),
                          (target_position[1] - current_position[1])
                          // (total_time * self.animation_fps)]
        # print("target move", index, self.canvasToGrid(current_position),
        #       self.canvasToGrid(target_position))
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
        else:
            self.spriteMoveTo(index, target_position)
            self.animation_status[index + 4] = True

    def spriteRotate(self, index: int, abs_rotation_degrees: int):
        abs_rotation_degrees %= 360
        self.rotations[index] = abs_rotation_degrees
        if 90 <= abs_rotation_degrees <= 270:
            self.sprites[index].img = PIL.ImageTk.PhotoImage(
                self.images[index].rotate(
                    -abs_rotation_degrees, expand=True).
                transpose(PIL.Image.FLIP_TOP_BOTTOM))
        else:
            self.sprites[index].img = PIL.ImageTk.PhotoImage(
                self.images[index].rotate(
                    abs_rotation_degrees, expand=True))

        self.sprites[index].undraw()
        self.sprites[index].draw(self.win)

    def spriteRotateOverTime(self, index: int, total_time: float,
                             target_degrees: int):
        self.animation_status[index] = False
        target_degrees %= 360
        total_delta_degrees = target_degrees - self.rotations[index]
        if abs(target_degrees - self.rotations[index]) >= 180:
            total_delta_degrees = self.rotations[index] - target_degrees
        self._continueSpriteRotate(
            index, total_delta_degrees
            // int(total_time * self.animation_fps),
            target_degrees, 1000 // self.animation_fps)

    def _continueSpriteRotate(self, index: int, delta_degrees: int,
                              target_degrees: int, delta_ms: int):
        if not ((target_degrees - abs(delta_degrees)) <
                self.rotations[index] <
                (target_degrees + abs(delta_degrees))):
            self.spriteRotate(index, self.rotations[index] + delta_degrees)
            self.win.after(delta_ms, self._continueSpriteRotate, index,
                           delta_degrees, target_degrees, delta_ms)
        else:
            self.spriteRotate(index, target_degrees)
            self.animation_status[index] = True

    def jumpToCoordinates(self, coordinates: list):
        for i in range(len(self.sprites)):
            self.spriteMoveTo(i, self.gridToCanvas(coordinates[i]))
            if len(coordinates[i]) > 2:
                self.spriteRotate(i, coordinates[i][2])

    def setCoordinates(self, next_pos: list,
                       rotation_seconds: float = 1, move_seconds: int = 1):
        rotate = 0
        for i in range(len(next_pos)):
            current_position = self.canvasToGrid([
                self.sprites[i].getAnchor().getX(),
                self.sprites[i].getAnchor().getY()])
            if len(next_pos[i]) < 3:
                next_pos[i].append(int(math.degrees(math.atan2(
                    current_position[1] - next_pos[i][1],
                    next_pos[i][0] - current_position[0]))))
            next_pos, current_position = self.checkThroughMovement(
                i, next_pos, current_position)
            if next_pos[i][2] != self.rotations[i]:
                rotate += 1
                self.animation_status[i] = False
                self.spriteRotateOverTime(i, rotation_seconds,
                                          next_pos[i][2])

                if next_pos[i][:2] != current_position:
                    self.win.after(
                        rotation_seconds * 1000, self.spriteMoveOverTime,
                        i, move_seconds, self.gridToCanvas(next_pos[i]))
                    self.animation_status[i + 4] = False
            elif next_pos[i][:2] != current_position:
                self.spriteMoveOverTime(
                    i, move_seconds, self.gridToCanvas(next_pos[i]))
                self.animation_status[i + 4] = False
        if rotate:
            self.win.mainloop(rotation_seconds)
        self.win.mainloop(move_seconds)

    def animationComplete(self) -> bool:
        return all(self.animation_status)

    def setFleeMode(self, in_flee_mode: list):
        for i in range(len(in_flee_mode)):
            if in_flee_mode[i]:
                self.images[i] = self.flee_images[i]
            else:
                self.images[i] = self.regular_images[i]
            self.spriteRotate(i, self.rotations[i])

    def checkThroughMovement(self, i: int, next_pos: list,
                             current_position: list):
        moves = [[0, 0], [0, 0], [0, 0]]
        if next_pos[i][0] == -1:
            # Go through left wall
            moves = [[-7, next_pos[i][1]],
                     [11, next_pos[i][1]], [9, next_pos[i][1]]]
        elif next_pos[i][0] == 10:
            # Go through right wall
            moves = [[11, next_pos[i][1]],
                     [-7, next_pos[i][1]], [0, next_pos[i][1]]]
        elif next_pos[i][1] == -1:
            # Go through top wall
            moves = [[next_pos[i][0], -2],
                     [next_pos[i][0], 11], [next_pos[i][0], 9]]
        elif next_pos[i][1] == 10:
            # Go through bottom wall
            moves = [[next_pos[i][0], 11],
                     [next_pos[i][0], -2], [next_pos[i][0], 0]]
        if moves != [[0, 0], [0, 0], [0, 0]]:
            next_pos[i][:2] = moves[0]
            self.win.after(2000, self.spriteMoveTo, i,
                           self.gridToCanvas(moves[1]))
            self.win.after(2100, self.spriteMoveOverTime, i, 1,
                           self.gridToCanvas(moves[2]),
                           self.gridToCanvas(moves[1]))
        return next_pos, current_position


if __name__ == "__main__":
    testGUI = SharkGUI()
    testGUI.win.getMouse()
    testGUI.jumpToCoordinates([[0, 0, 0], [0, 1, 180],
                               [0, 2, 180], [7, 2, 0]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[7, 2], [2, 7], [1, 1], [5, 4]])
    testGUI.win.getMouse()
    testGUI.setFleeMode([True, False, True])
    testGUI.setCoordinates([[7, -1], [2, 8], [1, 2], [5, 5]])
    testGUI.win.getMouse()
    testGUI.setFleeMode([True, False, False])
    testGUI.setCoordinates([[0, 6]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[-1, 6]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[9, 9]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[10, 9]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[9, 3]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[10, 3]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[0, 7]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[-1, 7]])
    testGUI.win.getMouse()
    testGUI.setCoordinates([[9, -1]])

    testGUI.win.getMouse()
    testGUI.disableEntry()
    testGUI.start_button.deactivate()
    testGUI.move_button.activate()
    print(testGUI.getCoordinates())
