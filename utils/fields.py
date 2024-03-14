"""
这是一个用于读取游戏内存的模块，主要基于Python pywin32库实现。
首先获取游戏窗口的句柄，然后获取游戏进程的句柄，最后通过进程句柄读取游戏内存中的属性值。
对外主要提供以下函数：
------------------------------------------------
初始化函数：
1. update_proc()：获取游戏窗口句柄和进程句柄。
2. update_proc_with_pid(pid)：根据进程id获取进程句柄。
3. update_pbattleMgr()：获取游戏内存中的pbattleMgr对象。

读取函数：
1. get_int(address, offset)：根据基地址加偏移量的形式读取int属性的值。
2. get_short(address, offset)：根据基地址加偏移量的形式读取short属性的值。
3. get_float(address, offset)：根据基地址加偏移量的形式读取float属性的值。
4. get_char(address, offset)：根据基地址加偏移量的形式读取char属性的值。
5. get_uchar(address, offset)：根据基地址加偏移量的形式读取uchar属性的值。
6. get_ptr(address, offset)：根据基地址加偏移量的形式读取void *属性的值。

写入函数：
1. set_int(address, offset, value)：根据基地址加偏移量的形式写入int属性的值。
2. set_short(address, offset, value)：根据基地址加偏移量的形式写入short属性的值。
3. set_float(address, offset, value)：根据基地址加偏移量的形式写入float属性的值。
4. set_char(address, offset, value)：根据基地址加偏移量的形式写入char属性的值。
5. set_uchar(address, offset, value)：根据基地址加偏移量的形式写入uchar属性的值。

@Author: zhaiwuz5
@Reference: https://github.com/SokuDev/SokuMods/blob/master/modules/LabTool/fields.h
"""

import ctypes
import struct
import win32gui
import win32process
import win32con
from utils import address
import psutil

kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
ReadProcessMemory = kernel32.ReadProcessMemory
WriteProcessMemory = kernel32.WriteProcessMemory
OpenProcess = kernel32.OpenProcess

# Description: This file contains the offsets for the fields of the classes in the game.
CF_UNKNOWN = 0x7D0  # short
CF_X_POS = 0x0EC  # float
CF_Y_POS = 0x0F0  # float
CF_X_SPEED = 0x0F4  # float
CF_Y_SPEED = 0x0F8  # float
CF_GRAVITY = 0x100  # float
CF_DIR = 0x104  # char
CF_COLOR_B = 0x110  # uchar
CF_COLOR_G = 0x111  # uchar
CF_COLOR_R = 0x112  # uchar
CF_COLOR_A = 0x113  # uchar
CF_SHADER_TYPE = 0x114  # int
CF_SHADER_COLOR_B = 0x118  # uchar
CF_SHADER_COLOR_G = 0x119  # uchar
CF_SHADER_COLOR_R = 0x11A  # uchar
CF_SHADER_COLOR_A = 0x11B  # uchar
CF_SCALE_X = 0x11C  # float
CF_SCALE_Y = 0x120  # float
CF_Z_ROTATION = 0x12C  # float
CF_CURRENT_SEQ = 0x13C  # short
CF_CURRENT_SUBSEQ = 0x13E  # short
CF_CURRENT_FRAME = 0x140  # short
CF_ELAPSED_IN_FRAME = 0x142  # short
CF_ELAPSED_IN_SUBSEQ = 0x144  # int
CF_CURRENT_FRAME_DATA = 0x158  # ptr
CF_CURRENT_SEQ_FRAMES = 0x15C  # ptr
CF_ENEMY = 0x170  # ptr
CF_CURRENT_HEALTH = 0x184  # short
CF_HIT_STATE = 0x190  # int
CF_HIT_COUNT = 0x194  # char
CF_HIT_STOP = 0x196  # short
CF_ATTACK_BOX_COUNT = 0x1CB  # char
CF_HURT_BOX_COUNT = 0x1CC  # char
CF_HURT_BOXES = 0x1D0  # rect[5]
CF_ATTACK_BOXES = 0x220  # rect[5]
CF_ATTACK_BOXES_ROT = 0x320  # altbox[5]
CF_HURT_BOXES_ROT = 0x334  # altbox[5]
CF_CHARACTER_INDEX = 0x34C  # char
CF_PLAYER_INDEX = 0x350  # char
CF_BULLET_COUNTER = 0x36C  # short
CF_CURRENT_SPIRIT = 0x49E  # short
CF_SPIRIT_REGEN_DELAY = 0x4A2  # short
CF_TIME_STOP = 0x4A8  # short
CF_UNTECH = 0x4BA  # short
CF_DAMAGE_LIMIT = 0x4BE  # short
CF_CARD_SLOTS = 0x5E6  # char
CF_CARDS_ARRAY = 0x5E8  # ptr
CF_SKILL_LEVELS_1 = 0x6A4  # char[32]
CF_SKILL_LEVELS_2 = 0x6C4  # char[32]
CF_OBJ_LIST_MGR = 0x6F8  # ptr
CF_PRESSED_X_AXIS = 0x754  # int
CF_PRESSED_Y_AXIS = 0x758  # int
CF_PRESSED_A = 0x75C  # int
CF_PRESSED_B = 0x760  # int
CF_PRESSED_C = 0x764  # int
CF_PRESSED_D = 0x768  # int
CF_PRESSED_AB = 0x76C  # int
CF_PRESSED_BC = 0x770  # int
CF_PRESSED_X_AXIS1 = 0x774  # int
CF_PRESSED_Y_AXIS1 = 0x778  # int
CF_PRESSED_A_1 = 0x77C  # int
CF_PRESSED_B_1 = 0x780  # int
CF_PRESSED_C_1 = 0x784  # int
CF_PRESSED_D_1 = 0x788  # int
CF_PRESSED_AB_1 = 0x78C  # int
CF_PRESSED_BC_1 = 0x790  # int
CF_PRESSED_COMBINATION = 0x7C8  # int

