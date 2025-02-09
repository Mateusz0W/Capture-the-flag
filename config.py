from dataclasses import dataclass

@dataclass(frozen=True)
class MapConfig:
    grid_x=55
    grid_y=55
    base_size=10
    cell_size = 10 

@dataclass(frozen=True)
class Colors:
    LIGHT_GREY=(211, 211, 211)
    RED=(255,0,0)
    LIGHT_RED=(255, 77, 77)
    BLUE=(0,0,255)
    LIGHT_BLUE=(102, 204, 255)

@dataclass(frozen=True)
class WindowConfig:
    width=550
    height=550


@dataclass(frozen=True)
class GameConfig:
    players_in_team=1