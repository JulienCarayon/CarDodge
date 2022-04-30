from pyb import UART, SPI, Pin, LED, delay

# import pyb
import accelerometer
import voitures
import texts
import vt100
from constant import FSM

####### UART #######


####### PINs DEFINITION #######
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)
led_px, led_nx, led_py, led_ny = LED(1), LED(2), LED(3), LED(4)

######## SPI/ACCELEROMETER MANAGEMENT ###########

# x_addr = 0x28
# y_addr = 0x2A
# z_addr = 0x2C
# addr_who_am_I = 0x0F
# addr_ctrl_reg4 = 0x20


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

        cars_displayed = False
        choosen_car = None
        if logoIsDiplayed == False:
            vt100.clear_screen()
            vt100.display(texts.flag, 20, 2)
            vt100.display(texts.flag, 170, 2)
            vt100.display(texts.CarDodge, 55, 2)
            logoIsDiplayed = True
            for ycar in range(160, 30, -4):
                vt100.display(voitures.police, 90, ycar)
                vt100.display(voitures.bleu, 80, ycar - 20)

            delay(2000)

        FSM = "CHOOSE CAR"
        FSM_Changed = True
        ##END FSM : INITIALISATION ##

    elif FSM == "CHOOSE CAR":
        if FSM_Changed == True:
            vt100.clear_screen()
            vt100.display(texts.chooseCar, 30, 1)
            vt100.display(voitures.police, 22, 10)
            vt100.display(voitures.ambulance, 52, 10)
            vt100.display(voitures.rouge, 82, 10)
            vt100.display(voitures.bleu, 112, 10)
            vt100.display(voitures.verte, 142, 10)
            FSM_Changed = False

        if last_x != x:
            vt100.clear_object(texts.arrow, last_x, 30)
            vt100.display(skin=texts.arrow, x_display=x, y_display=30)
            last_x = x
        accelToMovementWithReset(step_x=30, x_min=30, x_max=150)

        if push_button.value():
            if x == 30:
                choosen_car = voitures.police
            if x == 60:
                choosen_car = voitures.ambulance
            if x == 90:
                choosen_car = voitures.rouge
            if x == 120:
                choosen_car = voitures.bleu
            if x == 150:
                choosen_car = voitures.verte
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
            vt100.display(choosen_car, x, 32)
            last_x = x

        # for i in range(0, SCREEN_HEIGHT, 1):
        #     move_VT100(0, i)
        #     uart.write("⬜️")
        #     move_VT100(0, i + 1)
        #     uart.write("⬜️")
        #     move_VT100(0, i + 2)
        #     uart.write("⬜️")
        #     move_VT100(0, i + 3)
        #     uart.write("⬜️")
        #     move_VT100(0, i + 4)
        #     uart.write("  ")
        accelToMovement(x_min=1, x_max=165, step_x=8)
    # move(x, y)
    # uart.write("█")
    # clear_screen()

    # for index, line in enumerate(voitures.police.splitlines()):
    #     move_VT100(x, y + index)
    #     uart.write(line)

    # if (
    #     push_button.value() and FSM == "PLAYING"
    # ):  # DEMANDER AU PROF POURQUOI IL RENTRE DANS LA BOUCLE !!
    #     FSM = "INITIALISATION"

    # string = "X = " + str(x) + " Last_X = " + str(last_x)
    # clear_line_VT100(49)
    # X_MIDDLE = int((SCREEN_WIDTH - len(string)) / 2)
    # move_VT100(X_MIDDLE, SCREEN_HEIGHT - 1)
    # uart.write(string)
