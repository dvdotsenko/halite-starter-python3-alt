from itertools import chain

from .vector_transform import VectorTransform


class _Moves(set):

    def add(self, obj):
        """
        Base class does not replace existing item with same hash value with new one
        We need to do that manually.
        """
        if obj in self:
            self.remove(obj)
        return super(_Moves, self).add(obj)

    def update(self, others):
        '''
        Base class does not replace existing item with same hash value with new one
        We need to do that manually.
        :param others:
        :return:
        '''
        return self.difference_update(others)

class Frame:

    min_x = 1
    min_y = 1
    # max_x is w
    # max_y is h

    _NEUTRAL = {'0', 0}

    def __init__(self, frame_id, w = 0, h = 0, production = None, moves = None, player_id = None):
        """
        :param int w:
        :param int h:
        :param dict production:
        """

        self.player_id = player_id
        self.id = frame_id
        self.w = w
        self.h = h
        self.production = production or dict()
        self.ownership = dict()
        self.strength = dict()
        self.moves = _Moves({move for move in moves or []})

    def shift(self, cell, vector):
        return VectorTransform.shift(cell, vector, self.min_x, self.min_y, self.w, self.h)

    def shift_many(self, cell, *vector):
        return [
            self.shift(cell, vector_transform)
            for vector_transform in vector
        ]

    def get_vector(self, from_cell, to_cell):
        return VectorTransform.get_vector(from_cell, to_cell, self.min_x, self.min_y, self.w, self.h)

    def compute_move_along(self, from_cell, vector):
        """
        :param tuple[int, int] from_cell:
        :param tuple[int, int] vector:
        :return: single step vector along the path described by vector from the cell
        :rtype: tuple[int, int]
        """
        x, y = vector
        if abs(x) >= abs(y):
            return int(x/abs(x)), 0
        else:
            return 0, int(y/abs(y))

    def compute_move_to(self, from_cell, to_cell):
        """
        :param tuple[int, int] from_cell:
        :param tuple[int, int] vector:
        :return: single step vector along the path described by vector from the cell
        :rtype: tuple[int, int]
        """
        return self.compute_move_along(from_cell, self.get_vector(from_cell, to_cell))

    def get_distance(self, from_cell, to_cell):
        x, y = self.get_vector(from_cell, to_cell)
        return abs(x) + abs(y)

    def get_neighbor_cells(self, cell, radius=1):
        vectors = set(VectorTransform.DIRECT)
        if radius > 1:
            for i in range(2, radius+1):
                vectors.update(VectorTransform.radial_dispersion_vectors(i))
        return self.shift_many(cell, *vectors)

    def is_me(self, cell):
        return self.ownership[cell] == self.player_id

    def is_neutral(self, cell):
        return self.ownership[cell] in self._NEUTRAL
