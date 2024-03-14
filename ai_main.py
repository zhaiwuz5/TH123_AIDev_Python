from utils import functions, fields, replay_to_data, keymanager
from model import TD3
import time
from pywinauto.application import Application


ADDR_BMGR_P1 = 0x0C
ADDR_BMGR_P2 = 0x10

th123_exe_path = r"D:\非想天则资源-为什么你要用度盘下载？\【2-27 完整游戏】非想天则-新则整合包\th123\th123.exe"
if not fields.update_proc():
    app = Application().start(th123_exe_path)
    win = app.top_window()

else:
    app = Application().connect(path=th123_exe_path)
    win = app.top_window()

win.set_focus()
keymgr = keymanager.KeyManager(win)
player1 = functions.Player()
player2 = functions.Player()
# agent_p1 = TD3.TD3(20, 11, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 11])
# agent_p1.load()
agent_p2 = TD3.TD3(20, 11, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 11])
agent_p2.load()

while fields.update_proc():
    previous_scene = None
    fields.check_scene()
    if fields.scene != previous_scene:
        # print(fields.scene)
        previous_scene = fields.scene

        # if fields.scene == 0:
        #     print('启动中')
        #
        # if fields.scene == 1:
        #     print('标题画面')
        #
        # if fields.scene == 2:
        #     print('模式选择')
        #
        # if fields.scene == 3:
        #     print('人物选择')

        while fields.check_scene() == 5:
            fields.update_pbattleMgr()
            player1.update_playerinfo(ADDR_BMGR_P1)
            player2.update_playerinfo(ADDR_BMGR_P2)
            frame = replay_to_data.to_dict(player1, player2)
            # print(frame)
            state = replay_to_data.transform_to_input(frame)
            action = agent_p2.select_action(state)
            keymgr.sendkeys(action, frame['p2_dir'])
            time.sleep(1 / 30)

    # 每两帧检查一次
    time.sleep(1 / 30)



