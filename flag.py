class Flag:
    def __init__(self,position,team):
        self.x,self.y=position
        self.team=team
        self.player_with_flag=None
        self.captured=False

    def update(self):
        if self.player_with_flag is not None:
            self.x=self.player_with_flag.x
            self.y=self.player_with_flag.y