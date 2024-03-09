"""
一些项目代码示范
"""


from utils import functions, fields, replay_to_data
import time
import pandas as pd


ADDR_BMGR_P1 = 0x0C
ADDR_BMGR_P2 = 0x10

if fields.update_proc():
    while fields.check_scene() == 5:
        fields.update_pbattleMgr()
        player1 = functions.Player()
        player2 = functions.Player()
        functions.update_playerinfo(player1, ADDR_BMGR_P1)
        functions.update_playerinfo(player2, ADDR_BMGR_P2)
        frame = replay_to_data.to_dict(player1, player2)
        df_frame = pd.DataFrame([frame])
        with open(r"./replay_csv/test.csv", "a") as f:
            df_frame.to_csv(f, header=f.tell() == 0, index=False)
        time.sleep(1 / 30)
    print("Battle Ended")
else:
    print("Process Not Found")

# replay_to_data.to_csv(r"./replay_csv/test.csv")
