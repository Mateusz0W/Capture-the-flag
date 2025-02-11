import pygame
from config import Colors, WindowConfig, MapConfig
from simulation import Simulation

class Renderer:
    def __init__(self,simulation : Simulation):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WindowConfig.width, WindowConfig.height)
        )
        self.clock = pygame.time.Clock()
        self.simulation=simulation

        self.blue_flag = pygame.image.load("blue_flag.png")
        self.blue_flag=pygame.transform.scale(self.blue_flag, (MapConfig.cell_size, MapConfig.cell_size))
        self.red_flag = pygame.image.load("red_flag.png")
        self.red_flag=pygame.transform.scale(self.red_flag, (MapConfig.cell_size, MapConfig.cell_size))

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
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x * MapConfig.cell_size, y * MapConfig.cell_size, MapConfig.cell_size, MapConfig.cell_size)
                )

                if self.simulation.map.grid[y][x] == 2:
                    self.screen.blit(self.blue_flag, (x * MapConfig.cell_size, y * MapConfig.cell_size))
                elif self.simulation.map.grid[y][x] == -2:
                    self.screen.blit(self.red_flag, (x * MapConfig.cell_size, y * MapConfig.cell_size))
                

    def render(self):
        while True:
            self.draw_map()
            self.simulation.run()
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        

