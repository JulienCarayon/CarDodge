FSM = "INITIALISATION"  # INIT,CHOOSE CAR,PLAYING,ENDGAME
logoIsDiplayed = False
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 50


class Object:
    def __init__(self, x, y, body):
        self.x = x
        self.y = y
        self.body = body

    def __del__(self):
        print("Object destroyed")
