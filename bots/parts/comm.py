import sys
import asyncio
import time
import io
import os

from collections import deque

import utils.debug

from utils.asyncio_stdio import get_stdin, get_stdout
from utils.context_managers import ContextManagerMixin
from utils.logger import log

from bots.models.frame import Frame
from bots.models.move import Move
from bots.models.external import Location


import logging
logger = logging.getLogger(__name__)

_start_time = time.time()


class EventLoopContext(ContextManagerMixin):
    """
    Needed to stick exit clean up callbacks somewhere...
    """

    _stdout = None
    _stdin = None

    def on_init(self, exit_callbacks=None, *args, **kwargs):
        super(EventLoopContext, self).on_init(*args, **kwargs)
        self.exit_callbacks = exit_callbacks if exit_callbacks is not None else []

    def on_enter(self):
        super(EventLoopContext, self).on_enter()
        self.loop = asyncio.get_event_loop()

    def on_exit(self):
        super(EventLoopContext, self).on_exit()
        self.loop.close()

    def run(self, task):
        exit_callbacks = self.exit_callbacks

        async def _dont_forget_cleanup():
            await task
            for cb in exit_callbacks:
                await cb()

        self.loop.run_until_complete(_dont_forget_cleanup())

    async def get_stdout(self):
        """
        Call this **before** `get_stdin`
        :return:
        :rtype: asyncio.StreamWriter
        """

        if not self._stdout:
            self._stdout = await get_stdout(self.loop, self.exit_callbacks)

        return self._stdout

    async def get_stdin(self):
        """
        Call this **after** `get_stdout`
        :return:
        :rtype: asyncio.StreamReader
        """
        if not self._stdin:
            self._stdin = await get_stdin(self.loop, self.exit_callbacks)

        return self._stdin

    async def send(self, message):

        log("send: '{}'".format(message))
        if isinstance(message, str):
            message = message.encode('utf8')
        stdout = await self.get_stdout()

        stdout.write(message + b'\n')
        await stdout.drain()

    async def readline(self):

        stdin = await self.get_stdin()
        line = await stdin.readline()
        line = line.decode('utf8').rstrip('\n')

        # log("readline: '{}'".format(line))
        return line


class HLTAsyncCommMixin:

    @classmethod
    async def get_init(cls, ctx):
        """
        :param EventLoopContext ctx:
        :return:
        :rtype: dict
        """

        player_id = await ctx.readline()
        log('get_init: player id {}'.format(player_id))

        w, h = cls._deserialize_map_size(await ctx.readline())

        log('get_init: size {} {}'.format(w, h))

        map_str = await ctx.readline()
        # if utils.debug.DEBUG:
        #     with open('production.map', 'wb') as fp:
        #         fp.write(map_str.encode('utf8'))
        production = cls._deserialize_production(map_str, w, h)

        return dict(
            production = production,
            player_id = player_id,
            w = w,
            h = h
        )

    @staticmethod
    def _deserialize_map_size(map_size_str):
        w, h = map_size_str.strip().split(" ")
        return int(w), int(h) # (width, height)

    @staticmethod
    def _deserialize_production(production_str, w, h):
        parts = deque(production_str.strip().split(" "))
        production = {}
        for y in range(1, h+1):
            for x in range(1, w+1):
                production[x,y] = int(parts.popleft())
        return production

    @staticmethod
    def _deserialize_map(map_str, frame_id, w, h, production, player_id):
        """
        :param map_str:
        :param w:
        :param h:
        :param production:
        :return:
        :rtype: GameMap
        """
        parts = deque(map_str.strip().split(" "))

        frame = Frame(frame_id, w, h, production=production, player_id=player_id)

        y = 1
        x = 1
        while y <= h:
            number_of_cells = int(parts.popleft())
            owner = parts.popleft()

            for _ in range(0, number_of_cells):
                frame.ownership[x,y] = owner
                if owner == player_id:
                    frame.moves.add(
                        Move((x,y))
                    )
                x += 1
                if x > w:
                    x = 1
                    y += 1

        for y in range(1, h+1):
            for x in range(1, w+1):
                frame.strength[x,y] = int(parts.popleft())

        return frame

    async def send_init(self, name, ctx):
        await ctx.send(name)

    @classmethod
    async def get_frame(cls, frame_id, w, h, production, player_id, ctx):
        """
        :type ctx: EventLoopContext
        :return:
        :rtype: GameMap
        """
        map_str = await ctx.readline()

        # if utils.debug.DEBUG:
        #     with open('frame_{}.map'.format(frame_id), 'wb') as fp:
        #         fp.write(map_str.encode('utf8'))

        return cls._deserialize_map(
            map_str,
            frame_id,
            w,
            h,
            production,
            player_id
        )

    @staticmethod
    def _serialize_move_set(moves):
        return ' '.join([move.serialize() for move in moves])

    @classmethod
    async def send_moves(cls, moves, ctx):
        """
        :type ctx: EventLoopContext
        """
        await ctx.send(
            cls._serialize_move_set(moves)
        )
