import torch
from torch.utils.data import Dataset, DataLoader
import argparse
from model import TD3
import pandas as pd
import numpy as np

device = 'cuda' if torch.cuda.is_available() else 'cpu'
parser = argparse.ArgumentParser()

parser.add_argument('--mode', default='train', type=str) # mode = 'train' or 'test'
parser.add_argument("--env_name", default="Pendulum-v0")  # OpenAI gym environment name， BipedalWalker-v2
parser.add_argument('--tau',  default=0.005, type=float) # target smoothing coefficient
parser.add_argument('--target_update_interval', default=1, type=int)
parser.add_argument('--iteration', default=5, type=int)

parser.add_argument('--learning_rate', default=3e-4, type=float)
parser.add_argument('--gamma', default=0.99, type=int) # discounted factor
parser.add_argument('--capacity', default=50000, type=int) # replay buffer size
parser.add_argument('--num_iteration', default=100000, type=int) #  num of  games
parser.add_argument('--batch_size', default=100, type=int) # mini batch size
parser.add_argument('--seed', default=1, type=int)

# optional parameters
parser.add_argument('--num_hidden_layers', default=2, type=int)
parser.add_argument('--sample_frequency', default=256, type=int)
parser.add_argument('--activation', default='Relu', type=str)
parser.add_argument('--render', default=False, type=bool) # show UI or not
parser.add_argument('--log_interval', default=50, type=int) #
parser.add_argument('--load', default=False, type=bool) # load model
parser.add_argument('--render_interval', default=100, type=int) # after render_interval, the env.render() will work
parser.add_argument('--policy_noise', default=0.2, type=float)
parser.add_argument('--noise_clip', default=0.5, type=float)
parser.add_argument('--policy_delay', default=2, type=int)
parser.add_argument('--exploration_noise', default=0.1, type=float)
parser.add_argument('--max_episode', default=2000, type=int)
parser.add_argument('--print_log', default=5, type=int)
args = parser.parse_args()


