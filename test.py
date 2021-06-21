from djitellopy import Tello
from time import sleep

tello = Tello()
tello.connect()
print(tello.get_battery())

tello.takeoff()

tello.move_left(20)
tello.rotate_clockwise(90)
tello.move_forward(20)

tello.land()