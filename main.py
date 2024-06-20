import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import logging

# logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# set up figure
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# add axis labels
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# universal const
e = -1.602 * 10**-19


# particle dictionary
pd = {
    "proton": {"m": 1.67 * 10**-27, "Q": -e, "c": "r", "view": 9**9},
    "electron": {"m": 9.11 * 10**-31, "Q": e, "c": "b", "view": 10**-15},
}

# fields
bo = np.array([0, 0, 1])  # the magnitude of the magnetic field.
E = np.array([0, 0, 0])

# time counter
n = count()

# particle path storage lists
x_values = []
y_values = []
z_values = []


class Particle:
    def __init__(self, p_type):
        self.Q = p_type["Q"]
        self.m = p_type["m"]
        self.pos = np.array([0, 0, 0])
        self.v = np.array([1, 0, 0])
        self.c = p_type["c"]
        self.view_scaler = p_type["view"]


p = Particle(pd["electron"])


# noinspection PyUnusedLocal
def animate_particle(t):
    log.info([next(n), "iteration"])  # log number of times the loop happens
    t = t * p.view_scaler
    # t scaler
    u = p.v
    # position calc
    a = p.Q * (E + np.cross(p.v, bo)) / p.m
    log.info(a)
    v = u + a * t
    log.info([v, "v"])
    p.pos = p.pos + v
    p.v = v

    # append particle position
    x_values.append(p.pos[0])
    y_values.append(p.pos[1])
    z_values.append(p.pos[2])

    # draw the particle
    plt.cla()
    plt.plot(p.pos[0], p.pos[1], p.pos[2], marker="v", c=p.c)
    plt.plot(x_values, y_values, z_values, c=p.c)


# quit function
def on_close_event(event):
    print(event)
    quit()


# scat = ax.scatter(p.x, p.y, p.z, marker="v", c=p.color)

anim = FuncAnimation(plt.gcf(), animate_particle)
fig.canvas.mpl_connect("close_event", on_close_event)
# set up viewer
plt.show()
