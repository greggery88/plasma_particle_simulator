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
        start_position=np.array([0.0, 0.0, 0.0]),
        start_velocity=np.array([0.0, 0.04, 0.0]),
    ):

        self.charge = params["Q"]
        self.mass = params["m"]

        self.start_position = np.array([0.0, 0.0, 0.0])
        self.start_velocity = np.array([0.0, 0.04, 0.0])

        self.position_ = start_position
        self.velocity = start_velocity

        self.position_history_x = []
        self.position_history_y = []
        self.position_history_z = []

    def update(self):
        self.position_history_x.append(self.position_[0])
        self.position_history_y.append(self.position_[1])
        self.position_history_z.append(self.position_[2])

    def get_position(self):
        return self.position_

    def get_history(self):
        return [
            self.position_history_x,
            self.position_history_y,
            self.position_history_z,
        ]


class PosComputeParticle(BaseParticle):
    def __init__(self, p_type):
        super().__init__(p_type)

    def rc(self):
        gyro_center = (
            self.mass
            * mag(self.start_velocity)
            / (abs(self.charge) * mag(self.magnetic_field()))
            * unit_vector(np.cross(self.start_velocity, self.magnetic_field()))
        )
        rc = (
            self.mass
            * mag(self.velocity)
            / (abs(self.charge) * mag(self.magnetic_field()))
            * unit_vector(np.cross(self.velocity, self.magnetic_field()))
        )
        difference = rc - gyro_center
        return difference

    def magnetic_field(self):
        x, y, x = self.position_
        return np.array([0.0, 0.0, 1.0])

    def update_position(self, delta_s=10**-17):
        # what is the force
        force = self.charge * np.cross(self.velocity, self.magnetic_field())
        # accel = force/mass
        accel = force / self.mass
        # increment velocity based on accel
        self.velocity += accel * delta_s
        # increment position based on velocity
        self.position_ += self.velocity * delta_s - self.rc()

        super().update()


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
        self.position_ = pos
        x, y, z = self.position_
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
