from . import external as _external


class VectorTransform:

    # direction = (x, y) shifts
    STAY = (0, 0)
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST = (-1, 0)
    EAST = (1, 0)
    NORTHWEST = (-1, 1)
    NORTHEAST = (1, 1)
    SOUTHWEST = (-1, -1)
    SOUTHEAST = (1, -1)

    DIRECT = {
        NORTH,
        SOUTH,
        WEST,
        EAST
    }

    DIAGONAL = {
        NORTHWEST,
        NORTHEAST,
        SOUTHWEST,
        SOUTHEAST
    }

    ALL = DIRECT | DIAGONAL

    _allowed_moves = DIRECT | {STAY}

    # in HALITE proper 0x0 is in upper left corner
    # in our coordinate system, 1x1 is lower left corner
    # this means up and down are flipped
    _move_enum_map = {
        STAY: _external.STAY,
        NORTH: _external.SOUTH, # flipped
        SOUTH: _external.NORTH, # flipped
        WEST: _external.WEST,
        EAST: _external.EAST
    }

    @classmethod
    def to_move_enum(cls, vector):
        assert vector in cls._allowed_moves
        return cls._move_enum_map[vector]

    @classmethod
    def reverse(cls, vector):
        x, y = vector
        return x * -1, y * -1

    @classmethod
    def shift(cls, cell, vector, min_x, min_y, max_x, max_y):
        """
        :return:
        """
        x, y = cell
        xd, yd = vector
        x += xd
        y += yd

        if x < min_x:
            x += max_x
        elif x > max_x:
            x -= max_x

        if y < min_y:
            y += max_y
        elif y > max_y:
            y -= max_y
        return x, y

    @classmethod
    def get_vector(cls, from_cell, to_cell, min_x, min_y, max_x, max_y):
        """
        derive vectore between two points while utilizing the
        wrapping hature of the map

        :param from_cell:
        :param to_cell:
        :param min_x:
        :param min_y:
        :param max_x:
        :param max_y:
        :return:
        """
        from_x, from_y = from_cell
        to_x, to_y = to_cell
        x = to_x - from_x
        y = to_y - from_y

        x_half = max_x / 2
        y_half = max_y / 2

        if x > x_half:
            x -= max_x
        elif x < x_half * -1:
            x += max_x

        if y > y_half:
            y -= max_y
        elif y < y_half * -1:
            y += max_y

        return x, y

    _radial_dispersion_cache = {}

    @classmethod
    def radial_dispersion_vectors(cls, steps=1):
        if steps not in cls._radial_dispersion_cache:
            vectors = set()
            for i in range(0, steps+1):
                vectors.update([
                    (i, steps-i),
                    (-i, -(steps-i)),
                    (i, -(steps-i)),
                    (-i, steps-i)
                ])
            cls._radial_dispersion_cache[steps] = vectors

        return cls._radial_dispersion_cache[steps]
