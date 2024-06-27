import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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


def magnetic_field(x, y, z):
    alpha = 1
    b0 = 1
    B = np.array(b0 * [alpha * z, 0, 1 + alpha * x])
    return B


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def mag(vector):
    return np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


class Particle:

    def __init__(self, p_type):
        # particle scaler s
        self.charge = p_type["Q"]
        self.mass = p_type["m"]

        # view only
        self.c = p_type["c"]
        self.alpha = np.random.uniform(0.6, 0.9)
        self.view_scaler = p_type["view"]

        # particle previous positions

        # particle vectors
        self.start_position = np.array([1, 1, 0])
        self.start_velocity = np.array([3, 3, 0])

        self.xs = [self.start_position[0]]
        self.ys = [self.start_position[1]]
        self.zs = [self.start_position[2]]

        self.theta_not = np.arctan(self.start_velocity[0] / self.start_velocity[1])
        self.x_ = self.xs[len(self.xs) - 1]
        self.y_ = self.ys[len(self.xs) - 1]
        self.z_ = self.zs[len(self.xs) - 1]
        self.speed = p_type["speed"] * mag(magnetic_field(self.x_, self.y_, self.z_))
        self.omega_c = (
            -self.charge * mag(magnetic_field(self.x_, self.y_, self.z_)) / self.mass
        )

        self.theta_not = np.arctan(self.start_velocity[0] / self.start_velocity[1])

        self.x_not = self.start_position[0] + (self.speed / self.omega_c) * np.sin(
            self.theta_not
        )
        self.y_not = self.start_position[1] - (self.speed / self.omega_c) * np.cos(
            self.theta_not
        )

    # noinspection PyUnresolvedReferences

    def draw(self, x, y, z):
        self.xs.append(x)
        self.ys.append(y)
        self.zs.append(z)
        # plot the points
        plt.plot(self.xs, self.ys, self.zs, c=self.c, alpha=(self.alpha - 0.4))
        plt.plot(x, y, z, c=self.c, alpha=self.alpha, marker=".")

    def x(self, t):
        return (
            -self.speed * np.cos(self.omega_c * t + self.theta_not) / self.omega_c
            + self.x_not
        )

    def y(self, t):
        return (self.speed / self.omega_c) * np.sin(
            self.omega_c * t + self.theta_not
        ) + self.y_not

    def z(self, t):
        return self.start_velocity[2] * t

    def xyz(self, t):
        x = self.x(t)
        y = self.y(t)
        z = self.z(t)
        return x, y, z


def main():
    fig = plt.figure()
    # noinspection PyUnusedLocal
    ax = fig.add_subplot(projection="3d")

    # counter
    n = count()
    nn = count()

    # particle

    p = Particle(pd["electron"])

    def animate_particle(t):
        timestep = 10**-12
        t = t * timestep
        x, y, z = p.xyz(t)
        plt.cla()
        p.draw(x, y, z)

    def on_close_event(event):  # close function
        quit()

    # animation function
    # noinspection PyUnusedLocal,PyTypeChecker
    anim = FuncAnimation(plt.gcf(), animate_particle, repeat=False)
    fig.canvas.mpl_connect("close_event", on_close_event)

    # print graphic
    plt.show()


if __name__ == "__main__":
    main()
