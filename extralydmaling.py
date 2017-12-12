import _thread
import time
import smbus
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
 
#import socket
from socket import *
UDP_IP = "255.255.255.255"
#UDP_IP = "192.168.137.1"
UDP_PORT = 11001
bus = smbus.SMBus(1)
MESSAGE = "Optager Lydnivue!"
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)
#host = socket.gethostname()
sock = socket(AF_INET, SOCK_DGRAM)
#sock.bind((host, UDP_PORT))
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
running = True
delay = 0.5

def warning():
	while True:
		MESSAGE = "FUCK!"
		reading = bus.read_byte(0x48)
		if(reading >= 80):
			print (MESSAGE)
			global delay
			time.sleep(delay)
		print_message()

def setLight():
        while True:
                reading = bus.read_byte(0x48)
                #Grøn
                if(reading <= 50):
                        GPIO.output(11,GPIO.LOW)
                        GPIO.output(9,GPIO.HIGH)
                        GPIO.output(10,GPIO.HIGH)
                #Gul
                if(50 < reading < 80):
                        GPIO.output(11,GPIO.LOW)
                        GPIO.output(9,GPIO.HIGH)
                        GPIO.output(10,GPIO.LOW)
                #Rød
                if(80 < reading):
                        GPIO.output(11,GPIO.HIGH)
                        GPIO.output(9,GPIO.HIGH)
                        GPIO.output(10,GPIO.LOW)
                #print_message()
                warning()
 
# Define a function for the thread
def print_message():
        bus.write_byte(0x48, 0x03)
        while True:
                if (running == True):
                        #setLight()
                        #warning()
                        reading = bus.read_byte(0x48)
                        reading = bus.read_byte(0x48)
                        global delay
                        time.sleep(delay)
                        print (reading)
                        sock.sendto(bytes(str(reading),'UTF-8'),(UDP_IP, UDP_PORT))
                        setLight()
                        #warning()

def change_delay():
        time.sleep(3)
        global delay
 
        while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                print ("received message:", data)
                splitext = data.split()
                print (splitext)
                print (str(splitext[1]))
                if (splitext[1]) == bytes("delay", 'UTF-8'):
                        delay = float(splitext[2])
                        print ("Skifter delay")


# Create two threads as follows
try:
        _thread.start_new_thread( print_message, () )
        _thread.start_new_thread( change_delay, () )
except:
        print ("Error: unable to start thread")
 
# endles do nothing - while other threads are working
while True:
        pass
