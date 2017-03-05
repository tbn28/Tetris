import sys
import os
import re
import tkinter
from tkinter import *
import random

class Tetris:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tkinter.Canvas(root, height=800, width=400)
        self.canvas.grid(row=0, column=0)
        self.tickrate = 1000
        self.parent.after(self.tickrate, self.tick)
        self.shapes = {'s':[['*',''],
                            ['*','*'],
                            ['','*']],
                       'z':[['','*'],
                            ['*','*'],
                            ['*','']],
                       'r':[['*','*'],
                            ['*',''],
                            ['*','']],
                       'l':[['*',''],
                            ['*',''],
                            ['*','*']],
                       'o':[['*','*'],
                            ['*','*']],
                       'i':[['*'],
                            ['*'],
                            ['*'],
                            ['*']],
                       't':[['*','*','*'],
                            ['','*','']],
                       }


    def tick(self):
        print('ticking')
        self.parent.after(self.tickrate, self.tick)

    def down(self):
        pass

    def shift(self, direction):
        pass

    def rotate(self, direction):
        pass

    def settle(self):
        pass

    def spawn(self):
        pass

    def new(self):
        pass

    def lose(self):
        pass

    def clear(self):
        pass

root = tkinter.Tk()
tetris = Tetris(root)
root.mainloop()
