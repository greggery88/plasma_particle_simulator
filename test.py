import logging
import unittest

import matplotlib.pyplot as plt
import numpy as np

import lorentzforce_p_sim as lfp
from particles import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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


if __name__ == "__main__":
    unittest.main()
