# import numpy as np
# from matplotlib import pyplot as plt
from functions import *
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# x, y, z axes
x_axes = np.array([1, 0, 0])
y_axes = np.array([0, 1, 0])
z_axes = np.array([0, 0, 1])


class BaseParticle(object):
    def __init__(
        self,
        params,
        start_position_=np.array([1.0, 1.0, 0.0]),
        start_velocity_=unit_vector(np.array([1.0, 0.0, 0.000001])),
    ):
        start_position = start_position_
        start_velocity = start_velocity_

        self.charge = params["Q"]
        self.mass = params["m"]

        self.start_position = start_position
        self.start_velocity = start_velocity
        self.speed = mag(start_velocity_)

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
        self.pitch_angle_0 = self.pitch_angle()
        self.b0 = self.magnetic_field()
        self.bm = 1 / (mag(self.b0) * (np.sin(self.pitch_angle_0)) ** 2)

    def magnetic_field(self):
        # v = -2x^2
        x, y, z = self.position
        u = 1
        v = 0
        # w = -400000 * self.position[2]
        w = 1
        b = 1 + z * 10**15
        rp = np.array([u, v, w])
        return b * rp / mag(rp)

    def pitch_angle(self):
        return np.arccos(mag(self.parallel_velocity()) / mag(self.velocity))

    def update_position(self, magnetic_field=True, delta_s=(1 / 64) * 10**-17):
        if magnetic_field == True:
            magnetic_field = self.magnetic_field()

        self.interation += 1

        # what is the force
        force = self.charge * np.cross(self.velocity, magnetic_field)
        # accel = force/mass
        accel = force / self.mass
        # increment velocity based on accel
        self.velocity += delta_s * accel
        self.velocity = self.speed * unit_vector(self.velocity)
        # increment position based on velocity
        self.position += self.velocity * delta_s
        if self.interation % 100 == 0:
            # print(self.interation)
            super().update()

    def parallel_velocity(self):
        b = self.magnetic_field()
        v = self.velocity
        pav = (np.dot(v, b) / np.dot(b, b)) * b
        return pav


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
        print([v, x, y, z])
        unit_vector(np.cross(x_axes, self.magnetic_field()))
        n1_hat = unit_vector(np.cross(self.magnetic_field(), y_axes))
        b_hat = unit_vector(self.magnetic_field())
        pos = np.array(x * n1_hat + y * n2_hat + z * b_hat)
        self.velocity = np.array(v[0] * n1_hat + v[1] * n2_hat + v[2] * b_hat)
        self.position = pos
        x_, y_, z_ = self.position
        super().update()
        return x_, y_, z_

    def magnetic_field(self):
        print(self)
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
        print(self)
        return np.array([0, 0, 1])
