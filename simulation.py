from map import Map
from player import Player
from config import GameConfig

class Simulation:
    def __init__(self):
        self.map=Map()
        self.players=[
            [Player('Blue',self.map)for i in range(GameConfig.players_in_team)]+
            [Player('Red',self.map)for i in range(GameConfig.players_in_team)]
        ]
        