import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

fig = plt.figure()
ax = plt.subplot(111, projection = 'polar')
ax.set_facecolor('black')
ax.set_xticks(np.linspace(0, np.pi, 20))
ax.grid(color='green', linewidth=1.5)
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
plt.title(' SONAR DATA PLOT', fontdict=font)
region = [0,np.pi/12,10]

ln, = ax.plot(0, 0, 'white',marker='o',markersize = 5)


server_data = [np.pi/2, 30]

def init():
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_rmax(100)
    return ln,

count = 0
flag1 = 0

flag2 = 1

def ch_region():
    global flag2
    global region
    if flag2:
        region[0]+=np.pi/12
        region[1]+=np.pi/12
        if region[0]>=11*np.pi/12:
            flag2 = 0
    elif flag2 ==0:
        region[0]-=np.pi/12
        region[1]-=np.pi/12
        if region[0]<=np.pi/12:
            flag2 = 1


def update(frame):
    global count
    global flag1
    global region
    global theta
    theta = np.linspace(region[0],region[1])


    if flag1 == 0:
        count+=25
        r = np.repeat(count, repeats=len(theta))
        ln.set_data(theta,r)
        
        if count ==100:
            flag1 = 1
        
        return ln,
    if flag1 ==1:
        count-=25
        r = np.repeat(count, repeats=len(theta))
        ln.set_data(theta,r)
        if count ==0:
            flag1 = 0
            ch_region()
        return ln,
 
ani1 = FuncAnimation( fig = fig,func = update,init_func=init,blit = True , interval = 50,repeat=False)

plt.show()
