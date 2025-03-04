from dataclasses import dataclass

@dataclass(frozen=True)
class MapConfig:
    grid_x=55
    grid_y=55
    base_size=10
    cell_size = 10 
    y_offset = 3

@dataclass(frozen=True)
class Colors:
    BLACK = (0,0,0)
    DARK_GREY=(64, 64, 64)
    LIGHT_GREY=(211, 211, 211)
    RED=(255,0,0)
    LIGHT_RED=(255, 77, 77)
    BLUE=(0,0,255)
    LIGHT_BLUE=(102, 204, 255)
    ORANGE=(255, 165, 0)
    PURPLE=(128, 0, 128)
    WHITE=(255, 255, 255)

@dataclass(frozen=True)
class WindowConfig:
    width=550
    height=600

@dataclass(frozen=True)
class GameConfig:
    players_in_team=4

@dataclass(frozen=True)
class MLConfig:
    GAMMA=0.99
    BATCH_SIZE=32
    REPLAY_SIZE=10_000
    REPLAY_START_SIZE=10_000
    LEARNING_RATE= 1e-4
    SYNC_TARGET_FRAMES = 1000
    EPSILON_DECAY_LAST_FRAME = 150000
    EPSILON_START = 1.0
    EPSILON_FINAL = 0.01
    MEAN_REWARD_BOUND = 50