# 定义数据集
class FightingGameDataset(Dataset):
    def __init__(self, csv_file):
        self.dataframe = pd.read_csv(csv_file)
        # print(self.dataframe['p1_comb'].unique())
        # 将所有动作操作转换为从0开始的整数
        self.dataframe['p1_left'] = self.dataframe['p1_left'].astype(int)
        self.dataframe['p1_right'] = self.dataframe['p1_right'].astype(int)
        self.dataframe['p1_up'] = self.dataframe['p1_up'].astype(int)
        self.dataframe['p1_down'] = self.dataframe['p1_down'].astype(int)

        self.dataframe['p2_left'] = self.dataframe['p2_left'].astype(int)
        self.dataframe['p2_right'] = self.dataframe['p2_right'].astype(int)
        self.dataframe['p2_up'] = self.dataframe['p2_up'].astype(int)
        self.dataframe['p2_down'] = self.dataframe['p2_down'].astype(int)

        self.dataframe.loc[self.dataframe['p1_a'] > 0, 'p1_a'] = 1
        self.dataframe.loc[self.dataframe['p1_b'] > 0, 'p1_b'] = 1
        self.dataframe.loc[self.dataframe['p1_c'] > 0, 'p1_c'] = 1
        self.dataframe.loc[self.dataframe['p1_d'] > 0, 'p1_d'] = 1
        self.dataframe.loc[self.dataframe['p1_ab'] > 0, 'p1_ab'] = 1
        self.dataframe.loc[self.dataframe['p1_bc'] > 0, 'p1_bc'] = 1

        self.dataframe.loc[self.dataframe['p2_a'] > 0, 'p2_a'] = 1
        self.dataframe.loc[self.dataframe['p2_b'] > 0, 'p2_b'] = 1
        self.dataframe.loc[self.dataframe['p2_c'] > 0, 'p2_c'] = 1
        self.dataframe.loc[self.dataframe['p2_d'] > 0, 'p2_d'] = 1
        self.dataframe.loc[self.dataframe['p2_ab'] > 0, 'p2_ab'] = 1
        self.dataframe.loc[self.dataframe['p2_bc'] > 0, 'p2_bc'] = 1

        self.dataframe.loc[self.dataframe['p1_comb'] == 139296, 'p1_comb'] = 1
        self.dataframe.loc[self.dataframe['p1_comb'] == 139296*2, 'p1_comb'] = 2
        self.dataframe.loc[self.dataframe['p1_comb'] == 32, 'p1_comb'] = 3
        self.dataframe.loc[self.dataframe['p1_comb'] == 32*2, 'p1_comb'] = 4
        self.dataframe.loc[self.dataframe['p1_comb'] == 536870912, 'p1_comb'] = 5
        self.dataframe.loc[self.dataframe['p1_comb'] == 536870912*2, 'p1_comb'] = 6
        self.dataframe.loc[self.dataframe['p1_comb'] == 2, 'p1_comb'] = 7
        self.dataframe.loc[self.dataframe['p1_comb'] == 2*2, 'p1_comb'] = 8
        self.dataframe.loc[self.dataframe['p1_comb'] == 514, 'p1_comb'] = 9
        self.dataframe.loc[self.dataframe['p1_comb'] == 514*2, 'p1_comb'] = 10

        self.dataframe.loc[self.dataframe['p2_comb'] == 139296, 'p2_comb'] = 1
        self.dataframe.loc[self.dataframe['p2_comb'] == 139296*2, 'p2_comb'] = 2
        self.dataframe.loc[self.dataframe['p2_comb'] == 32, 'p2_comb'] = 3
        self.dataframe.loc[self.dataframe['p2_comb'] == 32*2, 'p2_comb'] = 4
        self.dataframe.loc[self.dataframe['p2_comb'] == 536870912, 'p2_comb'] = 5
        self.dataframe.loc[self.dataframe['p2_comb'] == 536870912*2, 'p2_comb'] = 6
        self.dataframe.loc[self.dataframe['p2_comb'] == 2, 'p2_comb'] = 7
        self.dataframe.loc[self.dataframe['p2_comb'] == 2*2, 'p2_comb'] = 8
        self.dataframe.loc[self.dataframe['p2_comb'] == 514, 'p2_comb'] = 9
        self.dataframe.loc[self.dataframe['p2_comb'] == 514*2, 'p2_comb'] = 10

        # 构建奖励参数和结束标志
        self.dataframe['reward'] = self.dataframe['p1_hp'] - self.dataframe['p2_hp']
        self.dataframe['done'] = (self.dataframe['p1_hp'] <= 0) | (self.dataframe['p2_hp'] <= 0).astype(int)

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        state = row[['p1_x', 'p1_y', 'p1_x_speed', 'p1_y_speed', 'p1_gravity', 'p1_dir', 'p1_hp', 'p1_spirit', 'p1_untech', 'p1_card',
                     'p2_x', 'p2_y', 'p2_x_speed', 'p2_y_speed', 'p2_gravity', 'p2_dir', 'p2_hp', 'p2_spirit', 'p2_untech', 'p2_card']].values
        action = row[['p1_left', 'p1_right', 'p1_up', 'p1_down', 'p1_a', 'p1_b', 'p1_c', 'p1_d', 'p1_ab', 'p1_bc', 'p1_comb']].values
        reward = row['reward']
        done = row['done']
        return state, action, reward, done


# 创建数据集和数据加载器x
dataset = FightingGameDataset('replay_csv/test1.csv')
# 所有可能出现的动作数量
max_action = torch.tensor([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 11]).to(device)
state, action, reward, done = dataset[0]
state_dim = state.shape[0]
action_dim = action.shape[0]


agent = TD3.TD3(state_dim, action_dim, max_action)
ep_r = 0

for i in range(args.num_iteration):
    state, action, reward, done = dataset[0]
    for t in range(len(dataset)):
        state = state.astype(np.float32)
        # 如果是实时训练，那么就使用agent的选择动作
        # action = agent.select_action(state)
        # action = action + np.random.normal(0, args.exploration_noise, size=action.shape)

        action = action.astype(np.float32)
        # 下一个状态
        next_state, next_action, reward, done = dataset[t + 1]
        next_state = next_state.astype(np.float32)
        ep_r += reward

        agent.memory.push((state, next_state, action, reward, np.float32(done)))
        if i + 1 % 10 == 0:
            print('Episode {},  The memory size is {} '.format(i, len(agent.memory.storage)))
        if len(agent.memory.storage) >= args.capacity - 1:
            agent.update(10)

        state = next_state
        if done or t == args.max_episode - 1:

            if i % args.print_log == 0:
                print("Ep_i \t{}, the ep_r is \t{:0.2f}, the step is \t{}".format(i, ep_r, t))
            ep_r = 0
            break

    if i % args.log_interval == 0:
        agent.save()