# PRESSED COMBINATION CODES: (B version, multiply by two for C version)
# 421: 139296
# 214: 32
# 22: 536870912
# 236: 2
# 623: 514

CF_CHARGE_ATTACK = 0x7F4  # char
CF_DAMAGE_LIMITED = 0x7F7  # bool
CF_X_OFFSET = 0x88C  # short
CF_Y_OFFSET = 0x88E  # short
CF_SP_DOLL_COUNT = 0x890  # short
CF_DOLL_COUNT = 0x892  # short

# Projectile class.
PF_IS_ACTIVE = 0x34C  # int
PF_INIT_ARGS = 0x35C  # void *
PF_CUSTOM_FIELD = 0x390  # int
PF_PARENT = 0x398  # void *

# ProjectileManager class.
PMF_OBJ_PROJ_OFS = 0x54  # int

# Frame class.
FF_DAMAGE = 0x1C  # short
FF_SPIRIT_DAMAGE = 0x22  # short
FF_FFLAGS = 0x4C  # int
FF_AFLAGS = 0x50  # int
FF_COLLISION_BOX = 0x54  # rect<short>
FF_HURT_BOX_COUNT = 0x5C  # int
FF_HURT_BOXES = 0x60  # rect<short>
FF_ATTACK_BOX_COUNT = 0x5C  # int
FF_ATTACK_BOXES = 0x60  # rect<short>
FF_STAND = 0x1
FF_CROUCH = 0x2
FF_AIRBORNE = 0x4
FF_DOWN = 0x8
FF_GUARD_AVAILABLE = 0x10
FF_CANCELLEABLE = 0x20
FF_CH_ON_HIT = 0x40
FF_SUPERARMOR = 0x80
FF_EXTENDED_ARMOR = 0x100
FF_GUARD_POINT = 0x200
FF_GRAZE = 0x400
FF_GUARDING = 0x800
FF_GRAB_INVINCIBLE = 0x1000
FF_MELEE_INVINCIBLE = 0x2000
FF_PROJECTILE_INVINCIBLE = 0x4000
FF_INV_AIRBORNE = 0x8000
FF_INV_MID_BLOW = 0x10000
FF_INV_LOW_BLOW = 0x20000
FF_INV_SHOOT = 0x40000
FF_REFLECTION_PROJECTILE = 0x80000
FF_FLIP_VELOCITY = 0x100000
FF_HIGH_JUMP_CANCELLABLE = 0x200000
FF_UNK400000 = 0x400000
FF_UNK800000 = 0x800000
FF_ATK_AS_HIT = 0x1000000

# Attack flags.
AF_MID_HIT = 0x2
AF_LOW_HIT = 0x4
AF_AIR_BLOCKABLE = 0x8
AF_GRAZABLE = 0x400000

hwnd = None
proc = None
g_pbattleMgr = None
processID = None # 一个不可能的进程id
scene = 0 # 场景号
# 获取句柄和进程
def check_memory(address):
    # 定义MEMORY_BASIC_INFORMATION结构体
    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        _fields_ = [
            ('BaseAddress', ctypes.c_void_p),
            ('AllocationBase', ctypes.c_void_p),
            ('AllocationProtect', ctypes.c_ulong),
            ('RegionSize', ctypes.c_size_t),
            ('State', ctypes.c_ulong),
            ('Protect', ctypes.c_ulong),
            ('Type', ctypes.c_ulong),
        ]

    # 定义VirtualQueryEx函数
    VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
    VirtualQueryEx.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION),
                               ctypes.c_size_t]
    VirtualQueryEx.restype = ctypes.c_size_t

    # 检查内存地址范围
    mbi = MEMORY_BASIC_INFORMATION()
    result = VirtualQueryEx(proc, address, ctypes.byref(mbi), ctypes.sizeof(mbi))

    if result == 0:
        print("Failed to query memory information")
    else:
        print("Base address:", mbi.BaseAddress)
        print("Region size:", mbi.RegionSize)


