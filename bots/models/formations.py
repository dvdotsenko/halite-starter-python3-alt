
class Army(frozenset):

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self | other)
        else:
            return self.__class__(self | {other})

    def __repr__(self):
        return super(Army, self).__repr__()[:-1] + " #{} @{})".format(len(self), self.strength)

    @property
    def strength(self):
        return sum(e.strength for e in self)

class BaseUnit:

    NEUTRAL = 0

    player_id = 0 # type: int
    cell = None # type: tuple[int, int]
    strength = 0 # type: int
    ownership = None # type: str

    def __init__(self, cell, **data):
        self.__dict__.update(data)
        self.cell = cell

    def __hash__(self):
        return hash(self.cell)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __add__(self, other):
        return Army([self]) + other

    def __repr__(self):
        return "<{} {} @{}>".format(self.__class__.__name__, self.cell, self.strength)

    @property
    def is_neutral(self):
        return self.player_id == self.NEUTRAL

    @classmethod
    def get_by_cell(cls, cell, frame, **extra_data):
        return cls(
            cell=cell,
            strength = frame.strength[cell],
            player_id = frame.ownership[cell],
            **extra_data
        )


class Enemy(BaseUnit):

    guard_vectors = None # type: defaultdict[tuple[int,int],set[tuple[int,int]]]


class Battalion(BaseUnit):

    pass
