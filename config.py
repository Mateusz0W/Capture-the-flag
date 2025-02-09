from dataclasses import dataclass

@dataclass(frozen=True)
class MapConfig:
    grid_x=55
    grid_y=55
    base_size=10
    cell_size = 10 

@dataclass(frozen=True)
class Colors:
    GREY=(128, 128, 128)
    RED=(255,0,0)
    LIGHT_RED=(255, 102, 102)
    BLUE=(0,0,255)
    LIGHT_BLUE=(173, 216, 230)

@dataclass(frozen=True)
class WindowConfig:
    width=550
    height=550