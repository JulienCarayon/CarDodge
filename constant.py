FSM = "INITIALISATION"  # INIT,CHOOSE CAR,PLAYING,ENDGAME
logoIsDiplayed = False
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 50


class Object:
    def __init__(self, x, y, body, road_at_spawn):
        self.x = x
        self.y = y
        self.body = body
        self.road_at_spawn = road_at_spawn

    def __del__(self):
        print("Object destroyed")
