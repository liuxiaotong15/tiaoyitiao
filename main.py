# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO  
import time  
import signal  
import atexit  
import math
  
atexit.register(GPIO.cleanup)    
  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.OUT, initial=False)  
p = GPIO.PWM(18,50) #50HZ  
p.start(0)  
time.sleep(2)  

up = 9
down = 12.0

standard_distance = 0.005

import time
import picamera
import picamera.array
import cv2


def press(s):
    p.ChangeDutyCycle(down)
    time.sleep(0.08)
    p.ChangeDutyCycle(0)
    time.sleep(s)
    p.ChangeDutyCycle(up)
    time.sleep(0.08)
    p.ChangeDutyCycle(0)
    time.sleep(1)

global x1, x2, y1, y2

def on_EVENT_BUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global x1, y1
        x1 = x
        y1 = y
    elif event == cv2.EVENT_RBUTTONDOWN:
        global x2, y2
        x2 = x
        y2 = y

if __name__ == '__main__':
    distance = 0
    p.ChangeDutyCycle(up)
    time.sleep(0.1)
    p.ChangeDutyCycle(0)
    time.sleep(1)

    print("preparing")
    # time.sleep(1)
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.hflip = True
        camera.vflip = True
        # camera.start_preview()
        # time.sleep(10)
        while True:
            global x1, x2, y1, y2
            x1, x2, y1, y2 = 0,0,0,0

            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                image_orig = stream.array
                # image = image[130:736,508:845]
                # image = image[250:768,365:800]
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', on_EVENT_BUTTONDOWN)
            image = image_orig.copy()
            while(True):
                print(x1, x2)
                if distance != math.sqrt((x1-x2)**2 + (y1-y2)**2):
                    image = image_orig.copy()
                    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                print(distance)
                if x1 != 0:
                    cv2.circle(image, (x1, y1), 3, (0, 255, 255), 3)
                if x2 != 0:
                    cv2.circle(image, (x2, y2), 3, (255, 0, 255), 3)

                cv2.imshow("image", image)
                k = cv2.waitKey(100)
                if k == 27 and x1 != 0 and x2!=0:
                    cv2.destroyAllWindows()
                    break
                
            press(float(274.776915*3.08/1000) * distance * standard_distance)


