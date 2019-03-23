import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

r = np.arange(0, 100, 10)
ang = np.pi/4.5
theta = np.repeat(ang, repeats = len(r))
fig = plt.figure()
ax = plt.subplot(111, projection='polar')
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.set_rmax(100)
ax.grid(True, color = 'green')
ax.set_facecolor('black')
ax.set_xticks(np.linspace(0, np.pi, 20))
ax.set_title("A line plot on a polar axis", va='bottom')
line, = plt.plot(theta, r,  'green',marker = 'o', markersize = 7)
R = 100
m, = plt.plot(np.pi/7, R,marker = '*', markersize = 5 )
flag = 1

def update(frame):
    global ang
    global r
    global R
    global flag
    m.set_data(np.pi/4, R)
    R-=0.2

    theta = np.repeat(ang, repeats = len(r))
    
    if flag:
        line.set_data(theta,r )
        ang+=0.005
        if ang >= np.pi:
            flag = 0
        return line,m,
    else:
        line.set_data(theta,r )
        ang-=0.005
        if ang <= 0:
            flag = 1
        return line,


line_ani = animation.FuncAnimation(fig, update,
                                   interval=7, blit=True)

plt.show()