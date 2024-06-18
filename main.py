import numpy as np
import matplotlib.pyplot as plt

particle_dic = {
    "electron": {"charge": -1.602 * 10**-19, "mass": 9.11 * 10 * -31},
    "proton": {"charge": 1.602 * 10**-19, "mass": 1.67 * 10**-27},
}

bo = np.array([0, 0, 1])  # the magnitude of the magnetic field.
E = np.array([0, 0, -1])
t = 0


class Particle:
    def __init__(self, p_x, p_y, p_z, p_type):
        self.x = p_x
        self.y = p_y
        self.z = p_z
        self.pos = np.array([self.x, self.y, self.z])
        self.vx = 1
        self.vy = 0
        self.vz = 0
        self.v = np.array([self.vx, self.vy, self.vz])
        self.q = p_type["charge"]
        self.m = p_type["mass"]

    def force_calc(self):
        a = self.q * (E + np.cross(self.v, bo)) / self.m
        self.v = self.v + a

    def particle_motion(self):
        self.pos = self.v + self.pos


# run function
def main():
    ps = [Particle(1, 0, 0, particle_dic["electron"]) for _ in range(1)]
    
    # set up viewer
    plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")


if __name__ == "__main__":
    main()
