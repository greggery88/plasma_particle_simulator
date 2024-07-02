import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(particle_type="electron", case="1"):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # adding the axis labels

    # universal const
    e = -1.602 * 10**-19

    # particle dictionaries
    pd = {
        "proton": {"m": 1.67 * 10**-27, "Q": e, "c": "r", "view": 9**9},
        "electron": {"m": 9.11 * 10**-31, "Q": -e, "c": "b", "view": 1},
    }
    fpt = {
        "1": " moving under only the magnetic field",
        "2": " moving under the magnetic and electric field",
        "3": 1,
        "4": 1,
    }
    # variable for drawing
    xs = []
    ys = []
    zs = []

    # time counter
    n = count()

    # simulations variable
    bo = 1

    # particle
    class Particle:
        def __init__(self, p_type):
            self.Q = p_type["Q"]
            self.m = p_type["m"]
            self.pos = np.array([0, 0, 0])
            self.c = p_type["c"]
            self.view_scaler = p_type["view"]

    p = Particle(pd[particle_type])

    # omega_c
    omega_c = p.Q * bo / p.m

    def title():
        title_ = particle_type + "" + fpt[case]
        return title_

    def animate_particle(t):  # main animation loop
        log.info([next(n), "iteration"])  # log number of times the loop happens
        t = t / p.view_scaler  # makes it look god for proton
        log.info(p.view_scaler)

        # particle movement and position calculations
        u = np.cos(omega_c * t)
        v = np.sin(omega_c * t)
        w = np.cos(omega_c * t)

        select = {
            "1": {
                "x": u,
                "z": 1,
                "c": 0,
            },
            "2": {
                "x": u,
                "z": t,
                "c": 0,
            },
            "3": {"x": u, "z": 1, "c": 0},
            "4": {"x": u, "z": 1, "c": 0},
        }
        case_ = select[case]
        x_ = case_["x"]
        z_ = case_["z"]
        c = case_["c"]

        x = x_ + c
        y = v + c
        z = bo * z_ + w * c

        # append x y, z values
        xs.append(x)
        ys.append(y)
        zs.append(z)

        # plot the graph
        plt.cla()
        ax.set_title(title())
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        plt.plot(xs, ys, zs, alpha=0.4, c=p.c)
        plt.plot(x, y, z, marker="o", c=p.c)

    def on_close_event(event):  # close function
        print(event)
        quit()

    # animation function
    anim = FuncAnimation(plt.gcf(), animate_particle, frames=500, repeat=False)
    fig.canvas.mpl_connect("close_event", on_close_event)

    # print graphic
    plt.show()
