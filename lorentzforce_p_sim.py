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
    "proton": {"m": 1.67 * 10**-27, "Q": -e, "c": "r", "view": 1},
    "electron": {"m": 9.11 * 10**-31, "Q": e, "c": "b", "view": 1},
}


def magnetic_field():
    magnetic_field_ = np.array([0, 0, 0])
    return magnetic_field_


def electric_field():
    electric_field_ = np.array([0, 0, ])
    return electric_field_


def calculate_vector_mag(vector):
    n = 0
    for i in range(len(vector)):

        n += vector[i] ** 2
    return np.sqrt(n)


def main():
    fig = plt.figure()
    # noinspection PyUnusedLocal
    ax = fig.add_subplot(projection="3d")

    # counter
    n = count()
    nn = count()

    # particle
    class Particle:

        def __init__(self, p_type):
            # particle scaler s
            self.charge = p_type["Q"]
            self.mass = p_type["m"]
            self.c = p_type["c"]
            self.alpha = np.random.uniform(0.6, 0.9)

            # particle previous positions
            self.xs = []
            self.ys = []
            self.zs = []

            # particle vectors
            self.position = np.random.uniform(-0.0001, 0.0001, size=3)
            self.velocity = np.array([1, 0, 0])
            self.a = np.array([0, 0, 0])

        # noinspection PyUnresolvedReferences
        def calculate_pos_v_a(self, particles_):
            # set debye length
            debye_length = 5

            # find the force
            # forces

            resultant_force = np.zeros(3)
            # particle particle interactions

            resultant_force += self.particle_interactions(particles_, debye_length)

            # particle external field interactions
            resultant_force += self.external_field()

            # timestep to add detail for the integrate
            # edit to slow down or speed up.
            # speeding up the graph removes detail.
            timestep = 0.000000000001

            # calculates acceleration
            self.a = resultant_force / self.mass

            # calculates velocity
            self.velocity += self.a * timestep

            # calculates position
            self.position = self.position + self.velocity * timestep

            self.xs.append(self.position[0])
            self.ys.append(self.position[1])
            self.zs.append(self.position[2])

        def particle_interactions(self, particles_, debye_length):
            resultant_force = np.zeros(3)
            for p in particles_:
                if p != self:
                    displacement = p.position - self.position
                    distance = np.sqrt(
                        displacement[0] ** 2
                        + displacement[1] ** 2
                        + displacement[2] ** 2
                    )
                    if distance < debye_length:
                        force = -(
                            1
                            / 2
                            * ((k * self.charge * p.charge) / (distance**2))
                            * displacement
                            / distance
                        )
                        resultant_force += force
                        print(resultant_force)
            return resultant_force

        def external_field(self):
            # noinspection PyUnreachableCode
            field_force = self.charge * (
                electric_field() + np.cross(self.velocity, magnetic_field())
            )
            return field_force

        def draw(self):

            # plot the points
            plt.plot(self.xs, self.ys, self.zs, c=self.c, alpha=(self.alpha - 0.4))
            plt.plot(
                self.position[0],
                self.position[1],
                self.position[2],
                c=self.c,
                alpha=self.alpha,
                marker=".",
            )

    particles = [Particle(pd["electron"]) for _ in range(1)]
    # particles.append(Particle(pd["proton"]))

    def animate_particle(t):
        log.info(next(n))
        for particle in particles:
            particle.calculate_pos_v_a(particles)
        if next(nn) % 1 == 0:
            plt.cla()
            for particle in particles:
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
