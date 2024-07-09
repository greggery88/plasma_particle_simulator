import logging
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from particles import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# counter
n = count()

# universal constance.
e = -1.602 * 10**-19
k = 8.99 * 10**9


# particle dictionary
pd = {
    "proton": {
        "m": 1.67 * 10**-27,
        "Q": -e,
        "c": "r",
        "view": 10**-9,
        "speed": 9.58 * 10**7,
    },
    "electron": {
        "m": 9.109 * 10**-31,
        "Q": e,
        "c": "b",
        "view": 10**-12,
        "speed": 1.76 * 10**11,
    },
}


def draw_display(ax, p, params):
    x, y, z = p.get_position()
    hx, hy, hz = p.get_history()
    u, v, w = p.magnetic_field()
    l = len(hx) - 1
    # plot the particle
    ax.cla()
    u, v, w = p.parallel_velocity()
    plt.quiver(x, y, z, u, v, w, length=5 * 10**-8)
    u, v, w = p.velocity - p.parallel_velocity()
    plt.quiver(x, y, z, u, v, w, length=5 * 10**-8)
    # ax.quiver(x, y, z, u, v, w)
    plt.plot(hx, hy, hz, c=params["c"], alpha=0.3)
    # plt.plot(hx[l], hy[l], hz[l], c=params["c"], alpha=1, marker="o")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")


def get_pd():
    return pd


def main(model):
    fig = plt.figure()
    # noinspection PyUnusedLocal
    ax = fig.add_subplot(projection="3d")

    # get params
    params = pd["proton"]

    # particle
    p = model(pd["proton"])

    def animate_particle(t, fig, ax):
        log.info(next(n))
        for _ in range(1000000):
            p.update_position()
        print(mag(p.velocity))
        p.pitch_angle()
        draw_display(ax, p, params)
        scale = 5 * 10**-10
        # ax.set_ylim(-3 * scale, 3 * scale)
        # ax.set_xlim(-3 * scale, 3 * scale)
        # ax.set_zlim(-3 * scale, 3 * scale)

    def on_close_event(event):  # close function
        quit()

    # animation function
    # noinspection PyUnusedLocal,PyTypeChecker
    anim = FuncAnimation(
        fig,
        animate_particle,
        frames=100,
        repeat=False,
        fargs=(fig, ax),
    )
    fig.canvas.mpl_connect("close_event", on_close_event)

    # print graphic
    plt.show()


if __name__ == "__main__":
    main(PosComputeParticle)
