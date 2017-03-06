import sys
import os
import re
import tkinter
from tkinter import *
import random
from matrix_rotation import rotate_array

class Tetris:
    def __init__(self, parent):
        self.parent = parent
        self.width = 300
        self.height = 720
        self.square_width = self.width//10
        self.canvas = tkinter.Canvas(root, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)
        self.separator = self.canvas.create_line(0,
                                                 self.height//6,
                                                 self.width,
                                                 self.height//6,
                                                 width=2)
        self.tickrate = 1000
        self.piece_is_active = False
        self.parent.after(self.tickrate, self.tick)
        self.shapes = {'s': [['*', ''],
                             ['*', '*'],
                             ['', '*']],
                       'z': [['', '*'],
                             ['*', '*'],
                             ['*', '']],
                       'r': [['*', '*'],
                             ['*', ''],
                             ['*', '']],
                       'l': [['*', ''],
                             ['*', ''],
                             ['*', '*']],
                       'o': [['*', '*'],
                             ['*', '*']],
                       'i': [['*'],
                             ['*'],
                             ['*'],
                             ['*']],
                       't': [['*', '*', '*'],
                             ['', '*', '']]
                       }

    def tick(self):
        if not self.piece_is_active:
            self.spawn()
            self.piece_is_active = not self.piece_is_active


        #self.parent.after(self.tickrate, self.tick)

    def down(self):
        pass

    def shift(self, direction):
        pass

    def rotate(self, direction):
        pass

    def settle(self):
        pass
        self.piece_is_active = not self.piece_is_active

    def spawn(self):
        shape = self.shapes[random.choice('szrloit')]
        shape = rotate_array(shape, random.choice((0, 90, 180, 270)))
        width = len(shape[0])
        start = (10-width)//2
        self.active_piece = [shape, []]
        for y, row in enumerate(shape):
            for x, column in enumerate(row, start=start):
                if column:
                    self.active_piece[1].append(
                    self.canvas.create_rectangle(self.square_width*x,
                                                 self.square_width*y,
                                                 self.square_width*(x+1),
                                                 self.square_width*(y+1)))


    def new(self):
        pass

    def lose(self):
        pass

    def clear(self):
        pass

root = tkinter.Tk()
tetris = Tetris(root)
root.mainloop()
