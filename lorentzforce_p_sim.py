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
    B = b0 * np.array([alpha * z, y - y, 1 - alpha * x])
    print(B)
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
        self.alpha_view = np.random.uniform(0.6, 0.9)

        # initial conditions
        self.start_position = np.array([10, 1, 0])
        self.start_velocity = np.array([1, 1, 1])

        # previous positions
        self.xs = [self.start_position[0]]
        self.ys = [self.start_position[1]]
        self.zs = [self.start_position[2]]

        # previous position
        self.x_ = self.xs[len(self.xs) - 1]
        self.y_ = self.ys[len(self.xs) - 1]
        self.z_ = self.zs[len(self.xs) - 1]

        # current velocities
        self.velocity = self.start_velocity
        self.perpendicular_v = np.array([self.velocity[0], self.velocity[1], 0])
        self.parallel_v = self.velocity[2]

        # current speed
        self.speed_perpendicular = mag(
            np.array([self.velocity[0], self.velocity[1], 0])
        )

        # variables of motion

        # constants of motion
        self.theta_0 = np.arctan(self.start_velocity[0] / self.start_velocity[1])

        self.y_0 = self.start_position[1] - (
            self.speed_perpendicular / self.omega_c()
        ) * np.cos(self.theta_0)

    # noinspection PyUnresolvedReferences

    def x_0(self):
        x0 = self.start_position[0] + (
            self.speed_perpendicular / self.omega_c()
        ) * np.sin(self.theta_0)
        return x0

    def omega_c(self):
        omega_c = (
            -self.charge * mag(magnetic_field(self.x_, self.y_, self.z_)) / self.mass
        )
        if omega_c == 0:
            omega_c = (
                -self.charge
                * mag(
                    magnetic_field(
                        self.start_position[0],
                        self.start_position[1],
                        self.start_position[2],
                    )
                )
                / self.mass
            )
        return omega_c

    def draw(self, x, y, z):
        self.xs.append(x)
        self.ys.append(y)
        self.zs.append(z)
        # plot the points
        plt.plot(self.xs, self.ys, self.zs, c=self.c, alpha=(self.alpha_view - 0.4))
        plt.plot(x, y, z, c=self.c, alpha=self.alpha_view, marker=".")

    def pitch_angle(self):
        return np.arcsin(mag(self.perpendicular_v / mag(self.velocity)))

    def x(self, t):
        return (
            -self.speed_perpendicular
            * np.cos(self.omega_c() * t + self.theta_0)
            / self.omega_c()
        ) + self.x_0()

    def y(self, t):
        return (self.speed_perpendicular / self.omega_c()) * np.sin(
            self.omega_c() * t + self.theta_0
        ) + self.y_0

    def z(self, t):
        return self.start_velocity[2] * t

    def v(self, t):
        vx = self.speed_perpendicular * np.sin(self.omega_c() * t + self.theta_0)
        vy = self.speed_perpendicular * np.cos(self.omega_c() * t + self.theta_0)
        self.velocity = np.array([vx, vy, self.start_velocity[2]])

    def xyz(self, t):
        n = self.pitch_angle()
        self.v(t)
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

    p = Particle(pd["proton"])

    def animate_particle(t):
        timestep = 10**-5
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
