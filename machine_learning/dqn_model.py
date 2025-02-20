import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self,n_observations,n_actions):
        super(DQN,self).__init__()
        self.input_layer= nn.Linear(n_observations,128)
        self.hidden_layer=nn.Linear(128,128)
        self.output_layer=nn.Linear(128,n_actions)

    def forward(self,x):
        x=F.relu(self.input_layer(x))
        x=F.relu(self.hidden_layer(x))
        return self.output_layer(x)