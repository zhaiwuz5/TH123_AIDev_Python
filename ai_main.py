from utils import functions, fields, replay_to_data, keymanager
from model import TD3
import time
from pywinauto.application import Application
import pywinauto.keyboard as keyboard

ADDR_BMGR_P1 = 0x0C
ADDR_BMGR_P2 = 0x10

th123_exe_path = r"D:\非想天则资源-为什么你要用度盘下载？\【2-27 完整游戏】非想天则-新则整合包\th123\th123.exe"
pre_model_path = r"./pre_model_pths/"
model_path = r"./model_pths/"
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
agent_p1 = TD3.TD3(20, 11, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10])
agent_p1.load(pre_model_path)
agent_p2 = TD3.TD3(20, 11, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10])
agent_p2.load(model_path)

while fields.update_proc():
    previous_scene = None
    previous_state = [4.80e+02, 0.00e+00, 0.00e+00, 0.00e+00, 0.00e+00, 1.00e+00, 1.00e+04, 1.00e+03,
                      0.00e+00, 0.00e+00, 8.00e+02, 0.00e+00, 0.00e+00, 0.00e+00, 0.00e+00, 2.55e+02,
                      1.00e+04, 1.00e+03, 0.00e+00, 0.00e+00]  # 上一个对局状态
    previous_action_p1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 上一个对局动作
    previous_action_p2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 上一个对局动作
    previous_reward_p1 = 0  # 上一个对局奖励
    previous_reward_p2 = 0  # 上一个对局奖励
    i = 0 # 记录次数
    ep_r_p1 = 0  # 对局奖励
    ep_r_p2 = 0  # 对局奖励
    fields.check_scene()
    if fields.scene != previous_scene:
        print(fields.scene)
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
        if fields.scene == 3:
            print('人物选择')
            time.sleep(1)
            keyboard.send_keys('Z')
            time.sleep(1)
            keyboard.send_keys('Z')
            time.sleep(1)
            keyboard.send_keys('z')
            time.sleep(1)
            keyboard.send_keys('z')
            time.sleep(1)
            keyboard.send_keys('z')
            time.sleep(1)



        while fields.check_scene() == 5:
            fields.update_pbattleMgr()
            player1.update_playerinfo(ADDR_BMGR_P1)
            player2.update_playerinfo(ADDR_BMGR_P2)
            frame = replay_to_data.to_dict(player1, player2)
            # print(frame)
            state = replay_to_data.get_state(frame)
            reward_p1 = frame['p1_hp'] - frame['p2_hp']
            reward_p2 = frame['p2_hp'] - frame['p1_hp']
            done = float((frame['p1_hp'] <= 0) | (frame['p2_hp'] <= 0))
            action_p1 = agent_p1.select_action(state)
            action_p2 = agent_p2.select_action(state)
            agent_p1.memory.push((previous_state, state, previous_action_p1, previous_reward_p1, done))
            agent_p2.memory.push((previous_state, state, previous_action_p2, previous_reward_p2, done))
            if (i + 1) % 10 == 0:
                print('Episode {},  The memory size is {} '.format(i, len(agent_p2.memory.storage)))
            if len(agent_p2.memory.storage) >= 500 - 1:
                agent_p1.update(10)
                agent_p2.update(10)

            if done:
                if i % 50 == 0:
                    print("Ep_i \t{}, the ep_r is \t{:0.2f}, the step is \t{}".format(i, ep_r_p1, 1))
                ep_r_p1 = 0
                ep_r_p2 = 0
                break
            if i % 500 == 0:
                agent_p1.save(pre_model_path)
                agent_p2.save(model_path)

            previous_state = state
            previous_action_p2 = action_p2
            previous_reward_p2 = reward_p2
            ep_r_p1 += reward_p1
            ep_r_p2 += reward_p2
            i += 1
            keymgr.sendkeys(1, action_p1, frame['p1_dir'])
            keymgr.sendkeys(2, action_p2, frame['p2_dir'])
            time.sleep(1 / 30)

    # 每两帧检查一次
    time.sleep(1 / 5)
