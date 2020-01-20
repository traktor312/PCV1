from abc import ABC, abstractmethod
import math

DEFAULT_CONFIG = {"fill":"blue",
      "outline":"black",
      "width":"5",}

class Shape(ABC):
    def __init__(self, x, y, w, h):
        self.__x = x
        self.__y = y
        self.width = w
        self.height = h
        self.outline_color = DEFAULT_CONFIG["outline"]
        self.outline_width = DEFAULT_CONFIG["width"]
        self.fill_color = DEFAULT_CONFIG["fill"]

    def __repr__(self):
        return "Shape(x: {}, y: {}, width: {}, height: {}, fill_color: {} )".format(self.x, self.y, self.width, self.height, self.fill_color)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, value):
        self.__x = value
            
    @y.setter
    def y(self, value):
        self.__y = value

    @abstractmethod
    def draw(self, canvas):
        pass


class Rectangle(Shape):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.fill_color = "grey"

    def __repr__(self):
        return "Rectangle(x: {}, y: {}, width: {}, height: {}, fill_color: {}, width:{} )".format(self.x, self.y, self.width, self.height, self.fill_color, width=self.outline_width)

    def draw(self, canvas):
       return canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.fill_color) 

    def inside(self, x, y):
        if(x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height):
            return True
        return False

    def crash_with_rectangle(self, obj):
        if((self.inside(obj.points[0]["x"], obj.points[0]["y"]) or self.inside(obj.points[1]["x"], obj.points[1]["y"]) or self.inside(obj.points[2]["x"], obj.points[2]["y"]) 
        or self.inside(obj.points[3]["x"], obj.points[3]["y"]) or obj.crash_with_point(self.x, self.y) or obj.crash_with_point(self.x + self.width, self.y) 
        or obj.crash_with_point(self.x, self.y + self.height) or obj.crash_with_point(self.x + self.width, self.y + self.height))):
            if(obj.up):
                obj.x -= obj.a
                obj.y -= obj.b
            if(obj.down):
                obj.x += obj.a / 2
                obj.y += obj.b / 2
            if(obj.left):
                obj.angle += obj.rotation_speed
            if(obj.right):
                obj.angle -= obj.rotation_speed
            obj.calc_all()

    def ball_crash_with_corner(self, a, b, obj, new_angle):
        c = math.sqrt(a * a + b * b)
        if(c < obj.r):
            obj.x += a / c * obj.r - a
            obj.y += b / c * obj.r - b
            obj.angle = new_angle
            return True
        return False
                
    def crash_with_ball(self, obj):
        if(self.y < obj.y and self.y + self.height > obj.y and abs(self.x - obj.x) < obj.r):
            obj.angle = 540 - obj.angle
            obj.x -=  obj.r - abs(self.x - obj.x)
            return True
        elif(self.y < obj.y and self.y + self.height > obj.y and abs(self.x + self.width - obj.x) < obj.r):
            obj.angle = 540 - obj.angle
            obj.x +=  obj.r - abs(self.x + self.width - obj.x)
            return True
        elif(self.x < obj.x and self.x + self.width > obj.x and abs(self.y - obj.y) < obj.r):
            obj.angle = 360 - obj.angle
            obj.y -= obj.r - abs(self.y - obj.y)
            return True
        elif(self.x < obj.x and self.x + self.width > obj.x and abs(self.y + self.height - obj.y) < obj.r):
            obj.angle = 360 - obj.angle
            obj.y += obj.r - abs(self.y + self.height - obj.y)
            return True
        a = obj.x - self.x
        b = obj.y - self.y
        if(self.ball_crash_with_corner(a, b, obj, 225)):
            return True
        a -= self.width
        if(self.ball_crash_with_corner(a, b, obj, 315)):
            return True
        b -= self.height
        if(self.ball_crash_with_corner(a, b, obj, 45)):
            return True
        a += self.width
        if(self.ball_crash_with_corner(a, b, obj, 135)):
            return True
        return False