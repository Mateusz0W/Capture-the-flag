import torch
import gym
import gym_environment
import numpy as np
from machine_learning.dqn_model import DQN

if __name__=="__main__":
    env=gym.make('gym_environment/Capture-the-flag-v0',render_mode='human')
    state,_=env.reset()
    
    device = torch.device("cpu")
    net =DQN(env.observation_space.shape[0],env.action_space.n).to(device)
    net.load_state_dict(torch.load("machine_learning/models/Best_model.dat",map_location=device))
    print('Model loaded')
    net.eval()

    total_reward = 0
    done = False
    while True:
        state_a = np.array([state], copy=False)
        state_v = torch.tensor(state_a,dtype=torch.float32).to(device)
        q_vals_v = net(state_v)
        _, act_v = torch.max(q_vals_v, dim=1)
        action = int(act_v.item())
        

        new_state, reward, done, _, _ = env.step(action)
        total_reward += reward

        if done:
            state,_=env.reset()
        else:

            state = new_state
        print(total_reward)
    
    