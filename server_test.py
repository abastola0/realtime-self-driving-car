import json
import network
import machine
import sys
import socket
from hcsr04 import HCSR04
import time
import utime

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('@$#!$#', 'bastola78')

time.sleep(5)

def set_zero():
    pin1a.duty(0)
    pin1b.duty(0)
    pin2a.duty(0)
    pin2b.duty(0)

def stop_all():
    servo_pin.duty(77)
    set_zero()
    UDPServerSocket.close()
    station.active(False)
    print("Received disconnect message.  Shutting down.")
    sys.exit()


## For H-bridge
pin1a = machine.PWM(machine.Pin(27), freq=1000)
pin1b = machine.PWM(machine.Pin(14), freq=1000)
pin2a = machine.PWM(machine.Pin(12), freq=1000)
pin2b = machine.PWM(machine.Pin(13), freq=1000)

set_zero()
## set pin 26 as a pwm pin for servo rotation
servo_pin = machine.PWM(machine.Pin(26), freq = 50)
servo_pin.duty(77)
## For HCSR04
sensor = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=3000)
# set pin 25 and 33 as as trigger and echo pin

event = None

localIP = '0.0.0.0'
localPort   = 3000
bufferSize  = 1024



msgFromServer = "Hello UDP Client"

##bytesToSend         = str.encode(msgFromServer) 
UDPServerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort)) 
UDPServerSocket.settimeout(0.01)
def do_stuffs(scan_val = None):
    global servo_pin
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except:
        return
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    data = json.loads((message))
    if message.decode() == "disconnect":
        stop_all()
    
    if scan_val:
        try:
            y = str(data[2])
            servo_pin.duty(data[2])
            UDPServerSocket.sendto(bytes(str([int(sensor.distance_cm()), y]),'utf-8'), address)
        except:
            stop_all()



##    print(data)

    if data[0] <= 390 and data[1] <= 510:
        # move forward and left'
        
        pin2a.duty((1020- 2*data[0]))
        val = (1020-2*data[0])-(510-data[1])

        if val >= 0:
            pin1a.duty(val)
        else:
            pin2a.duty(-2*val)

        pin1b.duty(0)
        pin2b.duty(0)

    elif data[0] <= 390 and data[1] > 510:
        # move forward and right
        
        pin1a.duty(1020- 2*data[0])
        val = (1020-2*data[0])+(510-data[1])

        if val >= 0:
            pin2a.duty(val)
        else:
            pin1a.duty(-2*val)


        pin1b.duty(0)
        pin2b.duty(0)
        
    elif data[0] > 530 and data[1] <= 510:
        # move back and left
        
        pin2b.duty((2*data[0]-1020))
        val = (2*data[0]-1020)-(510-data[1])

        if val >= 0:
            pin1b.duty(val)

        pin1a.duty(0)
        pin2a.duty(0)

##
    elif data[0] > 530 and data[1] > 510:
        # move back and right
        
        pin1b.duty(2*data[0]-1020)
        val = (2*data[0]-1020)+(510-data[1])

        if val >= 0:
            pin2b.duty(val)

        pin1a.duty(0)
        pin2a.duty(0)

    else:
        set_zero()
        


def drive():

    while True:
        do_stuffs(scan_val='drive')
##        dist = int(sensor.distance_cm())
       
def train():
    machine.Pin(25).PULL_DOWN
    machine.Pin(33).PULL_DOWN
    while True:
        do_stuffs()
        
    
print("UDP server up and listening")

while True:

    
    try:
        event = UDPServerSocket.recvfrom(bufferSize)[0].decode()
    except:
        pass
    if event =='train' or event == 'drive':
        break
    
if event == "train":
    print('switched training mode')
    train()
elif event == "drive":
    print('switched driving mode')
    drive()

