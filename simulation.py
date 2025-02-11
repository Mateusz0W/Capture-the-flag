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
    
    def next_step(self):
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

        for flag in self.flags:
            flag.update()

    def run(self):
        self.next_step()
        self.map.update(self.players,self.flags)
