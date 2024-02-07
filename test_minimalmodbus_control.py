import minimalmodbus as minimalmodbus
import serial
import time

if __name__ == '__main__':
    motors = minimalmodbus.Instrument("COM9", 1,'rtu')
    motors.serial.baudrate = 115200 # Baudrate
    motors.serial.bytesize = 8
    motors.serial.parity = serial.PARITY_NONE
    motors.serial.stopbits = 1
    motors.serial.timeout = 1 # Seconds

    motors.write_register(0x200D, 3, 0, functioncode=int('0x10', 16))
    motors.write_register(0x2088, 64, 0, functioncode=int('0x10', 16))
    print(motors.read_register(0x200D, 0, functioncode=int('0x03', 16)))
    time.sleep(3)

    while True:
        try:
            print(motors.read_register(0x20AB, 1, functioncode=int('0x03', 16)))
            
        except IOError:
            print("Failed to read from ZLAC8015D")
