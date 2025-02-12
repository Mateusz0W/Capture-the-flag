import random
from map import Map
from player import Player
from config import GameConfig
from flag import Flag

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

    def __next_step(self):
        actions=['move','build']
        weights=[.9,.1]
        direction=['up','down','left','right','None']
        for player in self.players:
            action=random.choices(actions,weights,k=1)[0]
            if action == 'build':
                player.build(random.choice(direction),self.map)
            else:
                player.move(random.choice(direction),self.map)

            player.captured_the_flag(self.flags)

    def __end_game(self):
        for flag in self.flags:
            if flag.in_opponent_base():
                self.__add_point(flag)
                self.__reset()

    def run(self):
        self.__next_step()
        self.map.update(self.players,self.flags)
        self.__end_game()
        

    def __add_point(self,flag):
        team = 'Blue' if flag.team =='Red' else 'Red'
        self.teams_points[team]+=1

    def __reset(self):
        self.map.reset()
        for player in self.players:
            player.reset(self.map)
        for idx , flag in enumerate(self.flags):
            flag.reset(self.map.flags_positions[idx])
