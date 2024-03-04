from zlac8015d import ZLAC8015D
import keyboard
import time

motors = ZLAC8015D.MotorController(port = "COM9")

motors.disable_motor()
motors.enable_motor()
motors.set_mode(4)
motors.set_max_rpm(100)
motors.set_max_L_current(5)
motors.set_max_R_current(5)
motors.set_rated_L_current(3)
motors.set_rated_R_current(3)

while True:
    try:
        #L,R = motors.get_rpm()
        #print(f'Left RPM = {L}, Right RPM = {R}')

        #L,R = motors.get_torque()
        #V = motors.get_voltage()
        #print(f'L Torque = {L}, R Torque = {R}, Vol = {V}')
        ID = motors.get_rs485_id()
        print(f'ID = {ID}')

        if keyboard.is_pressed('3'):
            motors.set_rpm_w_toq(200)
        elif keyboard.is_pressed('4'):
            motors.set_rpm_w_toq(100)
        elif keyboard.is_pressed('q'):
            motors.set_rpm_w_toq(-100)
        elif keyboard.is_pressed('w'):
            motors.set_rpm_w_toq(-200)
        elif keyboard.is_pressed('e'):
            motors.set_rpm_w_toq(0)
        elif keyboard.is_pressed('1'):
            motors.set_mode(3)
            motors.set_rpm(30,30)
                        
    except KeyboardInterrupt:
        motors.disable_motor()
        break
    