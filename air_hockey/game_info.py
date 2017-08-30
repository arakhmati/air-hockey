class GameInfo(object):
    def __init__(self, frame):
        self.frame = frame
        self.puck_was_hit = False
        self.scored = False