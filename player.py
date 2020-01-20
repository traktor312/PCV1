from abc import ABC, abstractmethod

# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"red",
      "outline":"black",
      "width":"5",}

import math

class Player():
    def __init__(self, x, y, r):
        self.__x = float(x)
        self.__y = float(y)
        self.r = float(r)
        self.outline_color = DEFAULT_CONFIG["outline"]
        self.fill_color = DEFAULT_CONFIG["fill"]
        self.outline_width = DEFAULT_CONFIG["width"]
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.speed = 3

    def __repr__(self):
        return "Player(x: {}, y: {}, r: {}, fill_color: {}, width:{} )".format(self.x, self.y, self.r, self.fill_color, width=self.r)

    def draw(self, canvas):   
        return canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.fill_color)

    def move(self):
        if((self.up | self.down) & (self.left | self.right)):
            if(self.up == True):
                self.y -= self.speed / math.sqrt(2)
            if(self.down == True):
                self.y += self.speed / math.sqrt(2)
            if(self.right == True):
                self.x += self.speed / math.sqrt(2)
            if(self.left == True):
                self.x -= self.speed / math.sqrt(2)
        else:
            if(self.up == True):
                self.y -= self.speed
            if(self.down == True):
                self.y += self.speed
            if(self.right == True):
                self.x += self.speed
            if(self.left == True):
                self.x -= self.speed

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, value):
        if value < 0:
            self.__x = 0
        else:
            self.__x = value
            
    @y.setter
    def y(self, value):
        if value < 0:
            self.__y = 0
        else:
            self.__y = value



