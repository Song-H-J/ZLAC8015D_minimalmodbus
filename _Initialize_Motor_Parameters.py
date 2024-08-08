from zlac8015d import ZLAC8015D
import keyboard
import time

Lmotors = ZLAC8015D.MotorController(port = "COM9", id = 1)
Rmotors = ZLAC8015D.MotorController(port = "COM9", id = 2)

Lmotors.disable_motor()
Lmotors.enable_motor()
Lmotors.set_mode(4)
Lmotors.set_max_rpm(230)
Lmotors.set_max_L_current(17)
Lmotors.set_max_R_current(17)
Lmotors.set_rated_L_current(10)
Lmotors.set_rated_R_current(10)

Rmotors.disable_motor()
Rmotors.enable_motor()
Rmotors.set_mode(4)
Rmotors.set_max_rpm(230)
Rmotors.set_max_L_current(17)
Rmotors.set_max_R_current(17)
Rmotors.set_rated_L_current(10)
Rmotors.set_rated_R_current(10)


while True:
    try:
        # Connect Test

        if keyboard.is_pressed('1'):
            Lmotors.set_rpm_w_toq(200)
        elif keyboard.is_pressed('2'):
            Lmotors.set_rpm_w_toq(100)
        elif keyboard.is_pressed('3'):
            Lmotors.set_rpm_w_toq(-100)
        elif keyboard.is_pressed('4'):
            Lmotors.set_rpm_w_toq(-200)
        elif keyboard.is_pressed('5'):
            Lmotors.set_rpm_w_toq(0)

        elif keyboard.is_pressed('q'):
            Rmotors.set_rpm_w_toq(200)
        elif keyboard.is_pressed('w'):
            Rmotors.set_rpm_w_toq(100)
        elif keyboard.is_pressed('e'):
            Rmotors.set_rpm_w_toq(-100)
        elif keyboard.is_pressed('r'):
            Rmotors.set_rpm_w_toq(-200)
        elif keyboard.is_pressed('t'):
            Rmotors.set_rpm_w_toq(0)
        
                        
    except KeyboardInterrupt:
        Lmotors.disable_motor()
        Rmotors.disable_motor()
        break
    