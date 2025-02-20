import torch.optim as optim
from  tensorboardX import SummaryWriter
import gym
import matplotlib.pyplot as plt
from datetime import datetime

from collections import namedtuple,deque
import numpy as np
import torch
import torch.nn as nn
import time
import random

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dqn_model import DQN
from config import MLConfig
import gym_environment

def plot(rewards,frames):
    plt.plot(frames,rewards)
    plt.xlabel("Train steps")
    plt.ylabel("Reward")
    plt.title("learning process")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("plots", exist_ok=True) 
    plt.savefig(f"plots/learnign_result_{timestamp}.png")
    print("saved plot")

Experience = namedtuple('Experience',
                        field_names=['state','action','next_state','done','reward'])

class ReplayBuffer:
    def __init__(self,capacity):
        self.buffer = deque([],maxlen=capacity)

    def push(self, experience):
        self.buffer.append(experience)

    def sample(self,batch_size):
        return random.sample(self.buffer,batch_size)
    def __len__(self):
        return len(self.buffer)

class Agent:
    def __init__(self,env,buffer):
        self.env=env
        self.buffer=buffer
        self.__reset()

    def __reset(self):
        self.state, _=self.env.reset()
        self.total_reward=0.0

    @torch.no_grad()
    def play_step(self,net,epsilon=0.0,device="cpu"):
        done_reward=None

        if np.random.random() < epsilon:
            action =self.env.action_space.sample()
        else:
            state_a = np.array([self.state], copy=False)
            state_v = torch.tensor(state_a,dtype=torch.float32).to(device)
            q_vals_v = net(state_v)
            _, act_v = torch.max(q_vals_v, dim=1)
            action = int(act_v.item())
        
        new_state, reward, done, _, info = self.env.step(action)
        self.total_reward += reward
        exp = Experience(self.state, action, reward,done, new_state)
        self.buffer.push(exp)
        self.state = new_state
        if done:
            done_reward =self.total_reward
            self.__reset()
        return done_reward
    
def calc_loss(batch, net, tgt_net, device="cpu"):
    states, actions, rewards, dones, next_states = zip(*batch)
    states_v = torch.tensor(np.array(states, copy=False)).to(device)
    next_states_v = torch.tensor(np.array(next_states, copy=False)).to(device)
    actions_v = torch.tensor(actions).to(device)
    rewards_v = torch.tensor(rewards).to(device)
    done_mask = torch.BoolTensor(dones).to(device)

    state_action_values = net(states_v).gather(1, actions_v.unsqueeze(-1)).squeeze(-1)
    next_state_values = tgt_net(next_states_v).max(1)[0]
    next_state_values[done_mask] = 0.0
    next_state_values = next_state_values.detach()

    expected_state_action_values = next_state_values * MLConfig.GAMMA + rewards_v
    return nn.MSELoss()(state_action_values,expected_state_action_values)
    

if __name__ == "__main__":
    env_name="Capture-the-flag"
    device = torch.device("cpu")
    env = gym.make('gym_environment/Capture-the-flag-v0')
    net = DQN(env.observation_space.shape[0],env.action_space.n).to(device)
    target_net = DQN(env.observation_space.shape[0],env.action_space.n).to(device)

    writer= SummaryWriter(comment=env_name)
    print(net)
    buffer=ReplayBuffer(MLConfig.REPLAY_SIZE)
    agent=Agent(env,buffer)
    epsilon=MLConfig.EPSILON_START
    optimizer = optim.Adam(net.parameters(), lr=MLConfig.LEARNING_RATE)
    total_rewards = []
    frames=[]
    frame_idx = 0
    ts_frame = 0
    ts=time.time()
    best_mean_reward= None
    while True:
        frame_idx+=1
        epsilon=max(MLConfig.EPSILON_FINAL,MLConfig.EPSILON_START-frame_idx/MLConfig.EPSILON_DECAY_LAST_FRAME)
        reward=agent.play_step(net,epsilon,device)
        if reward is not None:
            frames.append(frame_idx)
            total_rewards.append(reward)
            speed = (frame_idx-ts_frame)/(time.time()-ts)
            ts_frame=frame_idx
            m_reward= np.mean(total_rewards[-100:])
            print(f"\r{frame_idx}: done {len(total_rewards)} games, reward {m_reward:.3f}, eps {epsilon:.2f}, speed {speed:.2f} f/s", end="", flush=True)
            writer.add_scalar("epsilon", epsilon, frame_idx)
            writer.add_scalar("speed", speed, frame_idx)
            writer.add_scalar("reward_100", m_reward, frame_idx)
            writer.add_scalar("reward", reward, frame_idx)
            if best_mean_reward is None or best_mean_reward <m_reward:
                torch.save(net.state_dict(),"models/"+env_name+"-best_%.0f.dat" % m_reward)
                if best_mean_reward is not None:
                    print("\nBest reward updated %.3f -> %.3f" % (best_mean_reward, m_reward))
                best_mean_reward = m_reward
            if m_reward >MLConfig.MEAN_REWARD_BOUND:
                torch.save(net.state_dict(),"models/Best_model.dat")
                print("Solved in %d frames!" % frame_idx)
                plot(total_rewards,frames)
                break
            
        if len(buffer) < MLConfig.REPLAY_START_SIZE:
            continue

        if frame_idx % MLConfig.SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())
            
        optimizer.zero_grad()
        batch = buffer.sample(MLConfig.BATCH_SIZE)
        loss_t = calc_loss(batch, net, target_net, device=device)
        loss_t.backward()
        optimizer.step()