import smbus
import time


#Sensor Parameter
temp_addr = 0x38
temp_meas = 0xE1
temp_chek = 0xAC
temp_rest = 0xBA


#init I2C Bus
bus =  smbus.SMBus(1)


def temp_init():
    #Initialise Sensor
    meas_cfg = [0x08, 0x00]
    bus.write_i2c_block_data(temp_addr, temp_meas, meas_cfg)
    time.sleep(1)
    #Start sensor measuremnt
    #meas_cmd = [0x33, 0x00]
    #bus.write_i2c_block_data(temp_addr, temp_chek, meas_cmd)
    #time.sleep(0.5)

def temp_read():
    #Start sensor measurement
    meas_cmd = [0x33, 0x00]
    bus.write_i2c_block_data(temp_addr, temp_chek, meas_cmd)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(temp_addr, 0x00)
    temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    huml = (data[1] << 12) | (data[2] << 4) | (data[3] & 0xF)
    T = ((temp * 200) / 1048576) - 50
    RH = int((huml * 100)/ 1048576)
    value = [T, RH]
    return value


temp_init()

while True:
    value = temp_read()
    print(u'Temperature: {0:.1f}C'.format(value[0]))
    print(u'Humility: {0}%'.format(value[1]))
    time.sleep(5)
