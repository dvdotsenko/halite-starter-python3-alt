
class Flag:

    def __init__(self, cell):
        """
        :param cell:
        :param direction:
        """
        self.cell = cell

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.cell)

    def __repr__(self):
        return super(Flag, self).__repr__()[:-1] + " {}>".format(self.cell)
