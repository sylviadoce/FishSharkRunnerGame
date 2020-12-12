# Shark Game GUI Handler (Benjamin Antupit)
# Background Water texture found at
# https://2minutetabletop.com/product/ocean-water-textures/
# All other graphics were created by Benjamin & Sylvia

from Button import Button
from graphics import GraphWin, tk, Image, Point, Entry, Text
import math

import PIL.Image
import PIL.ImageTk


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

        self.start_button = Button(Point(215, 430),
                                   316, 48, "Start").setSelectedOutline()
        self.move_button = Button(Point(212, 664),
                                  316, 48, "Move Fish").deactivate()
        self.is_shark_move = False
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
            PIL.Image.open("gui/purple_fish_low_res.png"),
            PIL.Image.open("gui/yellow_fish_low_res.png"),
            PIL.Image.open("gui/shark_low_res.png")]
        self.flee_images = [PIL.Image.open("gui/orange_fish_flee.png"),
                            PIL.Image.open("gui/purple_fish_flee.png"),
                            PIL.Image.open("gui/yellow_fish_flee.png"),
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
                        Image(Point(979, 219), "gui/shark_low_res.png")
                        .draw(self.win)]

    def disableEntry(self):
        for entry in self.entries:
            entry.entry.config(state=tk.DISABLED, highlightcolor="#B1E5FC")
        self.start_button.deactivate().setDeselectedOutline()
        self.move_button.activate().setSelectedOutline()

    def getCoordinates(self) -> list:
        entries = ["", "", ""]
        for i in range(3):
            entries[i] = "".join(list(filter(
                '0123456789,'.__contains__, self.entries[i].getText())
                                      )).split(",", 1)
            try:
                for j in range(len(entries[i])):
                    entries[i][j] = int(entries[i][j].strip(","))
            except ValueError:
                entries[i] = ""
        print(entries)
        return entries

    def displayMessage(self, string, callback_time=0):
        if callback_time:
            self.win.after(int(callback_time * 1000),
                           self.displayMessage, string)
            print("callback scheduled for display message",
                  callback_time, string)
        else:
            self.message.setText(string)

    def getStartPressed(self, point) -> bool:
        if self.start_button.clicked(point):
            self.start_button.deactivate()
            self.move_button.activate()
            return True
        else:
            return False

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
        print("target move", index, self.canvasToGrid(current_position),
              self.canvasToGrid(target_position))
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
        if self.images[index]:
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
        for i in range(len(coordinates)):
            self.spriteMoveTo(i, self.gridToCanvas(coordinates[i]))
            if len(coordinates[i]) > 2:
                self.spriteRotate(i, coordinates[i][2])

    def setSharkCoordinates(self, next_pos: list):
        self.setCoordinate(3, next_pos, 1, 1)

    def setCoordinates(self, next_pos: list,
                       rotation_sec: float = 1, move_sec: int = 1):
        for i in range(len(next_pos)):
            self.setCoordinate(i, next_pos[i], rotation_sec, move_sec)

    def setCoordinate(self, i: int, next_pos: list,
                      rotation_sec: float = 1, move_sec: int = 1):
        current_position = self.canvasToGrid([
            self.sprites[i].getAnchor().getX(),
            self.sprites[i].getAnchor().getY()])
        if len(next_pos) < 3:
            next_pos.append(int(math.degrees(math.atan2(
                current_position[1] - next_pos[1],
                next_pos[0] - current_position[0]))))
        next_pos, current_position = self.checkThroughMovement(
            i, next_pos, current_position)
        if next_pos[2] != self.rotations[i]:
            self.animation_status[i] = False
            self.spriteRotateOverTime(i, rotation_sec, next_pos[2])
            if next_pos[:2] != current_position:
                self.win.after(
                    rotation_sec * 1000, self.spriteMoveOverTime,
                    i, move_sec, self.gridToCanvas(next_pos))
                self.animation_status[i + 4] = False
        elif next_pos[:2] != current_position:
            self.spriteMoveOverTime(
                i, move_sec, self.gridToCanvas(next_pos))
            self.animation_status[i + 4] = False

    def animationComplete(self) -> bool:
        return all(self.animation_status)

    def setFleeMode(self, in_flee_mode: list, delay: float = 0):
        if delay:
            self.win.after(int(delay*1000), self.setFleeMode, in_flee_mode)
            print("callback on setFleeMode", delay, in_flee_mode)
            return
        for i in range(len(in_flee_mode)):
            if self.images[i]:
                if in_flee_mode[i]:
                    self.images[i] = self.flee_images[i]
                else:
                    self.images[i] = self.regular_images[i]
                self.spriteRotate(i, self.rotations[i])

    def setDead(self, is_dead: list):
        self.win.after(1800, self._callbackSetDead, is_dead)

    def _callbackSetDead(self, is_dead: list):
        for i in range(len(is_dead)):
            if is_dead[i]:
                self.sprites[i].undraw()
                self.images[i] = None
                self.spriteMoveTo(i, [-10, -10])

    def checkThroughMovement(self, i: int, next_pos: list,
                             current_position: list):
        moves = [[0, 0], [0, 0], [0, 0]]
        if next_pos[0] == -1:
            # Go through left wall
            moves = [[-7, next_pos[1]],
                     [11, next_pos[1]], [9, next_pos[1]]]
        elif next_pos[0] == 10:
            # Go through right wall
            moves = [[11, next_pos[1]],
                     [-7, next_pos[1]], [0, next_pos[1]]]
        elif next_pos[1] == -1:
            # Go through top wall
            moves = [[next_pos[0], -2],
                     [next_pos[0], 11], [next_pos[0], 9]]
        elif next_pos[1] == 10:
            # Go through bottom wall
            moves = [[next_pos[0], 11],
                     [next_pos[0], -2], [next_pos[0], 0]]
        if moves != [[0, 0], [0, 0], [0, 0]]:
            next_pos[:2] = moves[0]
            self.win.after(2000, self.spriteMoveTo, i,
                           self.gridToCanvas(moves[1]))
            self.win.after(2100, self.spriteMoveOverTime, i, 1,
                           self.gridToCanvas(moves[2]),
                           self.gridToCanvas(moves[1]))
        return next_pos, current_position

    def handleMouse(self):
        point = self.win.getMouse()
        if self.quit_button.clicked(point):
            quit("Quit Button Pressed")
        if self.start_button.clicked(point):
            print("start")
            return 1
        if self.move_button.clicked(point):  # and self.animationComplete()
            if self.is_shark_move:
                self.is_shark_move = False
                self.move_button.setLabel("Move Fish")
                print("move fish")
                return 3
            else:
                self.is_shark_move = True
                self.move_button.setLabel("Move Shark")
                print("move shark")
                return 2
        print("animationComplete", self.animationComplete(),
              self.animation_status)
        return 0

    def disableButtons(self):
        self.move_button.setLabel("Try Again")
        self.quit_button.activate().setDeselectedOutline()
        self.message.setTextColor("#FFFFFF")

    def close(self):
        self.win.close()


if __name__ == "__main__":
    testGUI = SharkGUI()
    testGUI.win.getMouse()
    print(testGUI.getCoordinates())
    testGUI.jumpToCoordinates([[1, 1], [4, 9], [7, 4]])
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
