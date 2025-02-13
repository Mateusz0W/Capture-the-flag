from config import MapConfig
import numpy as np

class Map:
    def __init__(self):
        self.flags_positions=[]
        self.grid=self.generate_map()
        self.init_grid_state=self.grid.copy()

    def generate_map(self):
        grid = np.zeros((MapConfig.grid_y, MapConfig.grid_x), dtype=int)
        center_x=MapConfig.grid_x//2
        base_cenetr=MapConfig.base_size//2

        for i in range(MapConfig.grid_y):
            for j in range(MapConfig.grid_x):
                #base
                if  MapConfig.y_offset < i < MapConfig.y_offset + MapConfig.base_size:
                    if  center_x-MapConfig.base_size//2 < j < center_x+MapConfig.base_size//2:
                        #flag
                        if i==MapConfig.y_offset + base_cenetr and j==center_x:
                            self.flags_positions.append((j,i))
                        #base field
                        grid[i][j]=1
                elif MapConfig.grid_y- MapConfig.y_offset - MapConfig.base_size < i < MapConfig.grid_y - MapConfig.y_offset:
                    if  center_x-MapConfig.base_size//2 < j < center_x+MapConfig.base_size//2:
                        #flag
                        if i==MapConfig.grid_y- MapConfig.y_offset -base_cenetr and j==center_x:
                            self.flags_positions.append((j,i))
                        #base field
                        grid[i][j]=-1

        
        return grid
    
    def update(self,players,flags):
        self.grid=self.init_grid_state.copy()
        for player in players:
            if player.team =='Blue':
                if player.has_a_flag:
                    self.grid[player.y][player.x]=6
                else:
                    self.grid[player.y][player.x]=3
            else:
                if player.has_a_flag:
                    self.grid[player.y][player.x]=-6
                else:
                    self.grid[player.y][player.x]=-3
        
        for flag in flags:
            if flag.team =='Blue' and not flag.captured:
                self.grid[flag.y][flag.x]= 2
            elif flag.team =='Red' and not flag.captured:
                self.grid[flag.y][flag.x]= -2

    def reset(self):
        self.flags_positions.clear()
        self.grid=self.generate_map()
        self.init_grid_state=self.grid.copy()

                
        
