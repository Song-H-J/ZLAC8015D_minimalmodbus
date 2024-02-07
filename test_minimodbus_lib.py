from zlac8015d import ZLAC8015D
import keyboard
import time

motors = ZLAC8015D.MotorController(port = "COM9")

motors.disable_motor()
motors.enable_motor()

cmd_torque = [0,1000]
motors.set_torque(cmd_torque[0],cmd_torque[1])

while True:
    try:
        L,R = motors.get_torque()
        print(f'Left Torque = {L}, Right Torque = {R}')
    except KeyboardInterrupt:
        motors.disable_motor()
        break
