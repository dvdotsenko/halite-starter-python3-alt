import unittest

from collections import defaultdict

from halitelib import networking as external_comm

from ..comm import HLTAsyncCommMixin


class TestingMapParsing(unittest.TestCase):

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

    def _extract_owners_from_map_external(self, mm, axis_start=1):
        return {
            (x,y): str(cell.owner)
            for y, row in enumerate(mm, start=axis_start)
            for x, cell in enumerate(row, start=axis_start)
            if cell.owner
        }

    def _extract_pow_from_map_external(self, mm, axis_start=1):
        return {
            (x,y): cell.strength
            for y, row in enumerate(mm, start=axis_start)
            for x, cell in enumerate(row, start=axis_start)
            if cell.strength
        }

    def _render_grid(self, grid, w, h, filter_fn=None, axis_start=1):

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
            filter_fn = lambda v: str(v) if v else '-'

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

    def _prn(self, n, t = 0):

        w = 30
        h = 30

        with open('frame_{}.map'.format(n)) as fp:
            map_str = fp.read()

        mm = self._parse_map_external(map_str, w, h)
        if t==0:
            dd = self._extract_owners_from_map_external(mm)
        elif t==1:
            dd = self._extract_pow_from_map_external(mm)

        print(self._render_grid(dd, w, h, axis_start=1))

    def _prni(self, n, t = 0):

        w = 30
        h = 30

        with open('frame_{}.map'.format(n)) as fp:
            map_str = fp.read()

        my_id = 1
        mm = self._parse_map_internal(map_str, n, w, h, None, my_id)
        if t==0:
            dd = self._extract_owners_from_map_internal(mm)
        elif t==1:
            dd = self._extract_pow_from_map_internal(mm)

        print(self._render_grid(dd, w, h, axis_start=1))

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

    def _extract_pow_from_map_internal(self, mm):
        return {
            k: v
            for k, v in mm.strength.items()
            if v
        }

    @unittest.skip('This must be manually scaffolded')
    def test_owner_and_power_parsing_parity(self):

        w = 30
        h = 30

        for n in range(1, 301):
            with open('frame_{}.map'.format(n)) as fp:
                map_str = fp.read()

            my_id = 1
            mm_i = self._parse_map_internal(map_str, n, w, h, None, my_id)
            mm_e = self._parse_map_external(map_str, w, h)

            oo_i = self._extract_owners_from_map_internal(mm_i)
            oo_e = self._extract_owners_from_map_external(mm_e)

            pp_i = self._extract_pow_from_map_internal(mm_i)
            pp_e = self._extract_pow_from_map_external(mm_e)

            self.assertEqual(
                oo_i,
                oo_e,
                "oo Frame {}".format(n)
            )

            self.assertEqual(
                pp_i,
                pp_e,
                "pp Frame {}".format(n)
            )


class ProductionParsing(unittest.TestCase):

    def _convert_external_production(self, production, axis_start=1):
        return {
            (x,y): cell
            for y, row in enumerate(production, start=axis_start)
            for x, cell in enumerate(row, start=axis_start)
        }

    def _parse_production_external(self, map_str, w, h):
        external_comm._width = w
        external_comm._height = h
        external_comm._productions = []
        external_comm.deserializeProductions(map_str)

        return self._convert_external_production(external_comm._productions)

    def _parse_production_internal(self, map_str, w, h):
        return HLTAsyncCommMixin._deserialize_production(
            map_str,
            w,
            h
        )

    @unittest.skip('This must be manually scaffolded')
    def test_production_parsing_parity(self):
        with open('production.map') as fp:
            map_str = fp.read()

        w = h = 30

        ppi = self._parse_production_internal(map_str, w, h)
        ppe = self._parse_production_external(map_str, w, h)

        self.assertEqual(
            ppi.keys(),
            ppe.keys()
        )

        self.assertEqual(
            ppi,
            ppe
        )
