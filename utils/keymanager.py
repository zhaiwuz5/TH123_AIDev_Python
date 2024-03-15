from utils import address, fields, functions, dx_keycode

import time
import ctypes

from pywinauto.application import Application


# TODO: 提供模拟键盘输入则主进程的功能
# 定义常量
DIK_CODE_P = {
    'up': dx_keycode.DIK_UP,  # UP arrow
    'down': dx_keycode.DIK_DOWN,  # DOWN arrow
    'left': dx_keycode.DIK_LEFT,  # LEFT arrow
    'right': dx_keycode.DIK_RIGHT,  # RIGHT arrow
    'a': dx_keycode.DIK_Z,  # A key
    'b': dx_keycode.DIK_X,  # B key
    'c': dx_keycode.DIK_C,  # C key
    'd': dx_keycode.DIK_A,  # D key
    'ab': dx_keycode.DIK_S,  # A key
    'bc': dx_keycode.DIK_D,  # B key
}

DIK_CODE_AI = {
    'up': dx_keycode.DIK_HOME,  # UP arrow
    'down': dx_keycode.DIK_END,  # DOWN arrow
    'left': dx_keycode.DIK_DELETE,  # LEFT arrow
    'right': dx_keycode.DIK_NEXT,  # RIGHT arrow
    'a': dx_keycode.DIK_NUMPAD7,  # NUMPAD7
    'b': dx_keycode.DIK_NUMPAD8,  # B key
    'c': dx_keycode.DIK_NUMPAD9,  # C key
    'd': dx_keycode.DIK_NUMPAD4,  # D key
    'ab': dx_keycode.DIK_NUMPAD5,  # A key
    'bc': dx_keycode.DIK_NUMPAD6,  # B key
}

# DIK_CODE = DIK_CODE_AI
# 定义函数
keybd_event = ctypes.windll.user32.keybd_event

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
def press_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, DIK_CODE[hexKeyCode], 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, DIK_CODE[hexKeyCode],
                        0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

class KeyManager:
    def __init__(self, win):
        self.win = win
        self.win.set_focus()
        self.keymap = None

    def send_z(self):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, DIK_CODE_P['a'], 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        time.sleep(0.1)
        ii_.ki = KeyBdInput(0, DIK_CODE_P['a'],
                            0x0008 | 0x0002, 0,
                            ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def sendkeys(self, control_p, model_output, direction):
        global DIK_CODE
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
            DIK_CODE = DIK_CODE_P
        else:
            DIK_CODE = DIK_CODE_AI
        if left:
            press_key('left')
        else:

            release_key('left')

        if right:
            press_key('right')
        else:

            release_key('right')

        if up:
            press_key('up')
        else:

            release_key('up')

        if down:
            press_key('down')
        else:

            release_key('down')

        if a:
            press_key('a')
        else:

            release_key('a')

        if b:
            press_key('b')
        else:

            release_key('b')

        if c:
            press_key('c')
        else:

            release_key('c')

        if d:
            press_key('d')
        else:

            release_key('d')

        if ab:
            press_key('ab')
        else:

            release_key('ab')

        if bc:
            press_key('bc')
        else:

            release_key('bc')

        if comb:
            if direction == 1:
                pass
            #     if comb == 1:
            #         self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['b'])
            #
            #     if comb == 2:
            #         self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['c'])
            #
            #     if comb == 3:
            #         self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['b'])
            #
            #     if comb == 4:
            #         self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['c'])
            #
            #     if comb == 5:
            #         self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['b'])
            #
            #     if comb == 6:
            #         self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['c'])
            #
            #     if comb == 7:
            #         self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['b'])
            #
            #     if comb == 8:
            #         self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['c'])
            #
            #     if comb == 9:
            #         self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['b'])
            #
            #     if comb == 10:
            #         self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['c'])
            #
            # if direction == 255:
            #     if comb == 1:
            #         self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['b'])
            #
            #     if comb == 2:
            #         self.win.type_keys(self.keymap['right']+self.keymap['down']+self.keymap['right']+self.keymap['c'])
            #
            #     if comb == 3:
            #         self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['b'])
            #
            #     if comb == 4:
            #         self.win.type_keys(self.keymap['down']+self.keymap['right']+self.keymap['c'])
            #
            #     if comb == 5:
            #         self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['b'])
            #
            #     if comb == 6:
            #         self.win.type_keys(self.keymap['down']+self.keymap['down']+self.keymap['c'])
            #
            #     if comb == 7:
            #         self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['b'])
            #
            #     if comb == 8:
            #         self.win.type_keys(self.keymap['down']+self.keymap['left']+self.keymap['c'])
            #
            #     if comb == 9:
            #         self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['b'])
            #
            #     if comb == 10:
            #         self.win.type_keys(self.keymap['left']+self.keymap['down']+self.keymap['left']+self.keymap['c'])








