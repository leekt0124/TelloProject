from djitellopy import Tello
from time import sleep

import key_press as kp

kp.init()
tello = Tello()
tello.connect()
print(tello.get_battery())

def get_keyboard_input():
    rl, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.get_key("RIGHT"): rl = speed
    elif kp.get_key("LEFT"): rl = -speed

    if kp.get_key("UP"): fb = speed
    elif kp.get_key("DOWN"): fb = -speed

    if kp.get_key("w"): ud = speed
    elif kp.get_key("s"): ud = -speed

    if kp.get_key("a"): yv = speed
    elif kp.get_key("d"): yv = -speed

    if kp.get_key("q"): tello.land()
    if kp.get_key("e"): tello.takeoff()

    # print(rl, fb, ud, yv)
    return [rl, fb, ud, yv]

while True:
    vals = get_keyboard_input()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)