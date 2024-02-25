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
motors.RATED_TORQUE = 6000

while True:
    try:
        #L,R = motors.get_rpm()
        #print(f'Left RPM = {L}, Right RPM = {R}')

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

        elif keyboard.is_pressed('z'): motors.set_mode(3)

        elif keyboard.is_pressed('q'):
            motors.set_rpm(100,100)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L >= 100:
                    end = time.time()
                    break
            print(f'Vel mode go to 100 RPM14 time = {end-start}')

        elif keyboard.is_pressed('w'):
            motors.set_rpm(50,50)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L <= 50:
                    end = time.time()
                    break
            print(f'Vel mode go to 50 RPM time = {end-start}')

        elif keyboard.is_pressed('e'):
            motors.set_rpm(200,200)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L >= 200:
                    end = time.time()
                    break
            print(f'Vel mode go to 200 RPM time = {end-start}')

        elif keyboard.is_pressed('r'):
            motors.set_rpm(-100,-100)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L <= -100:
                    end = time.time()
                    break
            print(f'Vel mode go to -100 RPM time = {end-start}')

        elif keyboard.is_pressed('t'):
            motors.set_rpm(-200,-200)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L <= -200:
                    end = time.time()
                    break
            print(f'Vel mode go to -200 RPM time = {end-start}')

        elif keyboard.is_pressed('y'):
            motors.set_rpm(0,-0)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L <= 0:
                    end = time.time()
                    break
            print(f'Vel mode go to 0 RPM time = {end-start}')
        elif keyboard.is_pressed('u'):
            motors.set_rpm(0,-0)
            start = time.time()
            while True:
                L,R = motors.get_rpm()
                if L >= 0:
                    end = time.time()
                    break
            print(f'Vel mode go to 0 RPM time = {end-start}')

                        
    except KeyboardInterrupt:
        motors.disable_motor()
        break
    