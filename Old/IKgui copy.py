
VERSION = "0.5"

from time import time
from tkinter import *
import random
import numpy as np
import math

GRAY = "#505050"
DARKGRAY = "#303030"

master = Tk()
l1text = StringVar()

master.configure(bg="black")
master.title("IK GUI" + VERSION)
master.resizable(0,0)

CANVAS_W = 1000
CANVAS_H = 750
ORIGIN = [CANVAS_W / 2, CANVAS_H / 2]

tgt_x = ORIGIN[0] + 
tgt_y = ORIGIN[1]

arm1_len = 200





    

def normalize(v):
    mag = np.linalg.norm(v)
    if mag > 0:
        return v/mag
    else:
        return 0

def canvas_drag(event):
    x = event.x       # get grid coords
    y = event.y
    #c.move(tgt, x, y)
    c.coords(tgt, x-10, y-10, x+10, y+10)

    arms[-1].backSolve([x,y])

    labeltext = ""
    for i in range(len(arms)):
        labeltext += f"seg{i}: {int(math.degrees(arms[i].local_angle))}   "

    l1text.set(labeltext)


def endProg(*arg):
    # exit program
    master.destroy()


# GUI creation

c = Canvas(master, width = CANVAS_W, height = CANVAS_H, bg="black", highlightthickness=0)
c.grid(row=1, columnspan=10)

l1 = Label(master,text="Arm1: ",bg = "black", fg="white", textvariable=l1text)
l1.grid(row=2, column=0, sticky = W)

# e_width = Entry(master, bg=DARKGRAY, fg="yellow", width = 3, justify="right", relief = FLAT)
# e_width.grid(row=2, column=1, sticky = W)
# e_width.insert(0, str(maze_w))

b_exit = Button(master,text="Exit", fg="green", bg = "black",relief=FLAT, width = 10)
b_exit.grid(row=2, column=9, sticky=W+E)
b_exit.bind("<Button-1>", endProg)

# statusbar = Label(master, text="", bd=1, bg = DARKGRAY, fg = "yellow", pady=5, padx=5)
# statusbar.grid(row=3, columnspan = 10, sticky=W+E)

tgt = c.create_oval(tgt_x - 10, tgt_y - 10, tgt_x + 10, tgt_y + 10, fill="cyan", outline="green", tag = "tgt")  # resetting start

arms = [Segment(ORIGIN, 100, 0)]
for _ in range(2):
    arms.append(Segment(arms[-1], 100, 0))


c.bind("<B1-Motion>", canvas_drag)


master.mainloop()

