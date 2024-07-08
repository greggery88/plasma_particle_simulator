import numpy
import numpy as np
from matplotlib import pyplot as plt
from functions import *

# x, y, z axes
x_axes = np.array([1, 0, 0])
y_axes = np.array([0, 1, 0])
z_axes = np.array([0, 0, 1])


class BaseParticle(object):
    def __init__(
        self,
        params,
        start_position_=np.array([0.0, 0.0, 0.0]),
        start_velocity_=np.array([-10.0, 0.0, 0.1]),
    ):
        start_position = start_position_
        start_velocity = start_velocity_

        self.charge = params["Q"]
        self.mass = params["m"]

        self.start_position = start_position
        self.start_velocity = start_velocity

        self.position = start_position
        self.velocity = start_velocity

        self.position_history_x = []
        self.position_history_y = []
        self.position_history_z = []

        self.interation = 0

    def update(self):
        self.position_history_x.append(self.position[0])
        self.position_history_y.append(self.position[1])
        self.position_history_z.append(self.position[2])

    def get_position(self):
        return self.position

    def get_history(self):
        return [
            self.position_history_x,
            self.position_history_y,
            self.position_history_z,
        ]


class PosComputeParticle(BaseParticle):
    def __init__(self, p_type):
        super().__init__(p_type)

    def magnetic_field(self):
        # y = -2x^2
        x = 1
        y = 0
        z = -400000 * self.position[2]
        rp = np.array([x, y, z])
        return 10 * (rp / mag(rp))

    def update_position(self, delta_s=1 / 48 * 10**-11):
        self.interation += 1
        # what is the force
        force = self.charge * np.cross(self.velocity, self.magnetic_field())
        # accel = force/mass
        accel = force / self.mass
        # increment velocity based on accel
        self.velocity += accel * delta_s

        # increment position based on velocity
        self.position += self.velocity * delta_s
        if self.interation % 1000 == 0:
            print(self.interation)
            super().update()

    def axes(self, b):
        n1 = unit_vector(np.cross(np.array([0, 1, 0]), b))
        n2 = unit_vector(np.cross(b, n1))
        b = unit_vector(b)
        return n1, n2, b


class ComputeParticle(BaseParticle):
    def __init__(self, p_type):
        super().__init__(p_type)

    def magnetic_field(self):
        x, y, x = self.position
        return np.array([0.0, 0.0, 10.0])

    def update_position(self, delta_s=10**-10):
        # what is the force
        force = self.charge * np.cross(self.velocity, self.magnetic_field())
        # accel = force/mass
        accel = force / self.mass
        # increment velocity based on accel
        self.velocity += accel * delta_s

        # increment position based on velocity
        self.position += self.velocity * delta_s

        super().update()

    def axes(self, b):
        n1 = unit_vector(np.cross(np.array([0, 1, 0]), b))
        n2 = unit_vector(np.cross(unit_vector(b), np.array([1, 0, 0])))
        b = unit_vector(b)
        return n1, n2, b

    def perpindicular_parallel_velocitys(self):
        perpendicular_velocity = 1
        parallel_velocity = 1
        return perpendicular_velocity, parallel_velocity


class SimpleParticle(BaseParticle):
    def __init__(self, p_type):
        super().__init__(p_type)
        self.position = self.start_position
        # current velocities
        self.velocity = self.start_velocity
        # current speed
        self.speed_perpendicular = mag(self.perpendicular_velocity())
        # constants of motion
        self.theta_0 = np.arctan(self.start_velocity[0] / self.start_velocity[1])

        self.y_0 = self.start_position[1] - (
            self.speed_perpendicular / self.omega_c()
        ) * np.cos(self.theta_0)
        self.x_0 = self.start_position[0] + (
            self.speed_perpendicular / self.omega_c()
        ) * np.sin(self.theta_0)

    def parallel_velocity(self):
        return (
            mag(self.start_velocity) ** 2 - mag(self.perpendicular_velocity()) ** 2
        ) * unit_vector(self.magnetic_field())

    def perpendicular_velocity(self):
        return np.cross(
            self.magnetic_field(),
            self.velocity,
        )

    def omega_c(self):
        return -self.charge * mag(self.magnetic_field()) / self.mass

    def x(self, t):
        return (
            -self.speed_perpendicular
            * np.cos(self.omega_c() * t + self.theta_0)
            / self.omega_c()
        ) + self.x_0

    def y(self, t):
        return (self.speed_perpendicular / self.omega_c()) * np.sin(
            self.omega_c() * t + self.theta_0
        ) + self.y_0

    def z(self, t):
        return self.parallel_velocity() * t

    def update_position(self, t):
        v = self.perpendicular_velocity()
        x = self.x(t)
        y = self.y(t)
        z = self.z(t)
        n2_hat = unit_vector(np.cross(x_axes, self.magnetic_field()))
        n1_hat = unit_vector(np.cross(self.magnetic_field(), y_axes))
        b_hat = unit_vector(self.magnetic_field())
        pos = np.array(x * n1_hat + y * n2_hat + z * b_hat)
        self.velocity = np.array(v[0] * n1_hat + v[1] * n2_hat + v[2] * b_hat)
        self.position = pos
        x, y, z = self.position
        super().update()
        return x, y, z

    def magnetic_field(self):
        return np.array([0, 0, 1])


class SimpleParticleNumerical(BaseParticle):
    def __init__(self, p_type):
        super().__init__(p_type)
        self.position = self.start_position
        # current velocities
        self.velocity = self.start_velocity
        # current speed
        self.speed_perpendicular = mag(self.perpendicular_velocity())
        # constants of motion
        self.theta_0 = np.arctan(self.start_velocity[0] / self.start_velocity[1])

        self.y_0 = self.start_position[1] - (
            self.speed_perpendicular / self.omega_c()
        ) * np.cos(self.theta_0)
        self.x_0 = self.start_position[0] + (
            self.speed_perpendicular / self.omega_c()
        ) * np.sin(self.theta_0)

    def parallel_velocity(self):
        return (
            mag(self.start_velocity) ** 2 - mag(self.perpendicular_velocity()) ** 2
        ) * unit_vector(self.magnetic_field())

    def perpendicular_velocity(self):
        return np.cross(
            self.magnetic_field(),
            self.velocity,
        )

    def omega_c(self):
        return -self.charge * mag(self.magnetic_field()) / self.mass

    def update_position(self, delta_s):
        self.velocity = self.perpendicular_velocity() + self.parallel_velocity()
        self.position += self.velocity * delta_s
        super().update()
        x, y, z = self.position
        return x, y, z

    def magnetic_field(self):
        return np.array([0, 0, 1])
