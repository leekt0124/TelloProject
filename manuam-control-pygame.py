from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
import logging
import math

from threading import Thread

# Speed of the drone
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 120


class Drone(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Control Pad")
        self.screen = pygame.display.set_mode([100, 100])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Set logger level
        Tello.LOGGER.setLevel(logging.WARNING)

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False
        self.should_stop = False

        self.video_t = Thread(target=self.video)

        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def connect(self):
        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        self.frame_read = self.tello.get_frame_read()

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.update()
            elif event.type == pygame.QUIT:
                self.should_stop = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.should_stop = True
                else:
                    self.keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.keyup(event.key)

    def run(self):
        curr_time = time.time()
        while not self.should_stop:
            # Manual control
            self.control()

            # Odometry
            elapsed_time = time.time() - curr_time
            curr_time = time.time()
            self.odometry(elapsed_time)

        pygame.quit()
        
        
        self.video_t.join()
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)

    def video(self):
        while not self.should_stop:
            frame = self.frame_read.frame
            frame = cv2.resize(frame, (360, 240))
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 240 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("video", frame)
            cv2.waitKey(1)

    def odometry(self, elapsed_time):
        # Currently I am using dead reckoning method, which accumulates error easily and will shift drone from its expected localized position
        # Orientation information from Tello is pretty accurate though
        # print(self.tello.get_speed_x(), self.tello.get_speed_y(), self.tello.get_speed_z(), self.tello.get_yaw())
        print(self.tello.get_acceleration_x(), self.tello.get_acceleration_y(), self.tello.get_acceleration_z())
        v_y = self.tello.get_speed_x()
        v_x = self.tello.get_speed_y()
        v_z = - self.tello.get_speed_z()
        # self.yaw = self.tello.get_yaw()
        # self.x += (v_x * math.cos(math.radians(self.yaw)) + v_y * math.sin(math.radians(self.yaw))) * elapsed_time
        # self.y += (- v_x * math.sin(math.radians(self.yaw)) + v_y * math.cos(math.radians(self.yaw))) * elapsed_time
        self.x += v_x * elapsed_time
        self.y += v_y * elapsed_time
        self.z += v_z * elapsed_time

        # print(self.x, self.y, self.z, self.tello.get_height(), self.tello.get_barometer())
        self.draw()

    def draw(self):
        img = np.zeros((1000, 1000, 3), np.uint8)
        cv2.circle(img, (50+x, 50+y), 10, (0, 0, 255), cv2.FILLED)
        cv2.imshow("position simulation", img)
        cv2.waitKey(1)


def main():
    drone = Drone()
    
    drone.connect()
    drone.video_t.start()
    drone.run()

if __name__ == '__main__':
    main()