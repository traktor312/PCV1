# -*- coding: utf-8 -*- 
from tkinter import *
from tkinter import messagebox, colorchooser, simpledialog
from player import *
from wall import *
from ball import *
from maps import *
import random

config = [
    {
        "x": 70,
        "y": 60,
        "width": 50,
        "height": 40,
        "color": "green",
        "angle": 45,
        "up": "e",
        "down": "d",
        "left": "s",
        "right": "f",
        "shoot": "q"
    },{
        "x": 1530,
        "y": 840,
        "width": 50,
        "height": 40,
        "color": "red",
        "angle": 225,
        "up": "Up",
        "down": "Down",
        "left": "Left",
        "right": "Right",
        "shoot": "-"
    },{
        "x": 1530,
        "y": 60,
        "width": 50,
        "height": 40,
        "color": "yellow",
        "angle": 135,
        "up": "i",
        "down": "k",
        "left": "j",
        "right": "l",
        "shoot": "space"
    },{
        "x": 70,
        "y": 840,
        "width": 50,
        "height": 40,
        "color": "aqua",
        "angle": 315,
        "up": "5",
        "down": "2",
        "left": "1",
        "right": "3",
        "shoot": "7"
    }
]


class MyApp:
    def __init__(self, parent):
        self.dialog = False
        self.label_scores = []
        self.map = 0
        self.players = []
        self.player_num = 3
        self.scores = []
        self.walls = []
        self.balls = []
        self.ball_nuber = 0
        self.parent = parent
        self.start()
        self.draw()

    def draw(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=screen_width / 2, height=100, bg="black")
        self.canvas = Canvas(self.parent, width=1600, height=900, bg="white")
        self.canvas.pack()
        self.parent.bind("<KeyRelease>", self.key_release)
        self.parent.bind_all("<KeyPress>", self.key_press)
        self.parent.bind("<Key>", self.key)

        for i in range(len(config)):
            self.add_label(i)
        self.container.pack()

        self.canvas.focus_set()

        self.main()

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='Hra',menu=filemenu)
        filemenu.add_command(label='Restart',command=self.restart)
        filemenu.add_command(label='Počet hráčů',command=self.set_players_num)
        filemenu.add_command(label='Reset skóre',command=self.reset_score)
        filemenu.add_command(label='Konec',command=self.parent.destroy)
        
    def set_players_num(self):
        self.dialog = True
        num = simpledialog.askinteger("Input", "Zadej počet hráčů (2 až 4)", parent=self.parent)
        if(num != None):
            if(num > len(config)):
                self.player_num = len(config)
                self.restart()
            elif(num < 2):
                self.player_num = 2
                self.restart()
            elif(num >= 2 and num <= len(config)):
                self.player_num = num
                self.restart()
        self.dialog = False

    def add_label(self, i):
        self.label_scores.append(Label(self.container, text=self.print_score(i), fg=config[i]["color"], bg="black", font=("Helvetica", 30), padx=10)) 
        self.label_scores[i].grid(row=0,column=i,sticky='nwes')
        if(self.player_num <= i):
            self.label_scores[i].grid_remove()

    def update_score(self):
        for i in range(self.player_num):
            self.label_scores[i]['text'] = self.print_score(i)
        for i in range(len(config)):
            if(self.player_num <= i):
                self.label_scores[i].grid_remove()
            else:
                self.label_scores[i].grid()

    def defaul_set_score(self):
        self.scores = []
        for i in range(len(config)):
            self.scores.append(0)

    def reset_score(self):
        self.scores = []
        for i in range(len(config)):
            self.scores.append(0)
        self.update_score()

    
    def print_score(self, i):
        return config[i]["color"].upper() + ": " + str(self.scores[i])

    def add_player(self, i, x, y, w, h, col, angle, up, down, left, right, shoot):
        self.players.append(Player2(i, x, y, w, h, col, angle, up, down, left, right, shoot))

    def add_players(self):
        i = 0
        for p in config:
            if(len(self.players) < self.player_num):
                self.add_player(i, p["x"], p["y"], p["width"],p["height"], p["color"], p["angle"], p["up"], p["down"], p["left"], p["right"], p["shoot"])
                i += 1
            else:
                break

    def remove_player(self):
        for p in self.players:
            if(not p.live):
                self.players.pop(self.players.index(p))
        if(len(self.players) <= 1):
            root.after(2000, self.pre_restart) 

    def add_wall(self, x, y, w, h):
        self.walls.append(Rectangle(x, y, w, h))

    def load_map(self):
        for w in maps[self.map]:
            self.add_wall(w["x"], w["y"], w["w"], w["h"])

    def add_ball(self, x, y, angle, owner):
        self.balls.append(Ball(self.ball_nuber,x, y, 3, angle, owner))
        self.ball_nuber += 1

    def add_score(self):
        if(len(self.players) == 1):
            self.scores[self.players[0].id] += 1
            self.update_score()

    def clear_canvas(self):
        self.canvas.delete("all")

    def main(self):
        self.clear_canvas()
        for p in self.players:
            p.move()
        for w in self.walls:
            w.draw(self.canvas)
            for p in self.players:
                w.crash_with_rectangle(p)
            for b in self.balls:
                if(w.crash_with_ball(b)):
                    break
        for b in self.balls:
            b.move(self)
            b.draw(self.canvas)
            for p in self.players:
                b.crash_with_player(p, self)
        for p in self.players:
            if(p.live):
                p.draw(self.canvas)
        root.after(20, self.main)

    def start(self):
        self.walls = []
        self.balls = []
        self.players = []
        self.map = random.randint(0, len(maps) - 1)
        self.load_map()
        self.add_players()
        self.defaul_set_score()


    def pre_restart(self):
        self.add_score()
        self.restart()

    def restart(self):
        self.walls = []
        self.balls = []
        self.players = []
        self.map = random.randint(0, len(maps) - 1)
        self.load_map()
        self.add_players()
        self.update_score()

    def remove_ball(self, i):
        for j in self.balls:
            if(j.id == i):
                self.balls.pop(self.balls.index(j))

    def key_release(self, event):
        if(not self.dialog):
            for p in self.players:
                p.key_release(event.char, event.keysym)

    def key_press(self, event):
        if(not self.dialog):
            for p in self.players:
                p.key_press(event.char, event.keysym)

    def key(self, event):
        if(not self.dialog):
            for p in self.players:
                p.key(event.char, event.keysym, self)


root = Tk()
root.geometry("1600x1000")
myapp = MyApp(root)
root.mainloop()