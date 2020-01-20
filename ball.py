from abc import ABC, abstractmethod
import math

# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"black",
      "outline":"black",
      "width":"1",}



class Ball():
    def __init__(self, i, x, y, r, angle, owner):
        self.owner = owner
        self.id = i
        self.x = x
        self.y = y
        self.a = 0
        self.b = 0
        self.r = r
        self.angle = angle
        self.last_angle = angle
        self.outline_color = DEFAULT_CONFIG["outline"]
        self.fill_color = DEFAULT_CONFIG["fill"]
        self.outline_width = DEFAULT_CONFIG["width"]
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.speed = 5
        self.live_time = 500
        self.calc_move()

    def __repr__(self):
        return "Player(x: {}, y: {}, r: {}, fill_color: {}, width:{} )".format(self.x, self.y, self.r, self.fill_color, width=self.r)

    def draw(self, canvas):   
        return canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.fill_color)

    def calc_move(self):
        angle_rad = self.angle / 180 * math.pi
        self.a = math.cos(angle_rad) * self.speed
        self.b = math.sin(angle_rad) * self.speed
        self.last_angle = self.angle

    def move(self, parrent):
        if(self.angle != self.last_angle):
            self.calc_move()
        self.x += self.a
        self.y += self.b
        self.live_time -= 1
        if(self.live_time <= 0):
            parrent.remove_ball(self.id)
            self.owner.balls -= 1

    def crash_with_player(self, obj, game):
        if(obj.crash_with_point(self.x, self.y)):
            obj.live = False
            self.owner.balls -= 1
            game.remove_player()
            game.remove_ball(self.id)
