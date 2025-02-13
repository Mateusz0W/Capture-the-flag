import gym
from gym.spaces import Discrete, Box
import numpy as np
from config import MapConfig
from core.simulation import Simulation
from core.renderer import Renderer

class Environment(gym.Env):
    metadata={"render_modes": ["human"]}

    def __init__(self,render_mode=None):
        self.simulation=Simulation()
        self.renderer=Renderer(self.simulation)

        self.observation_space=Box(low=-6, high=6,shape=(MapConfig.grid_y,MapConfig.grid_x),dtype=np.int32)
        
        # move : up, down, left, right
        # build : up, down, left, right
        # do_nothing
        self.action_space = Discrete(9)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def __get_obs(self):
        return self.simulation.map.grid
    
    def __get_info(self):
        # returns flag locations
        return {
            "Blue flag": (self.simulation.flags[0].x,self.simulation.flags[0].y),
            "Red flag": (self.simulation.flags[1].x,self.simulation.flags[1].y)
        }
    
    def reset(self,seed=None, options=None):
        super().reset(seed=seed)

        self.simulation.reset()
        observation = self.__get_obs()
        info = self.__get_info()
        
        return observation, info
    
    def __map_actions(self,action):
        if action == 0:
            return "move", "up"
        elif action == 1:
            return "move", "down"
        elif action == 2:
            return "move", "left"
        elif action == 3:
            return "move", "right"
        elif action == 4:
            return "build", "up"
        elif action == 5:
            return "build", "down"
        elif action == 6:
            return "build", "left"
        elif action == 7:
            return "build", "right"
        elif action == 8:
            return "do nothing", "do nothing"
        
    def step(self,action):
        action, direction = self.__map_actions(action)
        self.simulation.run(action,direction)
        done = self.simulation.game_over
        reward = self.simulation.reward('Red')
        observation = self.__get_obs()
        info = self.__get_info()

        if self.render_mode == 'human':
            self.renderer.render_frame()

        return observation, reward, done, False, info

 