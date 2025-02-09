import random
from config import MapConfig

class Player:
    def __init__(self,team,map):
        self.team=team
        self.x,self.y=self.set_starting_position(map)

    def set_starting_position(self,map):
        index=0  # blue team
        if self.team == 'Red':
            index=1

        start_x=map.flags_positions[index][0]-MapConfig.base_size//2
        end_x=map.flags_positions[index][0]+MapConfig.base_size//2
        start_y=map.flags_positions[index][1]-MapConfig.base_size//2
        end_y=map.flags_positions[index][1]+MapConfig.base_size//2
            
        while True:
            x=random.randint(start_x,end_x)
            y=random.randint(start_y,end_y)

            if map.grid[x][y]==1 and self.team=='Blue':
                map.grid[x][y]=3
                return x,y
            elif  map.grid[x][y]==-1 and self.team=='Red':
                map.grid[x][y]=-3
                return x,y
                
            
            

