import sys
import os
import re
import tkinter
from tkinter import *
import random
from matrix_rotation import rotate_array
try:
    import pygame
except ImportError:
    audio = None
else:
    audio = True

class Shape:
    def __init__(self, shape, key, piece, row, column, coords):
        self.shape = shape
        self.key = key
        self.piece = piece
        self.row = row
        self.column = column
        self.coords = coords

class Tetris:
    def __init__(self, parent):
        self.debug = 'debug' in sys.argv[1:]
        self.random = 'random' in sys.argv[1:]
        parent.title('Tetris')
        self.parent = parent
        if audio:
            pygame.mixer.init(buffer=512)
            try:
                self.sounds = {name:pygame.mixer.Sound(name)
                               for name in ('music.ogg',
                                            'settle.ogg',
                                            'clear.ogg',
                                            'lose.ogg')}
            except pygame.error:
                self.audio = None
                print(pygame.error)
            else:
                self.audio = {'m': True, 'f': True}
                for char in 'mMfF':
                    self.parent.bind(char, self.toggle_audio)
                self.sounds['music.ogg'].play(loops=-1)

        self.board_width = 10
        self.board_height = 24

        self.high_score = 1
        self.width = 300
        self.height = 720
        self.square_width = self.width//10
        self.max_speed_score = 1000
        self.speed_factor = 50

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
        self.colors = {
            's': 'green',
            'z': 'yellow',
            'r': 'turquoise',
            'l': 'orange',
            'o': 'blue',
            'i': 'red',
            't': 'violet'
        }
        for key in ('<Down>', '<Left>', '<Right>', 'a', 'A', 's', 'S', 'd', 'D'):
            self.parent.bind(key, self.shift)
        for key in ('<Up>', 'q', 'Q', 'e', 'E', 'w', 'W'):
            self.parent.bind(key, self.rotate)
        for key in ('<space>', 'z', 'Z', 'c', 'C'):
            self.parent.bind(key, self.snap)
        self.parent.bind('<Escape>', self.pause)
        self.parent.bind('<Control-n>', self.draw_board)
        self.parent.bind('<Control-N>', self.draw_board)
        self.canvas = None
        self.preview_canvas = None
        self.ticking = None
        self.spawning = None
        self.score_var = tkinter.StringVar()
        self.high_score_var = tkinter.StringVar()
        self.high_score_var.set('High Score:\n0')
        self.preview_label = tkinter.Label(root,
                                           text='Next Piece:',
                                           width=15,
                                           font=('Arial Black', 12))
        self.preview_label.grid(row=0, column=1, sticky='S')
        self.score_label = tkinter.Label(root,
                                         textvariable=self.score_var,
                                         width=15,
                                         height=5,
                                         font=('Arial Black', 12))
        self.score_label.grid(row=2, column=1, sticky='S')
        self.high_score_label = tkinter.Label(root,
                                              textvariable=self.high_score_var,
                                              width=15,
                                              height=5,
                                              font=('Arial Black', 12))
        self.high_score_label.grid(row=3, column=1, sticky='N')

        self.draw_board()

    def draw_board(self, event=None):
        if self.ticking:
            self.parent.after_cancel(self.ticking)
        if self.spawning:
            self.parent.after_cancel(self.spawning)
        self.score_var.set('Score:\n0')
        self.board = [['' for column in range(self.board_width)]
                      for row in range(self.board_height)]
        self.field = [[None for column in range(self.board_width)]
                      for row in range(self.board_height)]
        if self.canvas:
            self.canvas.destroy()
        self.canvas = tkinter.Canvas(root, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, rowspan=4)
        self.h_separator = self.canvas.create_line(0,
                                                 self.height//6,
                                                 self.width,
                                                 self.height//6,
                                                 width=2)
        self.v_separator = self.canvas.create_line(self.width,
                                                   0,
                                                   self.width,
                                                   self.height,
                                                   width=2)
        if self.preview_canvas:
            self.preview_canvas.destroy()
        self.preview_canvas = tkinter.Canvas(root,
                                        width=5 * self.square_width,
                                        height=5 * self.square_width)
        self.preview_canvas.grid(row=1, column=1)
        self.tickrate = 1000
        self.score = 0
        self.piece_is_active = False
        self.paused = False
        self.bag = ()
        self.preview()

        self.spawning = self.parent.after(self.tickrate, self.spawn)
        self.ticking = self.parent.after(self.tickrate*2, self.tick)

    def toggle_audio(self, event=None):
        if not event:
            return
        key = event.keysym.lower()
        self.audio[key] = not self.audio[key]
        if key == 'm':
            if not self.audio['m']:
                self.sounds['music.ogg'].stop()
            else:
                self.sounds['music.ogg'].play(loops=-1)

    def pause(self, event=None):
        if self.piece_is_active and not self.paused:
            self.paused = True
            self.piece_is_active = False
            self.parent.after_cancel(self.ticking)
        elif self.paused:
            self.paused = False
            self.piece_is_active = True
            self.ticking = self.parent.after(self.tickrate, self.tick)

    def print_board(self):
        for row in self.board:
            print(*(cell or ' ' for cell in row), sep='')

    def check(self, shape, r, c, l, w):
        for row, squares in zip(range(r, r + l), shape):
            for column, square in zip(range(c, c + w), squares):
                if (row not in range(self.board_height)
                    or
                    column not in range(self.board_width)
                    or
                        (square and self.board[row][column] == 'x')):
                    return
        return True

    def move(self, shape, r, c, l, w):
        square_idxs = iter(range(4))

        for row in self.board:
            row[:] = ['' if cell == '*' else cell for cell in row]

        for row, squares in zip(range(r, r + l), shape):
            for column, square in zip(range(c, c + w), squares):
                if square:
                    self.board[row][column] = square
                    square_idx = next(square_idxs)
                    coord = (column * self.square_width,
                             row * self.square_width,
                             (column + 1) * self.square_width,
                             (row + 1) * self.square_width)
                    self.active_piece.coords[square_idx] = coord
                    self.canvas.coords(self.active_piece.piece[square_idx], coord)

        self.active_piece.row = r
        self.active_piece.column = c
        self.active_piece.shape = shape
        if self.debug:
            self.print_board()
        return True

    def check_and_move(self, shape, r, c, l, w):
        if self.check(shape, r, c, l, w):
            self.move(shape, r, c, l, w)
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
        if self.piece_is_active:
            self.shift()
        self.ticking = self.parent.after(self.tickrate, self.tick)

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

    def settle(self):
        self.piece_is_active = False
        for row in self.board:
            row[:] = ['x' if cell == '*' else cell for cell in row]
        for (x1, y1, x2, y2), id in zip(self.active_piece.coords, self.active_piece.piece):
            self.field[y1//self.square_width][x1//self.square_width] = id
        indices = [idx for idx, row in enumerate(self.board) if all(row)]
        if indices:
            self.score += (1, 2, 5, 10)[len(indices) - 1]
            self.clear(indices)
            if all(not cell for row in self.board for cell in row):
                self.score += 10
            self.high_score = max(self.score, self.high_score)
            self.score_var.set('Score: \n{}'.format(self.score))
            self.high_score_var.set('High score: \n{}'.format(self.high_score))
            if self.score <= self.max_speed_score:
                self.tickrate = 1000 // (self.score // self.speed_factor + 1)
        if any(any(row) for row in self.board[:4]):
            self.lose()
            return
        if self.audio['f'] and not indices:
            self.sounds['settle.ogg'].play()
        self.spawning = self.parent.after(self.tickrate, self.spawn)

    def preview(self):
        self.preview_canvas.delete(tkinter.ALL)
        if not self.bag:
            if self.random:
                self.bag.append(random.choice('szrloit'))
            else:
                self.bag = random.sample('szrloit', 7)
        key = self.bag.pop()
        shape = rotate_array(self.shapes[key], random.choice((0, 90, 180, 270)))
        self.preview_piece = Shape(shape, key, [], 0, 0, [])
        width = len(shape[0])
        half = self.square_width // 2

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.preview_piece.coords.append((self.square_width * x + half,
                                                        self.square_width * y + half,
                                                        self.square_width*(x+1) + half,
                                                        self.square_width*(y+1) + half))
                    self.preview_piece.piece.append(
                        self.preview_canvas.create_rectangle(self.preview_piece.coords[-1],
                                                 fill=self.colors[key],
                                                 width=3))

        self.preview_piece.rotation_index = 0
        self.preview_piece.i_nudge = (len(shape) < len(shape[0])
                                                      ) and 4 in (len(shape), len(shape[0]))
        self.preview_piece.row = self.preview_piece.i_nudge

        if 3 in (len(shape), len(shape[0])):
            self.preview_piece.rotation = [(0, 0),
                                          (1, 0),
                                          (-1, 1),
                                          (0, -1)]
        else:
            self.preview_piece.rotation = [(1, -1),
                                          (0, 1),
                                          (0, 0),
                                          (-1, 0)]
        if len(shape) < len(shape[0]):
            self.preview_piece.rotation_index += 1

    def spawn(self):
        self.piece_is_active = True
        self.active_piece = self.preview_piece
        self.preview()
        width = len(self.active_piece.shape[0])
        start = (10 - width)//2
        self.active_piece.column = start
        self.active_piece.start = start
        self.active_piece.coords = []
        self.active_piece.piece = []

        for y, row in enumerate(self.active_piece.shape):
            self.board[y+self.active_piece.i_nudge][start:start+width] = self.active_piece.shape[y]
            for x, cell in enumerate(row, start=start):
                if cell:
                    self.active_piece.coords.append((self.square_width*x,
                                                     self.square_width*(y+self.active_piece.i_nudge),
                                                     self.square_width*(x+1),
                                                     self.square_width*(y+self.active_piece.i_nudge+1)))
                    self.active_piece.piece.append(
                    self.canvas.create_rectangle(self.active_piece.coords[-1],
                                                 fill=self.colors[self.active_piece.key],
                                                 width = 3)
                    )
        if self.debug:
            self.print_board()

    def lose(self):
        self.piece_is_active = False
        if self.audio['f']:
            self.sounds['lose.ogg'].play()
        self.parent.after_cancel(self.ticking)
        self.parent.after_cancel(self.spawning)
        self.clear_iter(range(len(self.board)))

    def snap(self, event=None):
        down = {'space'}
        left = {'z', 'Z'}
        right = {'0', 'c', 'C'}
        if not self.piece_is_active:
            return
        r = self.active_piece.row
        c = self.active_piece.column
        l = len(self.active_piece.shape)
        w = len(self.active_piece.shape[0])

        direction = event.keysym

        while 1:
            if self.check(self.active_piece.shape,
                          r+(direction in down),
                          c+(direction in right) - (direction in left),
                          l, w):
                r += direction in down
                c += (direction in right) - (direction in left)
            else:
                break

        self.move(self.active_piece.shape, r, c, l, w)

        if direction in down:
            self.settle()

    def clear(self, indices):
        if self.audio['f']:
            self.sounds['clear.ogg'].play()
        for idx in indices:
            self.board.pop(idx)
            self.board.insert(0, ['' for column in range(self.board_width)])
        self.clear_iter(indices)

    def clear_iter(self, indices, current_column=0):
        for row in indices:
            if row%2:
                cc = current_column
            else:
                cc = self.board_width - current_column - 1
            id = self.field[row][cc]
            self.field[row][cc] = None
            self.canvas.delete(id)
        if current_column < self.board_width - 1:
            self.parent.after(50, self.clear_iter, indices, current_column + 1)
        else:
            for idx, row in enumerate(self.field):
                offset = sum(r > idx for r in indices)*self.square_width
                for square in row:
                    if square:
                        self.canvas.move(square, 0, offset)
            for row in indices:
                self.field.pop(row)
                self.field.insert(0, [None for x in range(self.board_width)])


root = tkinter.Tk()
tetris = Tetris(root)
root.mainloop()
