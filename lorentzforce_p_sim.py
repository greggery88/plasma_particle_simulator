import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # universal constance.
    e = -1.602 * 10**-19
    k = 8.99 * 10**9
    c = 3 * 10**8

    # counter
    n = count()
    # fields
    ef = np.array([0, 0, 1])
    bf = np.array([0, 0, 1])

    # particle dictionary
    pd = {
        "proton": {"m": 1.67 * 10**-27, "Q": -e, "c": "r", "view": 1},
        "electron": {"m": 9.11 * 10**-31, "Q": e, "c": "b", "view": 1},
    }

    # calc mag
    def calc_mag(vector):
        n = 0
        for i in range(len(vector)):

            n += vector[i] ** 2
        return np.sqrt(n)

    class Particle:

        def __init__(self, p_type):
            # particle scaler s
            self.q = p_type["Q"]
            self.m = p_type["m"]
            self.c = p_type["c"]
            self.alpha = np.random.uniform(0.6, 0.9)

            # particle previous positions
            self.xs = []
            self.ys = []
            self.zs = []

            # particle vectors
            self.pos = np.random.uniform(-1, 1, size=3)
            self.velo = np.array([0, 0, 0])
            self.accel = np.array([0, 0, 0])

        def calc_pos(self, t, ps, es):
            debye_length = 1
            f_tot = np.zeros(3)
            timestep = 0.00000000001
            # print(np.cross(self.velo, bf))
            f = self.q * (ef + np.cross(self.velo, bf))  # -   self.q * (self.velo / c**2) * (np.dot(self.velo, ef))

            # f = f / lorentz_facter

            f_tot = f_tot + f
            # internal electric fields
            for p in ps:
                if p != self:
                    displacement = p.pos - self.pos
                    distance = np.sqrt(
                        displacement[0] ** 2
                        + displacement[1] ** 2
                        + displacement[2] ** 2
                    )
                    if distance < debye_length:
                        f = -(
                            1
                            / 2
                            * ((k * self.q * p.q) / (distance**2))
                            * displacement
                            / distance
                        )
                        f_tot = f + f_tot
            for p in es:
                if p != self:
                    displacement = p.pos - self.pos
                    distance = np.sqrt(
                        displacement[0] ** 2
                        + displacement[1] ** 2
                        + displacement[2] ** 2
                    )
                    if distance < debye_length:
                        f = -(
                            1
                            / 2
                            * ((k * self.q * p.q) / (distance**2))
                            * displacement
                            / distance
                        )
                        f_tot += f

            # find the posiont from the forces
            self.accel = f_tot / self.m
            self.velo = self.velo + self.accel * timestep
            if calc_mag(self.velo) > 3.0 * 10**8:
                self.velo = 3.0*10**8 * self.velo / calc_mag(self.velo)
            self.pos += self.velo * timestep

            # append position
            self.xs.append(self.pos[0])
            self.ys.append(self.pos[1])
            self.zs.append(self.pos[2])

        def draw(self):
            plt.plot(self.xs, self.ys, self.zs, c=self.c, alpha=(self.alpha - 0.1))
            plt.plot(
                self.pos[0],
                self.pos[1],
                self.pos[2],
                c=self.c,
                alpha=self.alpha,
                marker=".",
            )

    particles_p = [Particle(pd["proton"]) for _ in range(10)]
    particles_e = [Particle(pd["electron"]) for _ in range(10)]

    def animate_particle(t):
        log.info(next(n))
        for particle in particles_p:
            particle.calc_pos(t, particles_p, particles_e)
        for particle in particles_e:
            particle.calc_pos(t, particles_p, particles_e)

        plt.cla()
        for particle in particles_p:
            particle.draw()
        for particle in particles_e:
            particle.draw()

    def on_close_event(event):  # close function
        print(event)
        quit()

    # animation function
    # noinspection PyUnusedLocal,PyTypeChecker
    anim = FuncAnimation(plt.gcf(), animate_particle, repeat=False)
    fig.canvas.mpl_connect("close_event", on_close_event)

    # print graphic
    plt.show()


if __name__ == "__main__":
    main()
