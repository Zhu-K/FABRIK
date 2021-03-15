# FABRIK imeplementation of IK
# Author: Kai Zhu
# 2021

from tkinter import *
import math
from lib.ikchain import IKChain

VERSION = "0.6"

master = Tk()
master.title("IK GUI  " + VERSION)
master.resizable(0,0)
master.configure(bg="black")

l1text = StringVar()
txtLen = "100,100,100"

CANVAS_W = 1000
CANVAS_H = 750
ORIGIN = [CANVAS_W / 2, CANVAS_H / 2]

tgt_x = ORIGIN[0] + 700
tgt_y = ORIGIN[1]

def canvas_drag(event):
    x = event.x                             # get grid coords
    y = event.y

    c.coords(tgt, x-10, y-10, x+10, y+10)   # move the blue target pos dot

    arms.solve([x, y], fixed = True)                      # solve and render IK
    arms.update()

    labeltext = ""                          # update status bar
    for i in range(len(arms.segments)):
        labeltext += f"seg{i}: {int(math.degrees(arms.segments[i].local_angle))}   "
    l1text.set(labeltext)

def endProg(*arg):
    # exit program
    master.destroy()

def newIK(event):
    # creates new IK with segments specified in text entry
    global arms
    global txtLen
    
    master.focus()

    # checks for valid input, reset entry if not valid
    temp = e_lengths.get()
    lengths = temp.split(',')
    for i, length in enumerate(lengths):
        if length.strip().isnumeric() and int(length) > 0:
            lengths[i] = int(length)
        else:
            e_lengths.delete(0,END)
            e_lengths.insert(0,txtLen)
            return

    txtLen = temp
    arms.clearCanvas()
    arms = IKChain(ORIGIN, lengths)
    arms.draw(c)

# GUI creation
c = Canvas(master, width = CANVAS_W, height = CANVAS_H, bg="black", highlightthickness=0)
c.grid(row=1, columnspan=10)

e_lengths = Entry(master, bg="black", fg="white", justify="left", insertbackground  = "gray",relief = FLAT)
e_lengths.grid(row=2, column=0, sticky = W+E, columnspan=10)
e_lengths.insert(0, txtLen)
e_lengths.bind("<Return>", newIK)

l1 = Label(master,text="",bg = "black", fg="white", textvariable=l1text)
l1.grid(row=3, column=0, sticky = W+E, columnspan=10)

b_exit = Button(master,text="Exit", fg="white", bg = "black",relief=FLAT, width = 10)
b_exit.grid(row=2, column=9, sticky=E)
b_exit.bind("<Button-1>", endProg)

tgt = c.create_oval(tgt_x - 10, tgt_y - 10, tgt_x + 10, tgt_y + 10, fill="cyan", outline="green", tag = "tgt")

c.bind("<B1-Motion>", canvas_drag)      # binds mouse drag event

# creates IK system
arms = IKChain(ORIGIN, [100,100,100])   
arms.draw(c)


master.mainloop()

