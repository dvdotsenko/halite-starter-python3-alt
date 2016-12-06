
class Army(frozenset):

    _strength = None

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self | other)
        else:
            return self.__class__(self | {other})

    def __sub__(self, other):
        if isinstance(other, (self.__class__, set, frozenset)):
            return self.__class__(super(Army, self).__sub__(other))
        else:
            return self.__class__(super(Army, self).__sub__({other}))

    def __repr__(self):
        return super(Army, self).__repr__()[:-1] + " #{} @{})".format(len(self), self.strength)

    @property
    def strength(self):
        if self._strength is None:
            self._strength = sum(e.strength for e in self)
        return self._strength


class BaseUnit:

    NEUTRAL = {0, '0'}

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
        return self.player_id in self.NEUTRAL

    @classmethod
    def get_by_cell(cls, cell, frame, **extra_data):
        return cls(
            cell=cell,
            strength = frame.strength[cell],
            player_id = frame.ownership[cell],
            **extra_data
        )


class Enemy(BaseUnit):

    guard_vectors = None # type: set[tuple[int,int]]
    guard_cells = None # type: set[tuple[int,int]]


class Battalion(BaseUnit):

    pass
