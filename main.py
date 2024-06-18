import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

particle_dic = {
    "electron": {"charge": -1.602 * 10**-19, "mass": 9.11 * 10**-31, "color": "b"},
    "proton": {"charge": 1.602 * 10**-19, "mass": 1.67 * 10**-27, "color": "r"},
}

bo = np.array([0, 0, 10**-9])  # the magnitude of the magnetic field.
E = np.array([0, 0, 0])
time = count()
x_values = []
y_values = []
z_values = []


class Particle:
    def __init__(self, p_x, p_y, p_z, p_type):
        self.x = p_x
        self.y = p_y
        self.z = p_z
        self.pos = np.array([p_x, p_y, p_z])
        self.v = np.array([1, 0, 0])
        self.q = p_type["charge"]
        self.m = p_type["mass"]
        self.color = p_type["color"]

    def force_calc(self):
        F = self.q * (E + np.cross(self.v, bo))
        a = F / self.m
        self.v = a
        self.pos = self.v + self.pos


p = Particle(0, 0, 0, particle_dic["electron"])


def animate(i):
    t = next(time)
    print(t)
    # for _ in range(t):
    # p.force_calc()
    x_values.append(p.pos[0] + 1)
    y_values.append(p.pos[1])
    z_values.append(p.pos[2])
    # print([x_values, y_values, z_values])
    plt.scatter(x_values, y_values, z_values)


# run function
def main():
    # set up plots
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # scat = ax.scatter(p.x, p.y, p.z, marker="v", c=p.color)

    anim = FuncAnimation(plt.gcf(), animate, interval=1000)
    # set up viewer
    plt.show()


if __name__ == "__main__":
    main()
