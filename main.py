from pyb import UART, SPI, Pin, LED, delay
import random
import accelerometer
import voitures
import texts
import vt100
from constant import FSM, SCREEN_HEIGHT, SCREEN_WIDTH, Object


####### PINs DEFINITION #######
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)
led_px, led_nx, led_py, led_ny = LED(1), LED(2), LED(3), LED(4)

####### VARIABLES / CONSTANT #######
logoIsDiplayed = False

######  FUNCTIONS ######
Obj1 = Object  # To make sure the "checkCollision" function works
Obj2 = Object  # To make sure the "checkCollision" function works


def checkCollision(Obj1, Obj2):
    X1_Obj1 = Obj1.x + 4
    X2_Obj1 = Obj1.x + 25 - 4  # len(Obj1.body) - 4
    Y1_Obj1 = Obj1.y + 4
    # print("X2_Obj1")                       Here is how the colision calculation are done
    # print(X2_Obj1)                                         #     _Y1_
    Y2_Obj1 = Obj1.y + (len(Obj1.body.split("\n")) - 4)  # X1 |    |X2
    # print("Y2_Obj1")                                       #    |____|
    # print(Y2_Obj1)                                         #      Y2
    X1_Obj2 = Obj2.x + 4
    X2_Obj2 = Obj2.x + 25 - 4  # len(Obj2.body) - 4
    # print("X2_Obj2")
    # print(X2_Obj2)
    Y1_Obj2 = Obj2.y + 4
    Y2_Obj2 = Obj2.y + (len(Obj2.body.split("\n")) - 4)
    # print("Y2_Obj2")
    # print(Y2_Obj2)

    if (X1_Obj1 > X1_Obj2 and X1_Obj1 < X2_Obj2) or (
        X2_Obj1 > X1_Obj2 and X2_Obj1 < X2_Obj2
    ):
        print("colision X")
        if (Y1_Obj1 > Y1_Obj2 and Y1_Obj1 < Y2_Obj2) or (
            Y2_Obj1 > Y1_Obj2 and Y2_Obj1 < Y2_Obj2
        ):
            print("colision Y")
            return True
    else:
        return False


def accelToMovement(step_x=8, step_y=4, x_min=1, x_max=185, y_min=0, y_max=45):

    x_accel = accelerometer.read(accelerometer.x_addr)
    y_accel = accelerometer.read(accelerometer.y_addr)
    z_accel = accelerometer.read(accelerometer.z_addr)
    global x
    global y
    # print("{:20},{:20},{:20}".format(x_accel, y_accel, z_accel))

    if x_accel > 325 and x <= (x_max - (step_x - 1)):
        led_px.on()
        x = x + step_x
    elif 275:
        led_px.off()

    if y_accel > 325 and y > y_min:
        led_py.on()
        y = y - step_y
    elif 275:
        led_py.off()

    if x_accel < -325 and x >= (x_min + (step_x)):
        led_nx.on()
        x = x - step_x
    elif -275:
        led_nx.off()

    if y_accel < -325 and y < y_max:
        led_ny.on()
        y = y + step_y
    elif -275:
        led_ny.off()


def accelToMovementWithReset(step_x=8, step_y=4, x_min=1, x_max=185, y_min=0, y_max=45):

    x_accel = accelerometer.read(accelerometer.x_addr)
    y_accel = accelerometer.read(accelerometer.y_addr)
    z_accel = accelerometer.read(accelerometer.z_addr)
    global x
    global y
    # print("{:20},{:20},{:20}".format(x_accel, y_accel, z_accel))

    if x_accel > 325 and x <= (x_max - (step_x - 1)):
        led_px.on()
        x = x + step_x
        while x_accel >= 275:
            x_accel = accelerometer.read(accelerometer.x_addr)
    elif 275:
        led_px.off()

    if y_accel > 325 and y >= (y_min + (step_y)):
        led_py.on()
        y = y - step_y
    elif 275:
        led_py.off()

    if x_accel < -325 and x >= (x_min + (step_x)):
        led_nx.on()
        x = x - step_x
        while x_accel <= -275:
            x_accel = accelerometer.read(accelerometer.x_addr)

    elif -275:
        led_nx.off()

    if y_accel < -325 and y <= (y_max - (step_y - 1)):
        led_ny.on()
        y = y + step_y
    elif -275:
        led_ny.off()


###### WHILE MAIN LOOP #####


