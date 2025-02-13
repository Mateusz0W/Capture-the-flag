from config import MapConfig

class Flag:
    def __init__(self,position,team):
        self.x,self.y=position
        self.team=team
        self.captured=False

    def update(self,player):
        if player is not None:
            self.x=player.x
            self.y=player.y

    def in_opponent_base(self):
        center_x = MapConfig.grid_x//2
        start_x = center_x-MapConfig.base_size // 2
        end_x = center_x+MapConfig.base_size // 2

        blue_base_start_y = MapConfig.y_offset
        blue_base_end_y = MapConfig.y_offset+MapConfig.base_size
        red_base_start_y = MapConfig.grid_y - MapConfig.y_offset-MapConfig.base_size
        red_base_end_y = MapConfig.grid_y - MapConfig.y_offset

        if self.team == 'Red':
            if start_x < self.x < end_x and blue_base_start_y < self.y < blue_base_end_y:
                return True
            else:
                return False
        elif self.team == 'Blue':
            if start_x < self.x < end_x and red_base_start_y < self.y < red_base_end_y:
                return True
            else:
                return False
        

    def reset(self,position):
        self.x,self.y=position
        self.captured=False
        