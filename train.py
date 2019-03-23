from threading import Thread
import time
from client_test import run_client, q
import cv2
import os
from io import BytesIO
from PIL import Image
import csv
import shutil
import sys

url = 'http://192.168.43.1:8080/video'
##url = 'http://192.168.43.157:8080/video'
cap = cv2.VideoCapture(url)

img_names = []
images = []
steer = []
throt = []

print('storing image in buffer')
 # be stored in the csv file same as the image
def create_test_image(frame, count, steering_angle, throttle):
    

    file = BytesIO()
##     print(_)
    # image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))# this is the image file to be loaded
    # image.save(file, 'png')
    frame =Image.fromarray(frame)
    frame.save(file, 'jpeg')
    file.name = 'centre_%d'%count
    img_names.append('training_data/IMG/centre%d.jpeg'%count)
    steer.append(steering_angle)
    throt.append(throttle)
    file.seek(0)
    return file

folder_name = 'training_data'

def generate_data():
    count = 0
    now = time.time()
    global folder_name


    while True:
        

        _,Frame = cap.read()
        Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
        steering_angle, throttle , mode = q.get()
        

        images.append(create_test_image(Frame, count, steering_angle, throttle))


        count += 1
        if mode == 1:
            break

    future = time.time()
    print('Image FPS is:{}'.format(count/(future-now)))
    print('all frames are now stored in buffer')

    

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        os.mkdir(folder_name+'/IMG')
        print('no directory training_data present so creating one!!')##    
    else:
##        shutil.rmtree(folder_name)
##        print('deleting training_data and creating empty one!!')
        dirs = os.listdir()
        while 1:
            if folder_name in dirs:
                try:
                    folder_name  = folder_name[:-1]+str(int(folder_name[-1])+1)
                except:
                    folder_name = folder_name + str(1)
            else:
                break
                    
        os.mkdir(folder_name)
        os.mkdir(folder_name+'/IMG')

    print('retriving frames from the buffer to folder:{}'.format(folder_name))

    # this runs after completion of while loop
    for image in images:

        index = images.index(image)
        img = Image.open(image)
        img.save('%s/IMG/centre_%d.jpeg'%(folder_name, index))
        image.close()


    with open('%s/driving_log.csv'%('training_data'), 'w+') as csvfile:

         writer = csv.writer(csvfile)
         for a, b,c in zip(img_names,steer, throt ):

             data = [a,b,c]
             writer.writerow(data)
    
    print('process completed')
    sys.exit()

    

thread1 = Thread(target=run_client)
thread2 = Thread(target = generate_data)
thread1.start()
thread2.start()

thread1.join()
thread2.join()


