from pyb import UART, SPI, Pin, LED, delay


# import pyb
import accelerometer
import voitures
import texts
import vt100
from constant import FSM, SCREEN_HEIGHT, SCREEN_WIDTH, Object

####### UART #######


####### PINs DEFINITION #######
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)
led_px, led_nx, led_py, led_ny = LED(1), LED(2), LED(3), LED(4)

####### VARIABLES / CONSTANT #######
logoIsDiplayed = False

######  FUNCTIONS ######


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
        # print(accelerometer.readReg(addr_who_am_I))  # SPI PROTOCOLE
        # accelerometer.writeReg(addr_ctrl_reg4, 0x077)  # SPI PROTOCOLE
        vt100.clear_screen()
        x = 30
        y = 0
        last_x = 0
        vt100.move(0, 0)
        vt100.write("Please make sure your VT100 window is set to 200x50")
        delay(2000)
        intro_car1 = Object(90, 160, voitures.police)
        intro_car2 = Object(80, 140, voitures.bleu)
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
        Text = Object(30, 1, texts.chooseCar)
        Police = Object(22, 10, voitures.police)
        Ambulance = Object(52, 10, voitures.ambulance)
        Rouge = Object(82, 10, voitures.rouge)
        Bleu = Object(112, 10, voitures.bleu)
        Verte = Object(142, 10, voitures.verte)
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
                playerCar = Object(90, 32, voitures.police)
            if x == 60:
                playerCar = Object(90, 32, voitures.ambulance)
            if x == 90:
                playerCar = Object(90, 32, voitures.rouge)
            if x == 120:
                playerCar = Object(90, 32, voitures.bleu)
            if x == 150:
                playerCar = Object(90, 32, voitures.verte)
            FSM = "PLAYING"
            FSM_Changed = True
            ##END FSM : CHOOSE CAR ##

    elif FSM == "PLAYING":
        # pyb.delay(2000)
        if FSM_Changed == True:
            vt100.clear_screen()
            FSM_Changed = False
            last_x = 0

        if x != last_x:
            playerCar.x = x
            vt100.displayObj(playerCar)
            last_x = x
        accelToMovement(x_min=1, x_max=165, step_x=8)
