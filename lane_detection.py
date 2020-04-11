#The program code for lane detection system is given below:

import cv2
import numpy as np
import RPi.GPIO as GPIO
import threading
from imutils.video import VideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time

def mapValue ( x, in_min, in_max, out_min, out_max ) :
    return( x − in_min ) ∗ ( out_max − out_min )   // ( in_max − in_min ) + out_min
    
def calculateee( ) :
    d = int ( ( y [ l − 1 ] + y[0] ) / 2)
    cv2.line ( frame , ( y[0], int( np.size( gray, 0 ) / 2 ) ) ,
    ( y [ l −1], int( np.size( gray, 0 ) / 2 ) ), ( 255, 0, 0 ), 2 )
    return d
cap = VideoStream().start()
time.sleep( 2.0 )

GPIO.setmode( GPIO.BOARD )
GPIO.setwarnings( False )

FRD1 = 5
FRD2 = 3
BAK1 = 8
BAK2 = 7
LED1 = 22
LED2 = 18

GPIO.setup(FRD1, GPIO.OUT)
GPIO.setup(FRD2, GPIO.OUT)
GPIO.setup(BAK1, GPIO.OUT)
GPIO.setup(BAK2, GPIO.OUT)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
pwm1 = GPIO.PWM(LED1, 5000)
pwm2 = GPIO.PWM(LED2, 5000)
pwm1.start(0)
pwm2.start(0)
GPIO.output(FRD1,1)
GPIO.output(FRD2,1)
GPIO.output(BAK1,0)
GPIO.output(BAK2,0)

##cv2.namedWindow(”Video”)
global frame1
global roi1,running
while(True):
	while(True):
		##Captureframe−by−frame
		if cap.read() == None:
			cap = VideoStream().start()
		else:
			frame = cap.read()
			frame = imutils.resize(frame,width = 400)
			frame[frame[:,:,1]>30] = 255
			gray = cv2.cvtColor(frame,
			cv2.COLORBGR2GRAY)
			gray[gray<80] = 0
			gray[gray>= 80] = 255
			35x = np.where(gray[np.size(gray,0)/2,:]<60)
			y = x[0]
			l = len(y)
			
			if l!=0:
				d = calculateee()
				if d>210:
					GPIO.output(FRD1,0)
					GPIO.output(FRD2,1)
					GPIO.output(BAK1,1)
					GPIO.output(BAK2,0)
				elif d<190:
					GPIO.output(FRD1,1)
					GPIO.output(FRD2,0)
					GPIO.output(BAK1,0)
					GPIO.output(BAK2,1)
				else:
				GPIO.output(FRD1,1)
				GPIO.output(FRD2,1)
				pwm1.ChangeDutyCycle(60)
				pwm2.ChangeDutyCycle(60)
				GPIO.output(BAK1,0)
				GPIO.output(BAK2,0)
			else:
				GPIO.output(FRD1,0)
				GPIO.output(FRD2,0)
				GPIO.output(BAK1,1)
				GPIO.output(BAK2,1)
			if cv2.waitKey(1)&0xFF == ord(”q”):   //this maybe elif
				cv2.destroyAllWindows()
				break
	if cv2.waitKey(1)& 0xFF == ord(”q”):

cv2.destroyAllWindows()
GPIO.cleanup()
