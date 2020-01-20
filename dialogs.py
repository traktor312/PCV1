from tkinter import *

class ObjectDialog():
    def __init__(self, parent, shape):
        self.shape = shape
        top = self.top = Toplevel(parent)
        top.title("Parametry objektu")
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        x = parent.winfo_x()
        y = parent.winfo_y()
        top.geometry("%dx%d+%d+%d" % (400, 300, x + 100, y + 100))
        container1 = Frame(top, width=400, pady=10, padx=10)
        label_pozice = Label(container1, text="Pozice objektu", pady=5)
        label_pozice.pack()
        label_x = Label(container1, text="x:")
        label_x.pack(side=LEFT)
        spinbox_x = Spinbox(container1)
        spinbox_x.pack(side=LEFT)
        label_y = Label(container1, text="y:")
        label_y.pack(side=LEFT)
        spinbox_y = Spinbox(container1)
        spinbox_y.pack(side=LEFT)
        container1.pack(fill=BOTH)

        button_ok = Button(top, text="OK", command = self.ok)
        button_ok.pack()

    def ok(self, event=None):
        self.top.destroy()