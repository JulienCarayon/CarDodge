from pyb import SPI, Pin, LED


CS = Pin("PE3", Pin.OUT_PP)  # SPI PROTOCOLE

SPI_1 = SPI(  # SPI PROTOCOLE
    1,  # SPI1: PA5,PA6, PA7
    SPI.MASTER,
    baudrate=50000,
    polarity=0,
    phase=0,
)


x_addr = 0x28
y_addr = 0x2A
z_addr = 0x2C
addr_who_am_I = 0x0F
addr_ctrl_reg4 = 0x20


def readReg(address):
    CS.low()
    SPI_1.send(address | 0x80)
    tab_values = SPI_1.recv(1)
    CS.high()
    return tab_values[0]


def writeReg(address, data):
    CS.low()
    SPI_1.send(address)
    SPI_1.send(data)
    CS.high()


def convert_value(high, low):
    value = (high << 8) | low
    if value & (1 << 15):
        value = value - (1 << 16)
    return value * (2000 / 32768)


def read(baseAddr):
    low = readReg(baseAddr)
    high = readReg(baseAddr + 1)
    return convert_value(high, low)
