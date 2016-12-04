import unittest

from bots.models import Move
from bots.models import VectorTransform

from ..comm import HLTAsyncCommMixin


class TestingHLTNetworking(unittest.TestCase):

    def test_moves_are_serializable(self):

        m1 = Move((2,3), VectorTransform.WEST)
        m2 = Move((2,2), VectorTransform.EAST)
        m3 = Move((3,3), VectorTransform.WEST)

        # list on purpose to insure order for testing
        moves = [
            m1,
            m2,
            m3
        ]

        mm = HLTAsyncCommMixin._serialize_move_set(moves)

        # note that our locations are 1x1 based and Halite's location is 0x0 based
        self.assertEqual(
            mm,
            '1 2 4 1 1 2 2 2 4'
        )
