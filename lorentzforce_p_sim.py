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

    # plot the particle
    ax.cla()
    plt.plot(hx, hy, hz, c=params["c"], alpha=0.3)
    plt.plot(x, y, z, c=params["c"], alpha=1, marker="o")

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
        p.update_position()
        if t % 1 == 0:
            draw_display(ax, p, params)
        scale = 10**-9
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
        frames=10000,
        repeat=False,
        fargs=(fig, ax),
    )
    fig.canvas.mpl_connect("close_event", on_close_event)

    # print graphic
    plt.show()


if __name__ == "__main__":
    main(PosComputeParticle)
