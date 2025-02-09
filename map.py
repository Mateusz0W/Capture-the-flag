from config import MapConfig
import numpy as np

class Map:
    def __init__(self):
        self.grid=self.generate_map()

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
                            grid[i][j]=2
                        #base field
                        else:
                            grid[i][j]=1
                elif MapConfig.grid_y-3-MapConfig.base_size < i < MapConfig.grid_y-3:
                    if  center_x-MapConfig.base_size//2 < j < center_x+MapConfig.base_size//2:
                        #flag
                        if i==MapConfig.grid_y-3-base_cenetr and j==center_x:
                            grid[i][j]=-2
                        #base field
                        else:
                            grid[i][j]=-1

        
        return grid
                
        
