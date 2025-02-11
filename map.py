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
                if  3 < i < 3+MapConfig.base_size:
                    if  center_x-MapConfig.base_size//2 < j < center_x+MapConfig.base_size//2:
                        #flag
                        if i==3+base_cenetr and j==center_x:
                            self.flags_positions.append((i,j))
                        #base field
                        grid[i][j]=1
                elif MapConfig.grid_y-3-MapConfig.base_size < i < MapConfig.grid_y-3:
                    if  center_x-MapConfig.base_size//2 < j < center_x+MapConfig.base_size//2:
                        #flag
                        if i==MapConfig.grid_y-3-base_cenetr and j==center_x:
                            self.flags_positions.append((i,j))
                        #base field
                        grid[i][j]=-1

        
        return grid
    
    def update(self,players,flags):
        self.grid=self.init_grid_state.copy()
        for player in players:
            if player.team =='Blue':
                self.grid[player.x][player.y]=3
            else:
                self.grid[player.x][player.y]=-3
        
        for flag in flags:
            if flag.team =='Blue':
                self.grid[flag.x][flag.y]= 2
            else:
                self.grid[flag.x][flag.y]= -2

                
        
