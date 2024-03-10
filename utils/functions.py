"""
本模块主要定义了一系列偏移量OFFSET，定义了三个类，分别是Position, Player, PlayerKeys，并提供了获取信息的函数
----------------------------------------
Position类用于存储玩家的位置信息，包含以下属性：
x: x坐标 float
y: y坐标 float
xspeed: x方向速度 float
yspeed: y方向速度 float
gravity: 重力 float
direction: 方向 int 1为向右，255为向左
----------------------------------------
PlayerKeys类用于存储玩家的按键信息，包含以下属性：
keypressed_left: 左键是否按下 bool
keypressed_right: 右键是否按下 bool
keypressed_up: 上键是否按下 bool
keypressed_down: 下键是否按下 bool
keypressed_a: A键（体术）持续按下帧数 int
keypressed_b: B键（轻弹幕）持续按下帧数 int
keypressed_c: C键（重弹幕）持续按下帧数 int
keypressed_d: D键（冲刺）持续按下帧数 int
keypressed_ab: AB键（切卡）暂时未知
keypressed_bc: BC键（使用卡）暂时未知
keypressed_combination: 组合键对应代码 int
# PRESSED COMBINATION CODES: (B version, multiply by two for C version)
# 421: 139296
# 214: 32
# 22: 536870912
# 236: 2
# 623: 514
----------------------------------------
Player类用于存储玩家的信息，包含以下属性：
p: 玩家的地址
index: 玩家的角色编号
x_pressed: x方向的按键状态
y_pressed: y方向的按键状态
position: 玩家的位置信息Position类对象
keymgr_p: 玩家的按键管理器地址
keymap_p: 玩家的按键映射地址
playerkeys: 玩家的按键信息PlayerKeys类对象
framedata: 玩家的帧数据地址
frameflag: 玩家的帧标志
current_sequence: 玩家的当前序列
elapsed_in_subseq: 玩家在当前序列中的时间
health: 玩家的生命值
spirit: 玩家的灵力值
untech: 玩家的untight值
card: 玩家的卡片数量
----------------------------------------
其他函数：
update_position(player): 更新玩家的位置信息
update_keys(player): 更新玩家的按键信息
update_playerinfo(player, add_bmgr_px): 更新玩家的信息， add_bmgr_px为玩家相对于battle manager的偏移量
预计需要的函数：
update_weather()：获取天气信息
...

@Author: zhaiwuz5
"""

import ctypes
import struct
from utils import fields, address
from enum import Enum
from typing import NamedTuple

LEFT_CORNER_P1 = 40.0
LEFT_NEAR_P1 = 340.0
MIDSCREEN_P1 = 600.0
RIGHT_NEAR_P1 = 901.0
RIGHT_CORNER_P1 = 1201.0

LEFT_CORNER_P2 = 79.0
LEFT_NEAR_P2 = 379.0
MIDSCREEN_P2 = 639.0
RIGHT_NEAR_P2 = 940.0
RIGHT_CORNER_P2 = 1240.0

# Very Light - Light - Medium - Heavy (shifted compared to the usual notations)
VERYLIGHT_RB_TIME = 10
LIGHT_RB_TIME = 16
MEDIUM_RB_TIME = 22
HEAVY_RB_TIME = 28
VERYLIGHT_WB_TIME = 12
LIGHT_WB_TIME = 20
MEDIUM_WB_TIME = 28
AIR_B_TIME = 20

GUARDCRUSH = 143
AIR_GUARDCRUSH = 145
STAND_VL_RB = 150
STAND_L_RB = 151
STAND_M_RB = 152
STAND_H_RB = 153
CROUCH_VL_RB = 154
CROUCH_L_RB = 155
CROUCH_M_RB = 156
CROUCH_H_RB = 157
AIRBLOCK = 158
STAND_VL_WB = 159
STAND_L_WB = 160
STAND_M_WB = 161
CROUCH_L_WB = 164
CROUCH_M_WB = 165

FORWARD_TECH = 197
BACKWARD_TECH = 198
NEUTRAL_TECH = 199

# Keymaps of both players
SWRS_ADDR_1PKEYMAP = 0x00898940
SWRS_ADDR_2PKEYMAP = 0x0089912C

# 定义枚举类
class KeymapIndex(Enum):
    up = 0
    down = 1
    left = 2
    right = 3
    A = 4
    B = 5
    C = 6
    D = 7
    sw = 8
    sc = 9

class TechSelect(Enum):
    neutral = 0
    left = 1
    right = 2
    random = 3


