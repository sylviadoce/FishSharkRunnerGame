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
        """Creates new SharkGUI window
        including all buttons, entries and sprites."""
        self.animation_fps = 10
        self.animation_status = [True] * 8
        self.win = GraphWin("Water World", 1200, 800, False)
        self.background = Image(Point(600, 399),
                                "gui/fish-grid-01.png").draw(self.win)
        self.entries = [Entry(Point(308, 190), 8),
                        Entry(Point(308, 270), 8),
                        Entry(Point(308, 350), 8)]
        # Draw entries in reverse order so user cursor starts in top entry
        for entry in reversed(self.entries):
            entry.draw(self.win).setSize(26)
            entry.setFill("#80A5AF")
            entry.setTextColor("#FFFFFF")
            # Configure custom colors and borders
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
        self.quit_button = Button(Point(212, 736), 320, 48, "Quit")
        self.quit_button.setFill("").setOutline("")
        # Draw all elements to avoid passing self.win to button class
        for e in (self.start_button.getElements() +
                  self.move_button.getElements() +
                  self.quit_button.getElements()):
            e.draw(self.win)

        self.message = Text(Point(212, 568), "Enter Fish Coordinates \n"
                                             "and select Start to begin")
        self.message.draw(self.win).setTextColor("#B1E5FC")
        self.message.setSize(24)

        self.is_shark_move = False
        self.rotations = [361] * 4
        # Load all images as PIL images to allow for rotation
        # Convert to tkinter PhotoImage after rotation
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
        """Signals start of game. Disables entry boxes and enables move."""
        for entry in self.entries:
            entry.entry.config(state=tk.DISABLED, highlightcolor="#B1E5FC")
        self.start_button.deactivate().setDeselectedOutline()
        self.move_button.activate().setSelectedOutline()

    def getCoordinates(self) -> list:
        """Parse and retrieve coordinates from entry boxes"""
        entries = ["", "", ""]
        for i in range(3):
            # Filter entry responses for numbers, separate by comma
            entries[i] = "".join(list(filter(
                '0123456789,'.__contains__, self.entries[i].getText())
                                      )).split(",", 1)
            try: # Attempt to convert to int, otherwise return empty list
                for j in range(len(entries[i])):
                    entries[i][j] = int(entries[i][j].strip(","))
            except ValueError:
                entries[i] = ""
        return entries

    def displayMessage(self, string, callback_time=0):
        """Display message in sidebar. Use optional callback_time to
        display message in x seconds."""
        if callback_time:
            self.win.after(int(callback_time * 1000),
                           self.displayMessage, string)
        else:
            self.message.setText(string)

    def gridToCanvas(self, xy: list):
        """Convert grid coordinates (0,9) to window/canvas coordinates."""
        return [xy[0] * 72 + 475, xy[1] * 72 + 75]

    def canvasToGrid(self, xy: list):
        """Convert window/canvas coordinates to grid coordinates (0,9)."""
        return [(xy[0] - 440) // 72, (xy[1] - 40) // 72]

    def spriteMoveTo(self, index: int, canvas_coordinates: list):
        """Move specified sprite to canvas_coordinates immediately"""
        self.sprites[index].move(
            canvas_coordinates[0] - self.sprites[index].getAnchor().getX(),
            canvas_coordinates[1] - self.sprites[index].getAnchor().getY())

    def spriteMoveOverTime(self, index: int, total_time: float,
                           target_position: list, current_position=False):
        """Move specified sprite to canvas_coordinates incrementally over
        the following total_time seconds. \n
        Optionally, jump to current_position before beginning animation"""
        self.animation_status[index + 4] = False
        if not current_position:
            current_position = [self.sprites[index].getAnchor().getX(),
                                self.sprites[index].getAnchor().getY()]
        delta_position = [(target_position[0] - current_position[0])
                          // (total_time * self.animation_fps),
                          (target_position[1] - current_position[1])
                          // (total_time * self.animation_fps)]
        # Schedule initial callback to _continueSpriteMove
        self._continueSpriteMove(
            index, target_position, delta_position, 0,
            int(total_time * self.animation_fps) - 1,
            1000 // self.animation_fps)

    def _continueSpriteMove(self, index: int, target_position: list,
                            delta_position: list, count: int,
                            total_steps: int, delta_ms: int):
        """Scheduled callback from spriteMoveOverTime."""
        if count < total_steps:
            self.sprites[index].move(delta_position[0], delta_position[1])
            # Reschedule callback
            self.win.after(delta_ms, self._continueSpriteMove, index,
                           target_position, delta_position, count + 1,
                           total_steps, delta_ms)
        else:
            # At end of animation, jump to end position.
            # Rounding errors often occur which means that the animation
            #    does not reach the target position. End jump fixes this.
            self.spriteMoveTo(index, target_position)
            self.animation_status[index + 4] = True

    def spriteRotate(self, index: int, abs_rotation_degrees: int):
        """Rotate specified sprite to abs_rotation_degrees immediately"""
        abs_rotation_degrees %= 360
        self.rotations[index] = abs_rotation_degrees
        if self.images[index]:  # Check if fish is not dead (image exists)
            # Flip image if between 90 and 270 to keep fins on top
            if 90 <= abs_rotation_degrees <= 270:
                self.sprites[index].img = PIL.ImageTk.PhotoImage(
                    self.images[index].rotate(
                        -abs_rotation_degrees, expand=True).
                    transpose(PIL.Image.FLIP_TOP_BOTTOM))
            else:
                self.sprites[index].img = PIL.ImageTk.PhotoImage(
                    self.images[index].rotate(
                        abs_rotation_degrees, expand=True))
        # Undraw and draw sprite to update image on canvas
        self.sprites[index].undraw()
        self.sprites[index].draw(self.win)

    def spriteRotateOverTime(self, index: int, total_time: float,
                             target_degrees: int):
        """Rotate specified sprite to target_degrees incrementally over
                the following total_time seconds."""
        self.animation_status[index] = False
        target_degrees %= 360
        total_delta_degrees = target_degrees - self.rotations[index]
        # Choose rotation direction for shortest path
        if abs(target_degrees - self.rotations[index]) >= 180:
            total_delta_degrees = self.rotations[index] - target_degrees
        # Schedule initial callback for _continueSpriteRotate
        self._continueSpriteRotate(
            index, total_delta_degrees
            // int(total_time * self.animation_fps),
            target_degrees, 1000 // self.animation_fps)

    def _continueSpriteRotate(self, index: int, delta_degrees: int,
                              target_degrees: int, delta_ms: int):
        """Scheduled callback from spriteRotateOverTime."""
        if not ((target_degrees - abs(delta_degrees)) <
                self.rotations[index] <
                (target_degrees + abs(delta_degrees))):
            self.spriteRotate(index, self.rotations[index] + delta_degrees)
            self.win.after(delta_ms, self._continueSpriteRotate, index,
                           delta_degrees, target_degrees, delta_ms)
        else:
            # At end of animation, jump to end rotation.
            # Rounding errors often occur which means that the animation
            #    does not reach the target rotation. End jump fixes this.
            self.spriteRotate(index, target_degrees)
            self.animation_status[index] = True

    def jumpToCoordinates(self, coordinates: list):
        """Move and rotate all sprites to specified
        coordinates and rotations immediately"""
        for i in range(len(coordinates)):
            self.spriteMoveTo(i, self.gridToCanvas(coordinates[i]))
            if len(coordinates[i]) > 2:
                self.spriteRotate(i, coordinates[i][2])

    def setSharkCoordinates(self, next_pos: list):
        """Set translation and rotation of shark sprite"""
        self.setCoordinate(3, next_pos, 1, 1)

    def setCoordinates(self, next_pos: list,
                       rotation_sec: float = 1, move_sec: int = 1):
        """Set translation and rotation of all sprites"""
        for i in range(len(next_pos)):
            self.setCoordinate(i, next_pos[i], rotation_sec, move_sec)

    def setCoordinate(self, i: int, next_pos: list,
                      rotation_sec: float = 1, move_sec: int = 1):
        """Set translation and rotation of given sprite with index i"""
        current_position = self.canvasToGrid([
            self.sprites[i].getAnchor().getX(),
            self.sprites[i].getAnchor().getY()])
        if len(next_pos) < 3:  # Calculate rotation if none is provided
            next_pos.append(int(math.degrees(math.atan2(
                current_position[1] - next_pos[1],
                next_pos[0] - current_position[0]))))
            # Check if fish goess through wall and calculates coordinates
        next_pos, current_position = self.checkThroughMovement(
            i, next_pos, current_position)
        if next_pos[2] != self.rotations[i]:  # Check if rotation changed
            self.animation_status[i] = False
            self.spriteRotateOverTime(i, rotation_sec, next_pos[2])
            if next_pos[:2] != current_position:  # Did translation change?
                # Schedule translation after rotation
                self.win.after(
                    rotation_sec * 1000, self.spriteMoveOverTime,
                    i, move_sec, self.gridToCanvas(next_pos))
                self.animation_status[i + 4] = False
        elif next_pos[:2] != current_position:  # Did translation change?
            self.spriteMoveOverTime(
                i, move_sec, self.gridToCanvas(next_pos))
            self.animation_status[i + 4] = False

    def animationComplete(self) -> bool:
        """Returns true if all sprites have finished their animations"""
        return all(self.animation_status)

    def setFleeMode(self, in_flee_mode: list, delay: float = 0):
        """Set flee mode images of all fish. Optional delay in seconds."""
        if delay:  # Schedule callback and return
            self.win.after(int(delay*1000), self.setFleeMode, in_flee_mode)
            print("callback on setFleeMode", delay, in_flee_mode)
            return
        for i in range(len(in_flee_mode)):
            if self.images[i]:
                if in_flee_mode[i]:
                    self.images[i] = self.flee_images[i]
                else:
                    self.images[i] = self.regular_images[i]
                # Rotate new images to last set rotation and update canvas
                self.spriteRotate(i, self.rotations[i])

    def setDead(self, is_dead: list, delay=1.8):
        """Remove specified sprites from the canvas.
        Optional delay in seconds"""
        if delay:
            self.win.after(int(delay * 1000), self.setDead, is_dead)
            return
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
        self.quit_button.activate().setSelectedOutline()
        self.message.setTextColor("#FFFFFF")

    def close(self):
        self.win.close()


if __name__ == "__main__":
    testGUI = SharkGUI()
    testGUI.win.getMouse()
    print(testGUI.getCoordinates())
    testGUI.win.getMouse()
    testGUI.disableEntry()
    print(testGUI.getCoordinates())
