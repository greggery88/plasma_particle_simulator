import logging
import random
import unittest

import matplotlib.pyplot as plt
import numpy as np

import lorentzforce_p_sim as lfp
from particles import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

fig = plt.figure().add_subplot(projection="3d")
p = ComputeParticle(lfp.get_pd()["electron"])


class MyTestCase(unittest.TestCase):
    def test_what_did_i_break(self):

        p = PosComputeParticle(lfp.pd["electron"])
        gyro_center = (
            p.mass
            * mag(p.velocity)
            / (abs(p.charge) * mag(p.magnetic_field()))
            * unit_vector(np.cross(p.velocity, p.magnetic_field()))
        )

        for _ in range(10000):
            p.update_position()
        rc = (
            p.mass
            * mag(p.velocity)
            / (abs(p.charge) * mag(p.magnetic_field()))
            * unit_vector(np.cross(p.velocity, p.magnetic_field()))
        )
        self.assertAlmostEqual(mag(gyro_center), mag(p.get_position() + rc), 14)
        self.assertAlmostEqual(mag(gyro_center), mag(rc), 14)

    def test_rc(self):
        p = PosComputeParticle(lfp.get_pd()["electron"])
        for _ in range(1):
            p.update_position()
        rc = p.rc()
        self.assertAlmostEqual(mag(p.rc()), 0, 14)
        self.assertEqual(mag(p.rc()), 0)

    def test_axes(self):

        n1, n2, b = p.axes(np.array([0, 0, 1]))
        n1x, n1y, n1z = n1
        n2x, n2y, n2z = n2
        bx, by, bz = b
        self.assertEqual(n1x, 1)
        self.assertEqual(n1y, 0)
        self.assertEqual(n1z, 0)
        self.assertEqual(n2x, 0)
        self.assertEqual(n2y, 1)
        self.assertEqual(n2z, 0)
        self.assertEqual(bx, 0)
        self.assertEqual(by, 0)
        self.assertEqual(bz, 1)
        n1, n2, b = p.axes(np.array([0, 0, 10]))
        n1x, n1y, n1z = n1
        n2x, n2y, n2z = n2
        bx, by, bz = b
        self.assertEqual(n1x, 1)
        self.assertEqual(n1y, 0)
        self.assertEqual(n1z, 0)
        self.assertEqual(n2x, 0)
        self.assertEqual(n2y, 1)
        self.assertEqual(n2z, 0)
        self.assertEqual(bx, 0)
        self.assertEqual(by, 0)
        self.assertEqual(bz, 1)
        n1, n2, b = p.axes(np.array([1, 0, 10]))
        n1x, n1y, n1z = n1
        n2x, n2y, n2z = n2
        bx, by, bz = b

        fig.quiver(0, 0, 0, n1x, n1y, n1z, color="lime")
        fig.quiver(0, 0, 0, n2x, n2y, n2z, color="b")
        fig.quiver(0, 0, 0, bx, by, bz, color="r")

        b_ = np.random.uniform(-1, 1, 3)
        b = np.array([1, 0, 1])
        n1, n2, b = p.axes(b)

        self.assertEqual(np.dot(n1, b), 0)
        self.assertEqual(np.dot(n2, b), 0)
        self.assertEqual(np.dot(n1, n2), 0)
        plt.show()

    def test_perpendicular_and_parallel_velocitys(self):
        b_ = np.array([1, 0, 0])
        n1, n2, b = p.axes(b_)
        v = np.array([1, 1, 0])
        pev = np.cross(n2, b)
        pav = np.cross(v, n2)
        fig.quiver(0, 0, 0, b[0], b[1], b[2], color="red")
        fig.quiver(0, 0, 0, v[0], v[1], v[2], color="green")
        # fig.quiver(0, 0, 0, n1[0], n1[1], n1[2], color="k")
        fig.quiver(0, 0, 0, n2[0], n2[1], n2[2], color="silver")

        fig.quiver(0, 0, 0, -pev[1], pev[0], pev[2], color="pink")
        fig.quiver(pev[0], pev[1], pev[2], pav[0], pav[1], pav[2], color="brown")

        n = np.cross([0, -10, 1], [0, 0, -1])
        fig.set_xlim(-2, 2)
        fig.set_ylim(-2, 2)
        fig.set_zlim(-2, 2)
        plt.show()


if __name__ == "__main__":
    unittest.main()
