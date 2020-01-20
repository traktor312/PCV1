from abc import ABC, abstractmethod

# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"red",
      "outline":"black",
      "width":"5",}

import math

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
    def draw(self, canvas):       
        return canvas.create_rectangle(self.x, self.y, self.x+10, self.y+10, fill=DEFAULT_CONFIG['fill'])
        
    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y


class Shape(ABC):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.width = 200
        self.height = 100
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

    @abstractmethod
    def draw(self, canvas):
        pass


    @abstractmethod
    def detect_cursor(self, point):
        pass


class Rectangle(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill_color = "red"

    def __repr__(self):
        return "Rectangle(x: {}, y: {}, width: {}, height: {}, fill_color: {}, width:{} )".format(self.x, self.y, self.width, self.height, self.fill_color, width=self.outline_width)

    def draw(self, canvas):
       return canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.fill_color, outline=self.outline_color, width=self.outline_width) 

    def detect_cursor(self, point):
        return True if self.x <= point.x <= self.x + self.width and self.y <= point.y <= self.y + self.height else False


class Oval(Shape):
    def __repr__(self):
        return "Oval(x: {}, y: {}, width: {}, height: {}, fill_color: {}, width:{} )".format(self.x, self.y, self.width, self.height, self.fill_color, width=self.outline_width)
    
    def draw(self, canvas):
        return canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.fill_color, outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self, point):
        return True if ((point.x - (self.x + self.width / 2)) ** 2) / ((self.width / 2) ** 2) + ((point.y - (self.y + self.height / 2)) ** 2) / ((self.height / 2) ** 2) <= 1 else False