class Player2():
    def __init__(self, i, x, y, w, h, col, angle, up, down, left, right, shoot):
        self.live = True
        self.balls = 0
        self.id = i
        self.x = float(x)
        self.y = float(y)
        self.width = w
        self.height = h
        self.key_up = up
        self.key_down = down
        self.key_left = left
        self.key_right = right
        self.key_shoot = shoot
        self.outline_color = "black"
        self.fill_color = col
        self.outline_width = "1"
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.speed = 3
        self.rotation_speed = 4
        self.a = 0
        self.b = 0
        self.angle = angle
        self.last_angle = angle
        self.angle_rad = float(0)
        self.points = [
            {
                "x": 0,
                "y": 0
            },{
                "x": 0,
                "y": 0
            },{
                "x": 0,
                "y": 0
            },{
                "x": 0,
                "y": 0
            }
        ]
        self.gun_points = [
            {
                "x": 0,
                "y": 0
            },{
                "x": 0,
                "y": 0
            },{
                "x": 0,
                "y": 0
            },{
                "x": 0,
                "y": 0
            }
        ]
        self.shoot_point = {
            "x": 0,
            "y": 0
        }
        self.lines = []
        a = self.width / 2
        b = self.height / 2
        self.pom_radius = math.sqrt(a * a + b * b)
        self.pom_angle = math.acos(a / self.pom_radius)
        self.fire = False
        self.score = 0
        self.calc_all()

    def draw(self, canvas):   
        canvas.create_polygon(
        self.points[0]["x"] , self.points[0]["y"] , 
        self.points[1]["x"] , self.points[1]["y"] , 
        self.points[2]["x"] , self.points[2]["y"] ,   
        self.points[3]["x"] , self.points[3]["y"] ,  
        fill=self.fill_color, outline=self.outline_color, width=self.outline_width)
        pomx = self.x + self.pom_radius * math.cos(self.angle_rad) / 2
        pomy = self.y + self.pom_radius * math.sin(self.angle_rad) / 2
        canvas.create_polygon(
        self.gun_points[0]["x"] , self.gun_points[0]["y"] , 
        self.gun_points[1]["x"] , self.gun_points[1]["y"] , 
        self.gun_points[2]["x"] , self.gun_points[2]["y"] ,   
        self.gun_points[3]["x"] , self.gun_points[3]["y"] , 
        fill=self.fill_color, outline=self.outline_color, width=self.outline_width)
        canvas.create_oval(self.x - (self.height / 3), self.y - (self.height / 3), self.x + (self.height / 3), self.y + (self.height / 3), 
        fill=self.fill_color, outline=self.outline_color, width=self.outline_width)

    def calc_angle_rad(self):
        return self.angle / 180 * math.pi

    def calc_points(self):
        pom_angle1 = self.angle_rad + self.pom_angle
        pom_angle2 = self.angle_rad - self.pom_angle
        self.shoot_point["x"] = self.x + self.pom_radius * math.cos(self.angle_rad)
        self.shoot_point["y"] = self.y + self.pom_radius * math.sin(self.angle_rad)
        self.points[0]["x"] = self.x - self.pom_radius * math.cos(pom_angle2)
        self.points[0]["y"] = self.y - self.pom_radius * math.sin(pom_angle2)
        self.points[1]["x"] = self.x - self.pom_radius * math.cos(pom_angle1)
        self.points[1]["y"] = self.y - self.pom_radius * math.sin(pom_angle1)
        self.points[2]["x"] = self.x + self.pom_radius * math.cos(pom_angle2)
        self.points[2]["y"] = self.y + self.pom_radius * math.sin(pom_angle2)
        self.points[3]["x"] = self.x + self.pom_radius * math.cos(pom_angle1)
        self.points[3]["y"] = self.y + self.pom_radius * math.sin(pom_angle1)
        pomx = self.x + self.pom_radius * math.cos(self.angle_rad) / 2
        pomy = self.y + self.pom_radius * math.sin(self.angle_rad) / 2
        pom_angle1 = self.angle_rad + self.pom_angle / 2
        pom_angle2 = self.angle_rad - self.pom_angle / 2
        self.gun_points[0]["x"] = pomx - self.pom_radius * math.cos(pom_angle2) / 2
        self.gun_points[0]["y"] = pomy - self.pom_radius * math.sin(pom_angle2) / 2
        self.gun_points[1]["x"] = pomx - self.pom_radius * math.cos(pom_angle1) / 2
        self.gun_points[1]["y"] = pomy - self.pom_radius * math.sin(pom_angle1) / 2
        self.gun_points[2]["x"] = pomx + self.pom_radius * math.cos(pom_angle2) / 2
        self.gun_points[2]["y"] = pomy + self.pom_radius * math.sin(pom_angle2) / 2
        self.gun_points[3]["x"] = pomx + self.pom_radius * math.cos(pom_angle1) / 2
        self.gun_points[3]["y"] = pomy + self.pom_radius * math.sin(pom_angle1) / 2

    def calc_lines(self):
        self.lines = []
        self.lines.append(self.calc_line(self.points[0]["x"], self.points[0]["y"], self.points[1]["x"], self.points[1]["y"]))
        self.lines.append(self.calc_line(self.points[1]["x"], self.points[1]["y"], self.points[2]["x"], self.points[2]["y"]))
        self.lines.append(self.calc_line(self.points[2]["x"], self.points[2]["y"], self.points[3]["x"], self.points[3]["y"]))
        self.lines.append(self.calc_line(self.points[3]["x"], self.points[3]["y"], self.points[0]["x"], self.points[0]["y"]))
        
    def calc_line(self, x0, y0, x1, y1):
        a = y0 - y1
        b = x1 - x0
        c = (a * x0 + b * y0)
        return {"a": a, "b": b, "c": c}

    def calc_move(self):
        self.a = self.speed * math.cos(self.angle_rad)
        self.b = self.speed * math.sin(self.angle_rad)
        self.last_angle = self.angle

    def calc_all(self):
        self.angle_rad = self.calc_angle_rad()
        self.calc_points()
        self.calc_lines()
        self.calc_move()

    def move(self):
        if(self.right and not self.left):
            self.angle += self.rotation_speed
            if(self.angle > 360):
                self.angle -= 360
        elif(self.left):
            self.angle -= self.rotation_speed
            if(self.angle < 0):
                self.angle += 360
        if(self.angle != self.last_angle):
            self.calc_all()
        if(self.up):
            self.x += self.a
            self.y += self.b
            self.calc_points()
            self.calc_lines()
        elif(self.down):
            self.x -= self.a / 2
            self.y -= self.b / 2
            self.calc_points()
            self.calc_lines()

    def crash_with_point(self, x, y):
        for l in self.lines:
            if((l["a"] * x + l["b"] * y < l["c"] )and (l["a"] * self.x + l["b"] * self.y > l["c"]) or 
               (l["a"] * x + l["b"] * y > l["c"]) and (l["a"] * self.x + l["b"] * self.y < l["c"])):
                return False
        return True

    def key_press(self, key, key_code):
        if(key != ""):
            if(key == self.key_left and not self.right):
                self.left = True
            if(key == self.key_down and not self.up):
                self.down = True
            if(key == self.key_right and not self.left):
                self.right = True
            if(key == self.key_up and not self.down):
                self.up = True
        else:
            if(key_code == self.key_left and not self.right):
                self.left = True
            if(key_code == self.key_down and not self.up):
                self.down = True
            if(key_code == self.key_right and not self.left):
                self.right = True
            if(key_code == self.key_up and not self.down):
                self.up = True

    def key_release(self, key, key_code):
        if(key != ""):
            if(key == self.key_left):
                self.left = False
            if(key == self.key_down):
                self.down = False
            if(key == self.key_right):
                self.right = False
            if(key == self.key_up):
                self.up = False
        else:
            if(key_code == self.key_left):
                self.left = False
            if(key_code == self.key_down):
                self.down = False
            if(key_code == self.key_right):
                self.right = False
            if(key_code == self.key_up):
                self.up = False

    def key(self, key, key_code, game):
        if(self.balls < 10 and (key == self.key_shoot or key_code == self.key_shoot)):
            for w in game.walls:
                if(w.inside(self.shoot_point["x"], self.shoot_point["y"])):
                    self.live = False
                    game.remove_player()
                    break
            else:
                game.add_ball(self.shoot_point["x"], self.shoot_point["y"], self.angle, self)
                self.balls += 1

        