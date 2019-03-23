import numpy as np
angles = np.arange(30,132,2 )
count = 0
def send_control():
    global count
    global angles

    print(angles[count])
   
    count+=1
    if count is len(angles)-1:
        count = 0
        angles = angles[::-1]

while 1:
    send_control()
