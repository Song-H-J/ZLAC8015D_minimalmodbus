from zlac8015d import ZLAC8015D
import keyboard
import time

motors = ZLAC8015D.MotorController(port = "COM9")

motors.disable_motor()
motors.enable_motor()
motors.set_mode(4)
motors.set_max_rpm(250)
motors.set_max_L_current(11)
motors.set_max_R_current(11)
motors.set_rated_L_current(6)
motors.set_rated_R_current(6)
motors.RATED_TORQUE = 3000
start = time.time()

while True:
    try:
        start = time.time()
        L,R = motors.get_rpm()
        end = time.time()
        print(f'Left RPM = {L}, Right RPM = {R}, time = {end-start}')

        #L,R = motors.get_torque()
        #V = motors.get_voltage()
        #print(f'L Torque = {L}, R Torque = {R}, Vol = {V}')
        
        if keyboard.is_pressed('1'):
            motors.set_rpm_w_toq(200)
        elif keyboard.is_pressed('2'):
            motors.set_rpm_w_toq(100)
        elif keyboard.is_pressed('3'):
            motors.set_rpm_w_toq(-100)
        elif keyboard.is_pressed('4'):
            motors.set_rpm_w_toq(-200)
        elif keyboard.is_pressed('5'):
            motors.set_rpm_w_toq(0)
        elif keyboard.is_pressed('0'):
            motors.set_mode(4)
                        
    except KeyboardInterrupt:
        motors.disable_motor()
        break
    