class PlayerKeys:
    def __init__(self, keypressed_left, keypressed_right, keypressed_up, keypressed_down, keypressed_a, keypressed_b, keypressed_c, keypressed_d, keypressed_ab, keypressed_bc, keypressed_combination):
        self.keypressed_left = keypressed_left
        self.keypressed_right = keypressed_right
        self.keypressed_up = keypressed_up
        self.keypressed_down = keypressed_down

        self.keypressed_a = keypressed_a
        self.keypressed_b = keypressed_b
        self.keypressed_c = keypressed_c
        self.keypressed_d = keypressed_d
        self.keypressed_ab = keypressed_ab
        self.keypressed_bc = keypressed_bc
        self.keypressed_combination = keypressed_combination

    def __str__(self):
        return f'PlayerKeys(keypressed_left={self.keypressed_left}, keypressed_right={self.keypressed_right}, keypressed_up={self.keypressed_up}, keypressed_down={self.keypressed_down}, keypressed_a={self.keypressed_a}, keypressed_b={self.keypressed_b}, keypressed_c={self.keypressed_c}, keypressed_d={self.keypressed_d}, keypressed_ab={self.keypressed_ab}, keypressed_bc={self.keypressed_bc}, keypressed_combination={self.keypressed_combination})'


class Position:
    def __init__(self, x, y, xspeed, yspeed, gravity, direction):
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.gravity = gravity
        self.direction = direction

    def __str__(self):
        return f'Position(x={self.x}, y={self.y}, xspeed={self.xspeed}, yspeed={self.yspeed}, gravity={self.gravity}, direction={self.direction})'


class Player:
    def __init__(self):
        self.p = None
        self.index = None
        self.x_pressed = None
        self.y_pressed = None
        self.position = None
        self.keymgr_p = None
        self.keymap_p = None
        self.playerkeys = None
        self.framedata = None
        self.frameflag = None
        self.current_sequence = None
        self.elapsed_in_subseq = None
        self.health = None
        self.spirit = None
        self.untech = None
        self.card = None

    def __str__(self):
        return f'Player(p={self.p}, index={self.index}, x_pressed={self.x_pressed}, y_pressed={self.y_pressed}, position={self.position}, framedata={self.framedata}, frameflag={self.frameflag}, current_sequence={self.current_sequence}, elapsed_in_subseq={self.elapsed_in_subseq}, health={self.health}, spirit={self.spirit}, untech={self.untech}, card={self.card})'

    def update_playerinfo(self, add_bmgr_px):
        update_playerinfo(self, add_bmgr_px)


class Keys:
    def __init__(self, reset_pos, save_pos, reset_skills, display_states):
        self.reset_pos = reset_pos
        self.save_pos = save_pos
        self.reset_skills = reset_skills
        self.display_states = display_states


class ToggleKey:
    def __init__(self, reset_pos, save_pos, reset_skills, display_states):
        self.reset_pos = reset_pos
        self.save_pos = save_pos
        self.reset_skills = reset_skills
        self.display_states = display_states


class HeldKey:
    def __init__(self, reset_pos, save_pos, reset_skills, display_states, JOYPADreset_pos, JOYPADsave_pos, JOYPADreset_skills, JOYPADdisplay_states):
        self.reset_pos = reset_pos
        self.save_pos = save_pos
        self.reset_skills = reset_skills
        self.display_states = display_states
        self.JOYPADreset_pos = JOYPADreset_pos
        self.JOYPADsave_pos = JOYPADsave_pos
        self.JOYPADreset_skills = JOYPADreset_skills
        self.JOYPADdisplay_states = JOYPADdisplay_states


class Button:
    def __init__(self, reset_pos, save_pos, reset_skills, display_states):
        self.reset_pos = reset_pos
        self.save_pos = save_pos
        self.reset_skills = reset_skills
        self.display_states = display_states


class MiscState:
    def __init__(self, frame_advantage, blockstring, hjc_advantage, hjc_blockstring, isIdle, untight_nextframe, tech_mode, wakeup_count_p1, wakeup_count_p2):
        self.frame_advantage = frame_advantage
        self.blockstring = blockstring
        self.hjc_advantage = hjc_advantage
        self.hjc_blockstring = hjc_blockstring
        self.isIdle = isIdle
        self.untight_nextframe = untight_nextframe
        self.tech_mode = tech_mode
        self.wakeup_count_p1 = wakeup_count_p1
        self.wakeup_count_p2 = wakeup_count_p2


savestate_keys = Keys(0x00000001, 0x00000002, 0x00000004, 0x00000008)
toggle_keys = ToggleKey(False, False, False, False)
held_keys = HeldKey(False, False, False, False, False, False, False, False)
buttons = Button(0x00000010, 0x00000020, 0x00000040, 0x00000080)
misc_states = MiscState(0, False, 0, False, 0, False, 0, 0, 0)


