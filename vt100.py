from pyb import UART

# import pyb
from constant import SCREEN_WIDTH

uart = UART(2)
uart.init(2000000, bits=8, parity=None, stop=1)


def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")


def clear_line(y_to_clear):
    for x in range(0, SCREEN_WIDTH):
        move(x, y_to_clear)
        uart.write(" ")


def clear_object(skin, x_display, y_display):
    for yindex, line in enumerate(skin.splitlines()):
        move(x_display, y_display + yindex)
        for xindex in range(1, len(skin)):
            uart.write(" ")


def move(x_display, y_display):
    uart.write("\x1b[{};{}H".format(y_display, x_display))


def display(skin, x_display, y_display):
    for index, line in enumerate(skin.splitlines()):
        move(x_display, y_display + index)
        uart.write(line)


def write(char):
    uart.write(char)
