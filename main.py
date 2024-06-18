import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import mpl_toolkits.mplot3d.axes3d as p3

particle_dic = {
    "electron": {"charge": -1.602 * 10**-19, "mass": 9.11 * 10**-31, "color": "b"},
    "proton": {"charge": 1.602 * 10**-19, "mass": 1.67 * 10**-27, "color": "r"},
}

bo = np.array([0, 0, 10**-9])  # the magnitude of the magnetic field.
E = np.array([0, 0, 0])
t = np.linspace(0, 100, 100)
x_values = []
y_values = []
z_values = []


class Particle:
    def __init__(self, p_x, p_y, p_z, p_type):
        self.x = p_x
        self.y = p_y
        self.z = p_z
        self.pos = np.array([self.x, self.y, self.z])
        self.v = np.array([1, 0, 0])
        self.q = p_type["charge"]
        self.m = p_type["mass"]
        self.color = p_type["color"]

    def force_calc(self):
        F = self.q * (E + np.cross(self.v, bo))
        a = F / self.m
        self.v = a

    def particle_motion(self):
        self.pos = self.v + self.pos
        print("hi")


def animate_values(t_max, p):
    x_values.append(p.x)
    y_values.append(p.y)
    z_values.append(p.z)
    for _ in t_max:
        p.force_calc()
        p.particle_motion()
        print(p.x)
        x_values.append(p.x)
        y_values.append(p.y)
        z_values.append(p.z)


# run function
def main():
    # set up plots
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    # set up particles
    p = Particle(1, 0, 0, particle_dic["electron"])
    animate_values(t, p)
    print(x_values)
    print(y_values)
    print(z_values)
    scat = ax.scatter(p.x, p.y, p.z, marker="v", c=p.color)

    # set up viewer
    plt.show()


if __name__ == "__main__":
    main()
