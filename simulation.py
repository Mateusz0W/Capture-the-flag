import random
from map import Map
from player import Player
from config import GameConfig

class Simulation:
    def __init__(self):
        self.map=Map()
        self.players=[
            Player(color,self.map)
            for color in ('Blue','Red')
            for _ in range(GameConfig.players_in_team)
        ]     
    
    def next_step(self):
        movement=['up','down','left','right','None']
        for player in self.players:
            player.move(random.choice(movement),self.map)

    def run(self):
        self.next_step()
        self.map.update(self.players)
