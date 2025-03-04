import random
from game.map import Map
from game.player import Player
from config import GameConfig
from game.flag import Flag
import numpy as np

class Simulation:
    def __init__(self):
        self.map=Map()
        self.players=[
            Player(color,self.map)
            for color in ('Blue','Red')
            for _ in range(GameConfig.players_in_team)
        ]
        self.flags=[Flag(position,'Blue' if not index else 'Red' ) for index,position in enumerate(self.map.flags_positions)]     
        self.teams_points={
            "Blue": 0,
            "Red": 0
        }
        self.game_over=False

        self.team_captured_flag={
            "Blue": False,
            "Red": False,
        }

        self.rewards=np.zeros(GameConfig.players_in_team)

    def next_step(self,action,direction,team,idx):
        if team == 'Red':
            idx=GameConfig.players_in_team + idx
        
        if action == 'build':
            self.players[idx].build(direction,self.map)
        else:
            self.players[idx].move(direction,self.map)
            
        self.players[idx].captured_the_flag(self.flags)

    def __end_game(self):
        for flag in self.flags:
            if flag.in_opponent_base():
                self.__add_point(flag)
                self.game_over=True

    def run(self,action,direction,team,player_idx):
        self.next_step(action,direction,team,player_idx)
        self.map.update(self.players,self.flags)
        self.__end_game()
        

    def __add_point(self,flag):
        team = 'Blue' if flag.team =='Red' else 'Red'
        self.teams_points[team]+=1

    def reset(self):
        self.map.reset()
        for player in self.players:
            player.reset(self.map)
        for idx , flag in enumerate(self.flags):
            flag.reset(self.map.flags_positions[idx])
        self.game_over=False
        #reawrds
        for team in self.team_captured_flag:
            self.team_captured_flag[team] = False
        
        self.rewards=np.zeros(GameConfig.players_in_team)

    def reward(self,team,idx):
        if team == 'Red':
            idx=GameConfig.players_in_team + idx
        reward=0
        distance_to_flag = lambda player,flag: abs(flag.x-player.x)+abs(flag.y-player.y)
        flags={
            "Red": self.flags[0],
            "Blue": self.flags[1],
        }
        
        if self.players[idx].has_a_flag and self.players[idx].team == team and not self.team_captured_flag[team]:
            reward += 30
            self.team_captured_flag[team]=True
            self.players[idx].last_distances_to_flag.clear()

        if not self.team_captured_flag[team] and self.players[idx].team == team:
            dist = distance_to_flag(self.players[idx],flags[team])
            if len(self.players[idx].last_distances_to_flag) == self.players[idx].last_distances_to_flag.maxlen:
                if dist < self.players[idx].last_distances_to_flag[-1]:
                    r = max(0.3,2-0.1*dist) if dist != 0 else 2
                else:
                    r = -2
                reward += r
            self.players[idx].last_distances_to_flag.append(dist)
                
        elif self.team_captured_flag[team] and self.players[idx].team == team:
            dist = distance_to_flag(self.players[idx],flags["Blue"])
            if len(self.players[idx].last_distances_to_flag) == self.players[idx].last_distances_to_flag.maxlen:
                if dist < self.players[idx].last_distances_to_flag[-1]:
                    r = max(0.2,3-0.2*dist)+1 if dist != 0 else 2
                else:
                    r = -2
                reward += r
            self.players[idx].last_distances_to_flag.append(dist)

        if len(set(self.players[idx].last_distances_to_flag)) <= 2 and self.players[idx].team==team:
            reward -=3

        #reward for deliver flag to the base
        for flag in self.flags:
            if flag.in_opponent_base() and flag.team == team:
                reward -= 40
            elif flag.in_opponent_base() and flag.team != team:
                reward += 40

        self.rewards[idx-4]=reward
        return float(sum(self.rewards))
                
