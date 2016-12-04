import unittest

from ..vector_transform import VectorTransform as C

class TestingVectorDerivation(unittest.TestCase):

    def test_get_vector(self):

        min_x = min_y = 1
        max_x = max_y = 10

        c11 = (1,1)
        c33 = (3,3)
        c38 = (3,8)
        c88 = (8,8)
        c91 = (9,1)

        self.assertEqual(
            (2,2),
            C.get_vector(c11, c33, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (-2,-2),
            C.get_vector(c33, c11, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (-3,-3),
            C.get_vector(c11, c88, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (3,3),
            C.get_vector(c88, c11, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (2,-3),
            C.get_vector(c11, c38, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (-2,3),
            C.get_vector(c38, c11, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (-1,-3),
            C.get_vector(c91, c88, min_x, min_y, max_x, max_y)
        )

        self.assertEqual(
            (1, 3),
            C.get_vector(c88, c91, min_x, min_y, max_x, max_y)
        )

    def test_radial_dispersion(self):

        self.assertEqual(
            {
                (0, 3),
                (0, -3),
                (3, 0),
                (-3, 0),
                (1, 2),
                (-1, -2),
                (1, -2),
                (-1, 2),
                (2, 1),
                (-2, -1),
                (2, -1),
                (-2, 1),
            },
            C.radial_dispersion_vectors(3)
        )
