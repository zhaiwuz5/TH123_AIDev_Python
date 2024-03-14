from utils import address, fields, functions
import numpy as np
import time
import ctypes
import win32api
from pywinauto.application import Application


# TODO: 提供模拟键盘输入则主进程的功能
class KeyManager:
    def __init__(self, win):
        self.win = win
        self.win.set_focus()
        self.keymap = None
        self.keymap_ai = {
            'up': 'HOME',
            'down': 'END',
            'left': 'DELETE',
            'right': 'PGDN',
            'a': 'VK_NUMPAD7',
            'b': 'VK_NUMPAD8',
            'c': 'VK_NUMPAD9',
            'd': 'VK_NUMPAD4',
            'ab': 'VK_NUMPAD5',
            'bc': 'VK_NUMPAD6',
        }

        self.keymap_player = {
            'up': 'UP',
            'down': 'DOWN',
            'left': 'LEFT',
            'right': 'RIGHT',
            'a': 'VK_NUMPAD1',
            'b': 'VK_NUMPAD2',
            'c': 'VK_NUMPAD3',
            'd': 'ENTER',
            'ab': 'ADD',
            'bc': 'SUBTRACT',
        }

    def sendkeys(self, control_p, model_output, direction):
        print(model_output)
        left = model_output[0]
        right = model_output[1]
        up = model_output[2]
        down = model_output[3]
        a = model_output[4]
        b = model_output[5]
        c = model_output[6]
        d = model_output[7]
        ab = model_output[8]
        bc = model_output[9]
        comb = model_output[10]
        if control_p == 1:
            self.keymap = self.keymap_player
        else:
            self.keymap = self.keymap_ai
        if left:
            self.win.type_keys('{' + self.keymap['left'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['left'] + ' up}')

        if right:
            self.win.type_keys('{' + self.keymap['right'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['right'] + ' up}')

        if up:
            self.win.type_keys('{' + self.keymap['up'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['up'] + ' up}')

        if down:
            self.win.type_keys('{' + self.keymap['down'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['down'] + ' up}')

        if a:
            self.win.type_keys('{' + self.keymap['a'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['a'] + ' up}')

        if b:
            self.win.type_keys('{' + self.keymap['b'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['b'] + ' up}')

        if c:
            self.win.type_keys('{' + self.keymap['c'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['c'] + ' up}')

        if d:
            self.win.type_keys('{' + self.keymap['d'] + ' down}')
            time.sleep(0.01)
            self.win.type_keys('{' + self.keymap['d'] + ' up}')

        if ab:
            self.win.type_keys(self.keymap['ab'])

        if bc:
            self.win.type_keys(self.keymap['bc'])

        if comb:
            if direction == 1:
                if comb == 1:
                    self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['b'])

                if comb == 2:
                    self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['c'])

                if comb == 3:
                    self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['b'])

                if comb == 4:
                    self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['c'])

                if comb == 5:
                    self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['b'])

                if comb == 6:
                    self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['c'])

                if comb == 7:
                    self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['b'])

                if comb == 8:
                    self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['c'])

                if comb == 9:
                    self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['b'])

                if comb == 10:
                    self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['c'])

            if direction == 255:
                if comb == 1:
                    self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['b'])

                if comb == 2:
                    self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['c'])

                if comb == 3:
                    self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['b'])

                if comb == 4:
                    self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['c'])

                if comb == 5:
                    self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['b'])

                if comb == 6:
                    self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['c'])

                if comb == 7:
                    self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['b'])

                if comb == 8:
                    self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['c'])

                if comb == 9:
                    self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['b'])

                if comb == 10:
                    self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['c'])








