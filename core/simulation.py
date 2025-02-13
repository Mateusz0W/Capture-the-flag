import random
from game.map import Map
from game.player import Player
from config import GameConfig
from game.flag import Flag

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

    def next_step(self,action,direction):
        #actions=['move','build']
        #weights=[.9,.1]
        #direction=['up','down','left','right','None']
        for player in self.players:
        #   action=random.choices(actions,weights,k=1)[0]
            if action == 'build':
               player.build(direction,self.map)
            else:
               player.move(random.choice(direction),self.map)
        
            player.captured_the_flag(self.flags)

    def __end_game(self):
        for flag in self.flags:
            if flag.in_opponent_base():
                self.__add_point(flag)
                self.game_over=True

    def run(self,action,direction):
        self.next_step(action,direction)
        self.map.update(self.players,self.flags)
        #self.__end_game()
        

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

    def reward(self,team):
        reward=0
       
        for player in self.players:
            # reward for capturing enemy flag
            if  player.has_a_flag and player.team == team:
                reward += 10
            # reward for the loss of the flag
            elif player.has_a_flag and player.team != team:
                reward -= 10
        
        #reward for deliver flag to the base
        for flag in self.flags:
            if flag.in_opponent_base() and flag.team == team:
                reward += 20
            elif flag.in_opponent_base() and flag.team != team:
                reward -= 20

        return reward
                