while True:
    if FSM == "INITIALISATION":
        FSM_Changed = False
        vt100.clear_screen()
        x = 30
        y = 0
        last_x = 0
        enemyCar_Disappeared = True
        road = 0
        difficulty = 1

        vt100.writeAt("Please make sure your VT100 window is set to 200x50", 0, 0)
        delay(2000)

        intro_car1 = Object(90, 160, voitures.police, 0)
        intro_car2 = Object(80, 140, voitures.bleu, 0)
        cars_displayed = False
        choosen_car = None

        if logoIsDiplayed == False:
            vt100.clear_screen()
            vt100.display(texts.flag, 20, 2)
            vt100.display(texts.flag, 170, 2)
            vt100.display(texts.CarDodge, 55, 2)
            logoIsDiplayed = True

            for ycar in range(60, 30, -4):
                intro_car1.y = ycar
                intro_car2.y = ycar - 20
                # vt100.display(voitures.police, 90, ycar)
                vt100.displayObj(intro_car1)
                vt100.displayObj(intro_car2)

            delay(2000)
        del intro_car1
        del intro_car2
        FSM = "CHOOSE CAR"
        FSM_Changed = True
        ##END FSM : INITIALISATION ##

    elif FSM == "CHOOSE CAR":
        Text = Object(30, 1, texts.chooseCar, 0)
        Police = Object(22, 10, voitures.police, 0)
        Ambulance = Object(52, 10, voitures.ambulance, 0)
        Rouge = Object(82, 10, voitures.rouge, 0)
        Bleu = Object(112, 10, voitures.bleu, 0)
        Verte = Object(142, 10, voitures.verte, 0)
        Cars = (Text, Police, Ambulance, Rouge, Bleu, Verte)

        if FSM_Changed == True:
            vt100.clear_screen()
            for car in Cars:
                vt100.displayObj(car)
            FSM_Changed = False

        if last_x != x:
            vt100.clear_object(texts.arrow, last_x, 30)
            vt100.display(skin=texts.arrow, x_display=x, y_display=30)
            last_x = x
        accelToMovementWithReset(step_x=30, x_min=30, x_max=150)

        if push_button.value():
            if x == 30:
                playerCar = Object(90, 32, voitures.police, 0)
            if x == 60:
                playerCar = Object(90, 32, voitures.ambulance, 0)
            if x == 90:
                playerCar = Object(90, 32, voitures.rouge, 0)
            if x == 120:
                playerCar = Object(90, 32, voitures.bleu, 0)
            if x == 150:
                playerCar = Object(90, 32, voitures.verte, 0)
            FSM = "PLAYING"
            FSM_Changed = True

            ##END FSM : CHOOSE CAR ##

    elif FSM == "PLAYING":
        # pyb.delay(2000)
        if FSM_Changed == True or enemyCar_Disappeared == True:
            if FSM_Changed == True:
                vt100.clear_screen()
                live = 3
                last_x = 0
            print("coucou")
            FSM_Changed = False
            enemyCar_Disappeared = False
            random_position = random.randrange(0, 166, 1)
            random_car = random.randrange(1, 6, 1)
            if random_car == 1:
                enemyCar = Object(random_position, 0, voitures.police, road)
            if random_car == 2:
                enemyCar = Object(random_position, 0, voitures.ambulance, road)
            if random_car == 3:
                enemyCar = Object(random_position, 0, voitures.rouge, road)
            if random_car == 4:
                enemyCar = Object(random_position, 0, voitures.bleu, road)
            if random_car == 5:
                enemyCar = Object(random_position, 0, voitures.verte, road)

        if "enemyCar" in locals():

            if road - enemyCar.road_at_spawn < 51:
                enemyCar.y = road - enemyCar.road_at_spawn
                vt100.displayObj(enemyCar)

            if road - enemyCar.road_at_spawn > 50:
                enemyCar_Disappeared = True
                del enemyCar
        else:
            enemyCar_Disappeared = True
        if road // 400 > difficulty and difficulty < 4:
            difficulty = road // 400
        road = road + difficulty

        vt100.writeAt("Score :", 0, 0)
        vt100.writeAt(str(road), 10, 0)
        vt100.writeAt("Lives :", 90, 0)
        vt100.writeAt(str(live), 100, 0)
        vt100.writeAt("Difficulty : ", 170, 0)
        vt100.writeAt(str(difficulty), 190, 0)
        accelToMovement(x_min=1, x_max=165, step_x=8)
        playerCar.x = x
        if "enemyCar" in locals():
            if checkCollision(playerCar, enemyCar) == True:
                live = live - 1
                vt100.clear_screen()
                del enemyCar
                enemyCar_Disappeared = True

                if live == 0:
                    FSM_Changed = True
                    FSM = "LOSE"

        vt100.displayObj(playerCar)
    elif FSM == "LOSE":
        if FSM_Changed == True:
            vt100.clear_screen()
            vt100.display(texts.you_lose, 5, 7)
        FSM_Changed = False
        if push_button.value():
            FSM = "CHOOSE CAR"
            x = 30  # Reset the arrow to the right position
            FSM_Changed = True

    print(FSM)
