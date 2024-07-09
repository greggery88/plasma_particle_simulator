# import logging
# import random
import unittest

# import numpy as np
import matplotlib.pyplot as plt


import lorentzforce_p_sim as lfp
from particles import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

fig = plt.figure()
ax2d = fig.add_subplot()
ax3d = fig.add_subplot(projection="3d")

p = PosComputeParticle(lfp.get_pd()["electron"])


class MyTestCase(unittest.TestCase):
    def test_mirroring(self):
        pitch_ang = p.pitch_angle()

    def test_speed(self):
        p.speed = 1
        for _ in range(100000):
            p.update_position()
        self.assertAlmostEqual(p.speed, 1, 15, "speed constant")
        self.assertAlmostEqual(mag(p.velocity), p.speed, 15, "speed = velocity mag")
        self.assertAlmostEqual(mag(p.velocity), 1, 15, "velocity = 1")

    def test_unctions(self):
        v = np.array([3, 0, 4])
        self.assertEqual(mag(v), 5)
        self.assertEqual(mag(unit_vector(v)), 1)

    # def test_what_did_i_break(self):
    #     b = np.array([0, 0, 1])
    #     gyro_center = (
    #         p.mass
    #         * mag(p.velocity)
    #         / (abs(p.charge) * mag(b))
    #         * unit_vector(np.cross(p.velocity, b))
    #     )
    #
    #     for _ in range(1000):
    #         p.update_position(b)
    #     rc = (
    #         p.mass
    #         * mag(p.velocity)
    #         / (abs(p.charge) * mag(b))
    #         * unit_vector(np.cross(p.velocity, b))
    #     )
    #     self.assertAlmostEqual(mag(gyro_center), mag(p.get_position() + rc), 14)
    #     self.assertAlmostEqual(mag(gyro_center), mag(rc), 14)

    def test_velocity_projections(self):
        parallel = p.parallel_velocity()
        perpendicular = p.velocity - p.parallel_velocity()
        self.assertAlmostEqual(
            np.dot(parallel, perpendicular), 0, 15, "projection 90 deg to 16 decimals"
        )
        np.testing.assert_array_almost_equal(parallel + perpendicular, p.velocity, 16)


#     def test_tangent_vector(self):
#         num = 1000
#         x = np.linspace(-1, 1, num)
#         y = np.linspace
#         z = y**2
#
#         u, w, v = tangent(x, num)
#         ax3d.quiver(x, y, z, u, v, w, length=0.01, color="lime")
#         ax3d.plot(x, y, z)
#         print("finished")
#         plt.show()
#
#
# def tangent(t, num):
#     # y = -2x^2
#     x = t**2
#     y = t**2
#     z = t**2
#     rp = np.array([x, y, z])
#     return rp / mag(rp)


if __name__ == "__main__":
    unittest.main()
