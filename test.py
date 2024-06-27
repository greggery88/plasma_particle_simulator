import logging
import unittest

import matplotlib.pyplot as plt
import numpy as np

import lorentzforce_p_sim as lfp

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MyTestCase(unittest.TestCase):
    def test_something(self):

        p = lfp.Particle(lfp.pd["electron"])
        p.velocity = np.array([0.5, 1, 0])
        ax, ay, az = lfp.unit_vector(p.external_field())
        for _ in range(10):
            p.calculate_pos_v_a()
            log.info("1")
            v = p.velocity
            a = p.acceleration
            v1_u = lfp.unit_vector(v)
            v2_u = lfp.unit_vector(a)
            rads = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
            deg = rads * 180 / np.pi

            self.assertEqual(deg, 90)

    def test_unit_vector(self):
        v1 = np.array([0, 0, 0])
        v2 = np.array([1, 0, 0])
        v3 = np.array([100, 0, 0])
        v4 = np.array([3, 3, 3])
        # v1
        self.assertEqual(lfp.unit_vector(v1)[0], 0)
        self.assertEqual(lfp.unit_vector(v1)[1], 0)
        self.assertEqual(lfp.unit_vector(v1)[2], 0)
        # v2
        self.assertEqual(lfp.unit_vector(v2)[0], 1)
        self.assertEqual(lfp.unit_vector(v2)[1], 0)
        self.assertEqual(lfp.unit_vector(v2)[2], 0)
        # v3
        self.assertEqual(lfp.unit_vector(v3)[0], 1)
        self.assertEqual(lfp.unit_vector(v3)[1], 0)
        self.assertEqual(lfp.unit_vector(v3)[2], 0)
        # v4
        self.assertEqual(lfp.unit_vector(v4)[0], np.sqrt(3) / 3)
        self.assertEqual(lfp.unit_vector(v4)[1], np.sqrt(3) / 3)
        self.assertEqual(lfp.unit_vector(v4)[2], np.sqrt(3) / 3)

    def test_vector_field(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")  # projection="3d"
        ax.set_xlabel("x")
        x = np.linspace(-1, 1, 4)
        y = np.linspace(-1, 1, 4)
        z = np.linspace(-1, 1, 4)
        x, z, y = np.meshgrid(x, y, z)
        b = lfp.magnetic_field(x, y, z)
        u = b[0]
        v = b[1]
        w = b[2]

        plt.quiver(
            x, y, z, u, v, w, color="b", normalize=True, length=0.5
        )  # , normalize=True, length=20
        # north_pole
        # plt.plot(x, y, marker=".")
        plt.plot(0, 0, 0, color="r", marker="v")
        plt.show()


if __name__ == "__main__":
    unittest.main()
