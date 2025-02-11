import random
from config import MapConfig

class Player:
    def __init__(self,team,map):
        self.team=team
        self.x,self.y=self.set_starting_position(map)
        self.has_a_flag=False

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
            
    def move(self,direction,map):
        occupied_fields=[-3,3,4,6,-6]
        if direction == 'up':
            if self.y-1>=0 and map.grid[self.x][self.y-1] not in occupied_fields:
                self.y-=1
        elif direction =='down':
            if self.y+1<MapConfig.grid_y and map.grid[self.x][self.y+1] not in occupied_fields:
                self.y+=1
        elif direction == 'left':
            if self.x-1>=0 and map.grid[self.x-1][self.y] not in occupied_fields:
                self.x-=1
        elif direction == 'right':
            if self.x+1<MapConfig.grid_x and map.grid[self.x+1][self.y] not in occupied_fields:
                self.x+=1

    def build(self,direction,map):
        occupied_fields=[-2,2-3,3,4,6,-6]
        if direction == 'up':
            if self.y-1>=0 and map.grid[self.x][self.y-1] not in occupied_fields:
                map.init_grid_state[self.x][self.y-1]=4
        elif direction =='down':
            if self.y+1<MapConfig.grid_y and map.grid[self.x][self.y+1] not in occupied_fields:
                map.init_grid_state[self.x][self.y+1]=4
        elif direction == 'left':
            if self.x-1>=0 and map.grid[self.x-1][self.y] not in occupied_fields:
                map.init_grid_state[self.x-1][self.y]=4
        elif direction == 'right':
            if self.x+1<MapConfig.grid_x and map.grid[self.x+1][self.y] not in occupied_fields:
                map.init_grid_state[self.x+1][self.y]=4

    def captured_the_flag(self,flags):
        if self.has_a_flag:
            return
        
        for flag in flags:
            if flag.captured:
                return
            
            if self.team != flag.team and self.x == flag.x and self.y == flag.y:
                self.has_a_flag=True
                flag.player_with_flag=self
                flag.captured=True
                return
            


