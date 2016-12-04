import unittest

import halitelib.hlt as models


class TestingHLTModels(unittest.TestCase):

    def test_serialize_moves(self):
        m = models.Move(models.Location(2,3), models.WEST)
        self.assertEqual(
            str(m),
            '2 3 {}'.format(models.WEST)
        )

    def test_moves_are_hashable(self):

        m1 = models.Move(models.Location(2,3), models.WEST)
        m2 = models.Move(models.Location(2,3), models.EAST)
        m3 = models.Move(models.Location(3,3), models.WEST)

        moves = set()
        moves.add(m1)
        moves.add(m2) # should collapse into m1
        moves.add(m3)

        self.assertEqual(
            {m2, m3},
            moves
        )


