
import detect
import argparse
import base64
import time
import socket
import cv2
import numpy as np
from io import BytesIO
import utils
import tensorflow
from keras.models import load_model
from PIL import Image
from numpy import interp
import sys
from gps_utils import rdp
import mplleaflet
import sqlite3 as sql
import os
import matplotlib.pyplot as plt

##url = 'http://192.168.43.1:8080/video'
url = 'http://192.168.43.1:8080/video'
bufferSize  = 1024
UDP_IP = '192.168.43.157' # Vehicle IP address
UDP_PORT = 3000  # This port match the ones using on other scripts

cap = cv2.VideoCapture(url)
model = None
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.001)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# this triggers the driving mode on the server 
sock.sendto(bytes('drive', 'utf-8'), (UDP_IP,UDP_PORT ))
def recieve_data():
##     print('data recieved from the server:{}'.format(sock.recvfrom(bufferSize)))

     try:
          m = sock.recvfrom(bufferSize)[0].decode("utf-8") 
          print(m)
     except:
          pass

     
def send_control(values):
     values = [values[0], 1020-int(interp(round(values[1], 4), [-1,1], [0,1020]))]
     sock.sendto(bytes(str(values), 'utf-8'), (UDP_IP,UDP_PORT ))
     print('data sent to the vehicle:{}'.format(values))
     try:
          recieve_data()
     except:
          pass
##     print('data recieved from the server:{}'.format(sock.recvfrom(bufferSize)[0]))

def put_text(frame,steering_angle):
     return cv2.putText(frame,'Throttle:-1, Steering angle:'+str(round(steering_angle, 4)),(10,310), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(200,255,155),1 )

def predict_steer():     
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     steering_angle = 0
     while True:
          
          _,Frame = cap.read()
          
          # gets data in the form of pandas dataframe of image , throttle and steering angle
          if _:
               frame = Frame.copy()
               frame = put_text(frame, steering_angle)
               # this is to detect the pedrestrians

               cv2.imshow('image', frame)
               if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop_all()
                    
               Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
               # image = Image.open(BytesIO(base64.b64decode(Frame)))
               image = Frame
               try:
                    image = np.asarray(image)
                    image = utils.preprocess(image)
                    image = np.array([image])
                    steering_angle = float(model.predict(image ,batch_size = 1))
                    throttle = 0 # set throttle to maximum in our test case where our speed and mass is not high enough to create large Inertia
                    send_control([throttle, steering_angle])
                    
               except Exception as e:
                    print(e)
          else:
               print('no frames recieved!\nplease make sure the video server is running!!')
               stop_all()

def stop_all():
     dat = str([511,511])
     sock.sendto(bytes(dat, 'utf-8'), (UDP_IP,UDP_PORT ))
     sock.sendto(bytes('disconnect', 'utf-8'), (UDP_IP, UDP_PORT))
     sock.close()
     sys.exit("pressed home button. Shutting down!!")



def generate_map():

     conn = sql.connect("geocoordinates1.db")
     c = conn.cursor()
     x = c.execute("SELECT lon,lat FROM  GeoCoordinates ")
     list_data = x.fetchall()
     x = []
     y = []
     for data in list_data:
          x.append(data[0])
          y.append(data[1])
     list_data = np.array(list_data)
     plt.plot(list_data[:,0],list_data[:,1])
     list_data = rdp(list_data, epsilon = 1e-4)
     fig = plt.figure()
     plt.plot(list_data[:, 0], list_data[:, 1], "r*")     
     mplleaflet.show() 

     
if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='Remote Driving')
     parser.add_argument(
          'model',
          type=str,
          help='Path to model h5 file. Model should be on the same path.'
     )
     parser.add_argument(
          'image_folder',
          type=str,
          nargs='?',
          default='',
          help='Path to image folder. This is where the images from the run will be saved.'
     )
     args = parser.parse_args()
     model = load_model(args.model)
     try:
          generate_map()
          predict_steer()
   
          
     except KeyboardInterrupt:
          stop_all()
