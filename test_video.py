from djitellopy import Tello
from time import sleep
import cv2

tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

# tello.takeoff()

# tello.move_left(20)
# tello.rotate_clockwise(90)
# tello.move_forward(20)

# tello.land()