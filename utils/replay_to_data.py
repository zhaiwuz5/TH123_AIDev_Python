"""
此模块用于记录本地战斗的数据帧，并保存至csv文件
to_dict(player1, player2) -> dict:
    将两位玩家的信息转换为字典格式
to_csv(csv_path: str):
    将两位玩家的信息转换为字典格式，并保存至csv文件
    csv_path: 保存的csv文件路径
    请先启动游戏并进行本地战斗，再运行此函数

预计进行的优化：
to_csv(csv_path: str)实现一个监视主进程的方法，当游戏启动的时候唤醒，并在游戏结束后自动停止，将csv文件保存为以时间命名的文件
"""


from utils import functions, fields
import time
import json
import pandas as pd
import numpy as np


ADDR_BMGR_P1 = 0x0C
ADDR_BMGR_P2 = 0x10


def to_dict(player1, player2):
    return {
        "p1_x": player1.position.x,
        "p1_y": player1.position.y,
        "p1_x_speed": player1.position.xspeed,
        "p1_y_speed": player1.position.yspeed,
        "p1_gravity": player1.position.gravity,
        "p1_dir": player1.position.direction,

        "p1_left": player1.playerkeys.keypressed_left,
        "p1_right": player1.playerkeys.keypressed_right,
        "p1_up": player1.playerkeys.keypressed_up,
        "p1_down": player1.playerkeys.keypressed_down,
        "p1_a": player1.playerkeys.keypressed_a,
        "p1_b": player1.playerkeys.keypressed_b,
        "p1_c": player1.playerkeys.keypressed_c,
        "p1_d": player1.playerkeys.keypressed_d,
        "p1_ab": player1.playerkeys.keypressed_ab,
        "p1_bc": player1.playerkeys.keypressed_bc,
        "p1_comb": player1.playerkeys.keypressed_combination,

        "p1_hp": player1.health,
        "p1_spirit": player1.spirit,
        "p1_untech": player1.untech,
        "p1_card": player1.card,

        "p2_x": player2.position.x,
        "p2_y": player2.position.y,
        "p2_x_speed": player2.position.xspeed,
        "p2_y_speed": player2.position.yspeed,
        "p2_gravity": player2.position.gravity,
        "p2_dir": player2.position.direction,

        "p2_left": player2.playerkeys.keypressed_left,
        "p2_right": player2.playerkeys.keypressed_right,
        "p2_up": player2.playerkeys.keypressed_up,
        "p2_down": player2.playerkeys.keypressed_down,
        "p2_a": player2.playerkeys.keypressed_a,
        "p2_b": player2.playerkeys.keypressed_b,
        "p2_c": player2.playerkeys.keypressed_c,
        "p2_d": player2.playerkeys.keypressed_d,
        "p2_ab": player2.playerkeys.keypressed_ab,
        "p2_bc": player2.playerkeys.keypressed_bc,
        "p2_comb": player2.playerkeys.keypressed_combination,

        "p2_hp": player2.health,
        "p2_spirit": player2.spirit,
        "p2_untech": player2.untech,
        "p2_card": player2.card
    }


def get_state(frame):
    state = [frame['p1_x'], frame['p1_y'], frame['p1_x_speed'], frame['p1_y_speed'], frame['p1_gravity'], frame['p1_dir'], frame['p1_hp'], frame['p1_spirit'], frame['p1_untech'], frame['p1_card'],
             frame['p2_x'], frame['p2_y'], frame['p2_x_speed'], frame['p2_y_speed'], frame['p2_gravity'], frame['p2_dir'], frame['p2_hp'], frame['p2_spirit'], frame['p2_untech'], frame['p2_card']]
    return np.array(state)


def to_csv(csv_path):
    # TODO - 需要一个监视主进程的方法，在游戏启动的时候唤醒
    if fields.update_proc():
        while fields.check_scene() == 0x05 or fields.check_scene() == 0x09:
            fields.update_pbattleMgr()
            player1 = functions.Player()
            player2 = functions.Player()
            player1.update_playerinfo(ADDR_BMGR_P1)
            player2.update_playerinfo(ADDR_BMGR_P2)
            frame = to_dict(player1, player2)
            df_frame = pd.DataFrame([frame])
            with open(csv_path, "a") as f:
                df_frame.to_csv(f, header=f.tell() == 0, index=False)
            time.sleep(1 / 30)
        print("Battle Ended")
    else:
        print("Process Not Found")
