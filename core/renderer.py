import os
import pygame
from config import Colors, WindowConfig, MapConfig
from core.simulation import Simulation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")

class Renderer:
    def __init__(self,simulation : Simulation):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WindowConfig.width, WindowConfig.height)
        )
        self.clock = pygame.time.Clock()
        self.simulation=simulation

        self.blue_flag = pygame.image.load(os.path.join(ASSETS_PATH, "blue_flag.png"))
        self.blue_flag=pygame.transform.scale(self.blue_flag, (MapConfig.cell_size, MapConfig.cell_size))
        self.red_flag = pygame.image.load(os.path.join(ASSETS_PATH, "red_flag.png"))
        self.red_flag=pygame.transform.scale(self.red_flag, (MapConfig.cell_size, MapConfig.cell_size))

        self.font=pygame.font.Font(None, 50)

    def draw_map(self):
        for y in range(len(self.simulation.map.grid)):
            for x in range(len(self.simulation.map.grid[y])):
                color=Colors.LIGHT_GREY
                if self.simulation.map.grid[y][x]==1:
                    color=Colors.LIGHT_BLUE
                elif self.simulation.map.grid[y][x]== 3:
                    color=Colors.BLUE
                elif self.simulation.map.grid[y][x]==-1:
                    color=Colors.LIGHT_RED
                elif self.simulation.map.grid[y][x]==-3:
                    color=Colors.RED
                elif self.simulation.map.grid[y][x]==4:
                    color=Colors.DARK_GREY
                elif self.simulation.map.grid[y][x]==6:
                    color=Colors.PURPLE
                elif self.simulation.map.grid[y][x]==-6:
                    color=Colors.ORANGE
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x * MapConfig.cell_size, y * MapConfig.cell_size, MapConfig.cell_size, MapConfig.cell_size)
                )

                if self.simulation.map.grid[y][x] == 2:
                    self.screen.blit(self.blue_flag, (x * MapConfig.cell_size, y * MapConfig.cell_size))
                elif self.simulation.map.grid[y][x] == -2:
                    self.screen.blit(self.red_flag, (x * MapConfig.cell_size, y * MapConfig.cell_size))
                

    def display_result(self):
        pygame.draw.rect(self.screen,Colors.BLACK, (0, 550, WindowConfig.width, 50)) #refreshing result
        result = self.font.render(f"Blue {self.simulation.teams_points['Blue']} - {self.simulation.teams_points['Red']} Red",True,Colors.WHITE)
        position=result.get_rect(center=(WindowConfig.width//2,575))
        self.screen.blit(result,position)
        pygame.display.update()

    def render(self):
        reward=0
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            keys = pygame.key.get_pressed()
            action ='move'
            direction='do_nothing'
            idx=0
            if keys[pygame.K_UP]:
                direction ='up'
            elif keys[pygame.K_DOWN]:
                direction ='down'
            elif keys[pygame.K_LEFT]:
                direction ='left'
            elif keys[pygame.K_RIGHT]:
                direction ='right'

            if keys[pygame.K_1]:
                idx=1
            elif keys[pygame.K_2]:
                idx =2
            elif keys[pygame.K_3]:
                idx= 3
            

            self.draw_map()
            self.display_result()
            self.simulation.run(action,direction,'Red',idx)
            #reward+=self.simulation.reward('Red')
            print(self.simulation.reward('Red',idx))
            self.clock.tick(60)

    def render_frame(self):
        self.draw_map()
        self.display_result()
        self.clock.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        

