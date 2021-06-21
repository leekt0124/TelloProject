from djitellopy import Tello
import time
import cv2
from threading import Thread

import key_press as kp

kp.init()
tello = Tello()
tello.connect()
print(tello.get_battery())

VIDEO = True
CONTROL = True

tello.streamon()

def get_keyboard_input():
    global VIDEO
    global CONTROL
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

    if kp.get_key("q"): 
        tello.land()
        VIDEO = False
        CONTROL = False
        video_t.join()

    if kp.get_key("e"): tello.takeoff()

    if kp.get_key("z"): 
        cv2.imwrite(f'Resources/Images/{time.time}.jpg', img)
        time.sleep(0.1)

    # print(rl, fb, ud, yv)
    return [rl, fb, ud, yv]

def video():
    while VIDEO:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

# video_t = Thread(target=video)
# video_t.start()

def control():
    while CONTROL:
        vals = get_keyboard_input()
        tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])


video_t = Thread(target=video)
video_t.start()

# tello.takeoff()

while CONTROL:
    control()
#     vals = get_keyboard_input()
#     # tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    # img = tello.get_frame_read().frame
    # img = cv2.resize(img, (360, 240))
    # cv2.imshow("Image", img)
    # cv2.waitKey(1)