import sys
import socket, struct
##import time
import pygame
from modules.utils import *
import json
from numpy import interp
import queue
import time

q = queue.LifoQueue(maxsize = 1)

def run_client():
    # Main configuration
    UDP_IP = '192.168.43.157' # Vehicle IP address
    UDP_PORT = 3000 # This port match the ones using on other scripts

    update_rate = 0.01 # 100 hz loop cycle

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # this triggers the training mode on the server

    sock.sendto(bytes('train', 'utf-8'), (UDP_IP,UDP_PORT ))


    try:
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        
    except:
        print( "No joystick connected on the computer")


    while True:
        current = time.time()
        elapsed = 0

        # Joystick reading
        pygame.event.pump()
        ##    interp(256,[1,512],[5,10])
        roll = int(interp(round(joystick.get_axis(1),3), [-1,1],[0,1020]))
        yaw = int(interp(round(joystick.get_axis(3),3), [-1,1], [0,1020]))
        mode = joystick.get_button(8)
        if q.full():
            q.queue.clear()

        ##      q.put([yaw, roll, mode])        
        q.put([round(joystick.get_axis(1),3),round(joystick.get_axis(3),3),mode])



        buf = str([roll,yaw])

        sock.sendto(bytes(buf, 'utf-8'), (UDP_IP,UDP_PORT ))

        if mode == 1:
            break


        # Make this loop work at update_rate
        while elapsed < update_rate:
            elapsed = time.time() - current
    sock.sendto(bytes('disconnect', 'utf-8'), (UDP_IP, UDP_PORT))
    sock.close()
    sys.exit("pressed home button. Shutting down!!")
