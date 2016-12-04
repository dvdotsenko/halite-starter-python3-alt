from . import external as _external
from .vector_transform import VectorTransform


class Move:

    def __init__(self, cell, vector=VectorTransform.STAY):
        """
        :param tuple[int, int] cell:
        :param tuple[int, int] vector:
        """
        self.cell = cell
        self.vector = vector

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.cell)

    def serialize(self):
        # Note that location is used as 1x1 based internally
        # but is communicated to server as 0x0 based
        return str(self.cell[0] - 1) + " " + \
               str(self.cell[1] - 1) + " " + \
               str(VectorTransform.to_move_enum(self.vector))

    def __repr__(self):
        return '<{class_name} {cell} {vector}>'.format(
            class_name = self.__class__.__name__,
            cell = self.cell,
            vector = self.vector
        )
