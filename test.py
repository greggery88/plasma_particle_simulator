import unittest
import numpy as np
import main as ma


class TestMyMath(unittest.TestCase):
    def test_lorentz_law(self):
        p = ma.Particle(0, 0, 0, ma.particle_dic["electron"])

        # starting const
        ma.E = np.array([0, 0, 0])
        ma.bo = np.array([0, 0, 0])
        p.v = np.array([1, 0, 0])

        # operation
        p.force_calc()

        # assert =
        u = p.v[0]
        v = p.v[1]
        w = p.v[2]

        self.assertEqual(u, 1)
        self.assertEqual(v, 0)
        self.assertEqual(w, 0)

    def test_lorentz_law_2(self):
        p = ma.Particle(0, 0, 0, ma.particle_dic["electron"])
        ma.E = np.array([0, 0, 0])
        ma.bo = np.array([0, 0, 1])
        p.v = np.array([1, 0, 0])

        # operation
        p.force_calc()

        # assert =
        u = p.v[0]
        v = p.v[1]
        w = p.v[2]

        self.assertEqual(u, 1)
        self.assertEqual(v, 1.758 * 10**11)
        self.assertEqual(w, 0)


if __name__ == "__main__":
    unittest.main()
