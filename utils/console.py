from collections import defaultdict

from halitelib.networking import networking as external_comm

from bots.parts.comm import HLTAsyncCommMixin


class Parser:

    @classmethod
    def _parse_map_external(self, map_str, w, h):
        external_comm._width = w
        external_comm._height = h
        external_comm._productions = defaultdict(lambda: defaultdict(int))
        return external_comm.deserializeMap(map_str).contents

    @staticmethod
    def _parse_map_internal(map_str, frame_id, w, h, production, player_id):
        return HLTAsyncCommMixin._deserialize_map(
            map_str,
            frame_id,
            w,
            h,
            production,
            player_id
        )

    @classmethod
    def _extract_owners_from_map_external(self, mm, axis_start=1):
        return {
            (x,y): str(cell.owner)
            for y, row in enumerate(mm, start=axis_start)
            for x, cell in enumerate(row, start=axis_start)
            if cell.owner
        }

    @classmethod
    def _extract_pow_from_map_external(self, mm, axis_start=1):
        return {
            (x,y): cell.strength
            for y, row in enumerate(mm, start=axis_start)
            for x, cell in enumerate(row, start=axis_start)
            if cell.strength
        }

    @classmethod
    def _extract_owners_from_map_internal(self, mm):
        """

        :param Frame mm:
        :return:
        """
        return {
            k: v
            for k, v in mm.ownership.items()
            if v not in (None, 0, '0')
        }

    @classmethod
    def _extract_pow_from_map_internal(self, mm):
        return {
            k: v
            for k, v in mm.strength.items()
            if v
        }

    @classmethod
    def parse_owners_and_strength(self, n, w, h, my_id='1', production=None):

        with open('frame_{}.map'.format(n)) as fp:
            map_str = fp.read()

        mm_i = self._parse_map_internal(map_str, n, w, h, production, my_id)
        mm_e = self._parse_map_external(map_str, w, h)

        oo_i = self._extract_owners_from_map_internal(mm_i)
        oo_e = self._extract_owners_from_map_external(mm_e)

        assert oo_i == oo_e

        pp_i = self._extract_pow_from_map_internal(mm_i)
        pp_e = self._extract_pow_from_map_external(mm_e)

        assert pp_i == pp_e

        return mm_i

    @classmethod
    def _convert_external_production(self, production, axis_start=1):
        return {
            (x,y): cell
            for y, row in enumerate(production, start=axis_start)
            for x, cell in enumerate(row, start=axis_start)
        }

    @classmethod
    def _parse_production_external(self, map_str, w, h):
        external_comm._width = w
        external_comm._height = h
        external_comm._productions = []
        external_comm.deserializeProductions(map_str)

        return self._convert_external_production(external_comm._productions)

    @classmethod
    def _parse_production_internal(self, map_str, w, h):
        return HLTAsyncCommMixin._deserialize_production(
            map_str,
            w,
            h
        )

    @classmethod
    def parse_production(self, w, h):
        with open('production.map') as fp:
            map_str = fp.read()

        w = h = 30

        ppi = self._parse_production_internal(map_str, w, h)
        ppe = self._parse_production_external(map_str, w, h)

        assert ppi == ppe

        return ppi

    @classmethod
    def parse_frame(cls, n, w=30, h=30, me_id='1'):
        p = cls.parse_production(w, h)
        return cls.parse_owners_and_strength(n, w, h, me_id, p)


    @classmethod
    def render_grid(self, grid, w, h, filter_fn=None, axis_start=1):

        def _n_yielder(value=1):
            while True:
                yield value
                value += 1
                if value == 10:
                    value = 0

        y_gen = _n_yielder(axis_start)
        x_gen = _n_yielder(axis_start)
        x_coord = ''.join([
            str(x_gen.__next__())
            for _ in range(w)
        ])

        if not filter_fn:
            filter_fn = lambda v: str(v) if v not in {None, 0, '0'} else '-'

        render_grid = [
            [
                filter_fn(grid.get((x,y), None))
                for x in range(axis_start, w+axis_start)
            ]
            for y in range(axis_start, h+axis_start)
        ]

        return '\n'.join(
            ['  ' + x_coord] + \
            [
                '{} '.format(y_gen.__next__())+''.join([
                    b
                    for b in a
                ])
                for a in render_grid
            ] + \
            ['  ' + x_coord]
        )
