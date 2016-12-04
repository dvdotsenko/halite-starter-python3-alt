import unittest

from ..frame import *

class TestingCentroidDetection(unittest.TestCase):

    def test_frame_shift(self):

        f = Frame(0, 4, 4)

        self.assertEqual(
            (4,1),
            f.shift((1,1), VectorTransform.WEST)
        )

        self.assertEqual(
            (4,4),
            f.shift((1,1), VectorTransform.SOUTHWEST)
        )

        self.assertEqual(
            (1,1),
            f.shift((4,1), VectorTransform.EAST)
        )

        self.assertEqual(
            (1,1),
            f.shift((4,4), VectorTransform.NORTHEAST)
        )
