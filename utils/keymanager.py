from utils import address, fields, functions
import numpy as np
import time
from pywinauto.application import Application


# TODO: 提供模拟键盘输入则主进程的功能
class KeyManager:
    def __init__(self):
        self.app = Application().connect(process=fields.processID)
        self.win = self.app.top_window()
        self.win.set_focus()
        self.keymap = {
            '421': '{LEFT}{DOWN}{LEFT}',
            '214': '{}',
            '236': '{}',
            '623': '{}',
            '22': '{}'
        }

    def sendkeys(self, model_output):
        left = np.floor(model_output[0])
        right = np.floor(model_output[1])
        up = np.floor(model_output[2])
        down = np.floor(model_output[3])
        a = np.floor(model_output[4])
        b = np.floor(model_output[5])
        c = np.floor(model_output[6])
        d = np.floor(model_output[7])
        ab = np.floor(model_output[8])
        bc = np.floor(model_output[9])
        comb = np.floor(model_output[10])