def update_position(player):
    player.position = Position(
        fields.get_float(player.p, fields.CF_X_POS),
        fields.get_float(player.p, fields.CF_Y_POS),
        fields.get_float(player.p, fields.CF_X_SPEED),
        fields.get_float(player.p, fields.CF_Y_SPEED),
        fields.get_float(player.p, fields.CF_GRAVITY),
        int.from_bytes(fields.get_char(player.p, fields.CF_DIR), byteorder='little')
    )


def update_keys(player):
    # player.playerkeys = PlayerKeys(
    #     fields.get_int(player.keystate, 0) < 0,
    #     fields.get_int(player.keystate, 0) > 0,
    #     fields.get_int(player.keystate, 4) < 0,
    #     fields.get_int(player.keystate, 4) > 0,
    #
    #     fields.get_int(player.keystate, 4 * 2),
    #     fields.get_int(player.keystate, 4 * 3),
    #     fields.get_int(player.keystate, 4 * 4),
    #     fields.get_int(player.keystate, 4 * 5),
    #     fields.get_int(player.keystate, 4 * 6),
    #     fields.get_int(player.keystate, 4 * 7)
    # )
    player.playerkeys = PlayerKeys(
        fields.get_int(player.keymap_p, 0) < 0,
        fields.get_int(player.keymap_p, 0) > 0,
        fields.get_int(player.keymap_p, 4) < 0,
        fields.get_int(player.keymap_p, 4) > 0,

        fields.get_int(player.keymap_p, 4 * 2),
        fields.get_int(player.keymap_p, 4 * 3),
        fields.get_int(player.keymap_p, 4 * 4),
        fields.get_int(player.keymap_p, 4 * 5),
        fields.get_int(player.keymap_p, 4 * 6),
        fields.get_int(player.keymap_p, 4 * 7),
        fields.get_int(player.p, fields.CF_PRESSED_COMBINATION)
    )


# 获取玩家信息的核心函数
def update_playerinfo(player, add_bmgr_px):
    '''
    get the player's information

    :param player: Player Instance
    :param add_bmgr_px: Address OFFSET of the player's battle manager, usually ADDR_BMGR_P1 or ADDR_BMGR_P2
    '''
    player.p = fields.get_ptr(fields.g_pbattleMgr, add_bmgr_px)
    player.keymgr_p = fields.get_ptr(player.p, address.KEYMGROFS)
    player.keymap_p = fields.get_ptr(player.keymgr_p, 0) + address.KEYMAPOFS
    player.index = int.from_bytes(fields.get_char(player.p, fields.CF_CHARACTER_INDEX), byteorder='little')

    player.x_pressed = fields.get_int(player.p, fields.CF_PRESSED_X_AXIS)
    player.y_pressed = fields.get_int(player.p, fields.CF_PRESSED_Y_AXIS)
    update_position(player)
    update_keys(player)

    player.health = fields.get_short(player.p, fields.CF_CURRENT_HEALTH)
    player.spirit = fields.get_short(player.p, fields.CF_CURRENT_SPIRIT)

    player.framedata = fields.get_ptr(player.p, fields.CF_CURRENT_FRAME_DATA)
    player.frameflag = fields.get_int(player.framedata, fields.FF_FFLAGS)
    player.current_sequence = fields.get_short(player.framedata, fields.CF_CURRENT_SEQ)
    player.elapsed_in_subseq = fields.get_short(player.framedata, fields.CF_ELAPSED_IN_SUBSEQ)

    player.card = int.from_bytes(fields.get_char(player.p, fields.CF_CARD_SLOTS), byteorder='little')
    player.untech = fields.get_short(player.p, fields.CF_UNTECH)


def init_pos(custom_x):
    pos = Position(custom_x, 0, 0, 0, 0, 1)
    return pos


custom_pos = init_pos(480.0)
custom_pos2 = init_pos(800.0)
LC_P1 = init_pos(LEFT_CORNER_P1)
LC_P2 = init_pos(LEFT_CORNER_P2)
LN_P1 = init_pos(LEFT_NEAR_P1)
LN_P2 = init_pos(LEFT_NEAR_P2)
MID_P1 = init_pos(MIDSCREEN_P1)
MID_P2 = init_pos(MIDSCREEN_P2)
RN_P1 = init_pos(RIGHT_NEAR_P1)
RN_P2 = init_pos(RIGHT_NEAR_P2)
RC_P1 = init_pos(RIGHT_CORNER_P1)
RC_P2 = init_pos(RIGHT_CORNER_P2)


def save_checkpoint(player):
    pos = Position()
    pos.x = player.position.x
    pos.y = player.position.y
    pos.xspeed = player.position.xspeed
    pos.yspeed = player.position.yspeed
    pos.gravity = player.position.gravity
    return pos