def check_proc():
    """
    检查游戏进程是否正在运行
    return: bool是否运行
    """
    if proc is None:
        return False
    return psutil.pid_exists(processID)


def check_scene():
    """
    返回游戏当前场景号，已知场景值如下：
    0x00: 启动中
    0x01: 开场动画
    0x02: 主菜单
    0x03: 角色选择

    0x05: 本地对战/训练模式/回放

    0x09: 联机对战

    0x10: 章节选择
    0x14: 章节结束
    0x0c: 少女祈祷中
    0x0f: 观战中

    return: uint场景号
    """
    global scene
    buffer = ctypes.c_uint(0)
    bytesRead = ctypes.c_ulong(0)
    ReadProcessMemory(proc, address.SCENEID, ctypes.byref(buffer), 1, ctypes.byref(bytesRead))
    scene = buffer.value
    return scene


def update_proc():
    """
    更新三个全局变量hwnd, proc, processID
    如果游戏进程正在运行或者成功获取游戏句柄，那么返回True，否则返回False
    提供一个检查进程与初始化句柄的函数
    """
    global hwnd, proc, processID
    if check_proc():
        return True
    hwnd = win32gui.FindWindow("th123_110a", None)
    if hwnd:
        hreadID, processID = win32process.GetWindowThreadProcessId(hwnd)
        proc = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, processID)
        print("proc:", proc)
        return True
    else:
        return False


def update_proc_with_pid(pid):
    global proc
    proc = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, pid)


def update_pbattleMgr():
    global g_pbattleMgr
    buffer = ctypes.c_uint(0)
    bytesRead = ctypes.c_ulong(0)
    ReadProcessMemory(proc, address.PBATTLEMGR, ctypes.byref(buffer), 4, ctypes.byref(bytesRead))
    g_pbattleMgr = buffer.value


# 根据基地址加偏移量的形式读取相应属性的值
def get_field(address, offset, type):
    nsize = ctypes.sizeof(type)
    buffer = type(0)
    number_of_bytes_read = ctypes.c_uint(0)
    print(number_of_bytes_read)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))
    return buffer.value


def set_field(address, offset, value, type):
    nsize = ctypes.sizeof(type)
    buffer = ctypes.create_string_buffer(nsize)
    number_of_bytes_read = ctypes.c_uint(0)
    if type == ctypes.c_float:
        buffer.raw = struct.pack('f', value)
    else:
        buffer.raw = value.to_bytes(nsize, byteorder='little')
    WriteProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))


def get_int(address, offset):
    nsize = 4
    buffer = ctypes.c_int(0)
    number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))

    return buffer.value


def get_short(address, offset):
    nsize = 2
    buffer = ctypes.c_short(0)
    number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))

    return buffer.value


def get_float(address, offset):
    nsize = 4
    buffer = ctypes.c_float(0)
    number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))

    return buffer.value


def get_char(address, offset):
    nsize = 1
    buffer = ctypes.c_char(0)
    number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))

    return buffer.value


def get_uchar(address, offset):
    nsize = 1
    buffer = ctypes.c_ubyte(0)
    number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))

    return buffer.value


def get_ptr(address, offset):
    nsize = 4
    buffer = ctypes.c_uint(0)
    number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))

    return buffer.value


def set_int(address, offset, value):
    nsize = 4
    buffer = ctypes.c_int(0)
    buffer.value = value
    number_of_bytes_read = ctypes.c_uint(0)
    WriteProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))


def set_short(address, offset, value):
    nsize = 2
    buffer = ctypes.c_short(0)
    buffer.value = value
    number_of_bytes_read = ctypes.c_uint(0)
    WriteProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))


def set_float(address, offset, value):
    nsize = 4
    buffer = ctypes.c_float(0)
    buffer.value = value
    number_of_bytes_read = ctypes.c_uint(0)
    WriteProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))


def set_char(address, offset, value):
    nsize = 1
    buffer = ctypes.c_char(0)
    buffer.value = value
    number_of_bytes_read = ctypes.c_uint(0)
    WriteProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))


def set_uchar(address, offset, value):
    nsize = 1
    buffer = ctypes.c_ubyte(0)
    buffer.value = value
    number_of_bytes_read = ctypes.c_uint(0)
    WriteProcessMemory(proc, address + offset, ctypes.byref(buffer), nsize, ctypes.byref(number_of_bytes_read))
