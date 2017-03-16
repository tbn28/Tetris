import sys
import os
import re
import tkinter
from tkinter import *
import random
from matrix_rotation import rotate_array

class Shape:
    def __init__(self, shape, piece, row, column, coords):
        self.shape = shape
        self.piece = piece
        self.row = row
        self.column = column
        self.coords = coords

class Tetris:
    def __init__(self, parent):
        parent.title('Tetris')
        self.parent = parent
        self.board_width = 10
        self.board_height = 24
        self.board = [['' for column in range(self.board_width)]
                      for row in range(self.board_height)]
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
        self.parent.bind('<Down>', self.shift)
        self.parent.bind('<Left>', self.shift)
        self.parent.bind('<Right>', self.shift)
        self.parent.bind('a', self.shift)
        self.parent.bind('A', self.shift)
        self.parent.bind('d', self.shift)
        self.parent.bind('D', self.shift)
        self.parent.bind('s', self.shift)
        self.parent.bind('S', self.shift)
        self.parent.bind('q', self.rotate)
        self.parent.bind('Q', self.rotate)
        self.parent.bind('e', self.rotate)
        self.parent.bind('E', self.rotate)
        self.parent.bind('0', self.rotate)
        self.parent.bind('<Up>', self.rotate)
        self.parent.bind('w', self.rotate)
        self.parent.bind('W', self.rotate)

    def print_board(self):
        for row in self.board:
            print(*(cell or ' ' for cell in row), sep='')

    def check_and_move(self, shape, r, c, l, w):
        for row, squares in zip(range(r, r + l), shape):
            for column, square in zip(range(c, c + w), squares):
                if (row not in range(self.board_height)
                    or
                    column not in range(self.board_width)
                    or
                    (square and self.board[row][column] == 'x')):
                    return
        square_idxs = iter(range(4))

        for row in self.board:
            row[:] = ['' if cell == '*' else cell for cell in row]

        for row, squares in zip(range(r, r + l), shape):
            for column, square in zip(range(c, c + w), squares):
                if square:
                    self.board[row][column] = square
                    square_idx = next(square_idxs)
                    coord = (column*self.square_width,
                             row*self.square_width,
                             (column + 1 )*self.square_width,
                             (row + 1)*self.square_width)
                    self.active_piece.coords[square_idx] = coord
                    self.canvas.coords(self.active_piece.piece[square_idx], coord)

        self.active_piece.row = r
        self.active_piece.column = c
        self.active_piece.shape = shape
        self.print_board()
        return True


    def rotate(self, event=None):
        if not self.piece_is_active:
            return
        if len(self.active_piece.shape) == len(self.active_piece.shape[0]):
            return
        r = self.active_piece.row
        c = self.active_piece.column
        l = len(self.active_piece.shape)
        w = len(self.active_piece.shape[0])
        x = c + w//2
        y = r + l//2

        direction = event.keysym

        if direction in {'q', 'Q'}:
            shape = rotate_array(self.active_piece.shape, -90)
            rotation_index = (self.active_piece.rotation_index - 1) % 4
            rx, ry = self.active_piece.rotation[rotation_index]
            rotation_offsets = -rx, -ry
        elif direction in {'e', 'E', '0', 'Up', 'w', 'W'}:
            shape = rotate_array(self.active_piece.shape, 90)
            rotation_index = self.active_piece.rotation_index
            rotation_offsets = self.active_piece.rotation[rotation_index]
            rotation_index = (rotation_index + 1) % 4

        l = len(shape)
        w = len(shape[0])
        rt = y - l//2
        ct = x - w//2

        x_correction, y_correction = rotation_offsets
        rt += y_correction
        ct += x_correction

        success = self.check_and_move(shape, rt, ct, l, w)
        if not success:
            return

        self.active_piece.rotation_index = rotation_index

    def tick(self):
        if not self.piece_is_active:
            self.spawn()

        #self.parent.after(self.tickrate, self.tick)

    def shift(self, event=None):
        down = {'Down', 's', 'S'}
        left = {'Left', 'a', 'A'}
        right = {'Right', 'd', 'D'}
        if not self.piece_is_active:
            return

        r = self.active_piece.row
        c = self.active_piece.column
        l = len(self.active_piece.shape)
        w = len(self.active_piece.shape[0])

        direction = (event and event.keysym) or 'Down'
        #print(direction)

        if direction in down:
            rt = r + 1
            ct = c
        elif direction in left:
            rt = r
            ct = c - 1
        elif direction in right:
            rt = r
            ct = c + 1

        success = self.check_and_move(self.active_piece.shape, rt, ct, l, w)

        if direction in down and not success:
            self.settle()
            return

    def settle(self):
        pass
        self.piece_is_active = False
        print('hyc')
        for row in self.board:
            row[:] = ['x' if cell == '*' else cell for cell in row]
            print(*(cell or '' for cell in row))
        self.parent.after(self.tickrate, self.spawn())

    def spawn(self):
        self.piece_is_active = True
        shape = self.shapes[random.choice('szrloit')]
        shape = rotate_array(shape, random.choice((0, 90, 180, 270)))
        width = len(shape[0])
        start = (10-width)//2
        self.active_piece = Shape(shape, [], 0, start, [])

        for y, row in enumerate(shape):
            self.board[y][start:start+width] = shape[y]
            for x, cell in enumerate(row, start=start):
                if cell:
                    self.active_piece.coords.append((self.square_width*x,
                                                        self.square_width*y,
                                                        self.square_width*(x+1),
                                                        self.square_width*(y+1)))
                    self.active_piece.piece.append(
                    self.canvas.create_rectangle(self.active_piece.coords[-1]))

        self.active_piece.rotation_index = 0
        if 3 in (len(shape), len(shape[0])):
            self.active_piece.rotation = [(0, 0),
                                          (1, 0),
                                          (-1, 1),
                                          (0, -1)]
        else:
            self.active_piece.rotation = [(1, -1),
                                          (0, 1),
                                          (0, 0),
                                          (-1, 0)]
        if len(shape) < len(shape[0]):
            self.active_piece.rotation_index += 1

        self.print_board()

    def new(self):
        pass

    def lose(self):
        pass

    def clear(self):
        pass

root = tkinter.Tk()
tetris = Tetris(root)
root.mainloop()
#