import asyncio
import logging
import logging.handlers
import sys
import math

from collections import defaultdict, deque

import utils.debug

from utils.logger import log

from .base import BaseBot
from .comm import HLTAsyncCommMixin, EventLoopContext

from bots.models import Army, Battalion, Enemy

TURN_MAX_SECONDS = 0.90
INIT_MAX_SECONDS = 14.5


class StateParams:

    player_id = None # type: int
    production = [] # type: list
    w = 0 # type: int
    h = 0 # type: int


class BaseTimedBot(HLTAsyncCommMixin, BaseBot, StateParams):
    """
    Uses Python3's asyncio functionality for running
    move calculation in a cooperative thread that is watched
    by master thread and is killed if it runs close to 1 minute.
    """

    async def init(self, ctx):
        """
        :type ctx: EventLoopContext
        :return:
        :rtype: GameMap
        """

        log(
            "Starting '{}'".format(self.name)
        )

        self.ctx = ctx
        self.__dict__.update(
            await self.get_init(ctx)
        )

        self.turns_possible = int(10 * math.sqrt(self.w * self.h))

        self.current_frame = -1

    def get_current_frame(self, shift=0):
        return self.frames[self.current_frame + 0]

    async def receive_latest_frame(self, frame_id):
        return await self.get_frame(
            frame_id,
            self.w,
            self.h,
            self.production,
            self.player_id,
            self.ctx
        )

    async def sync_latest_frame(self):
        new_frame_id = self.current_frame + 1
        frame = await self.receive_latest_frame(new_frame_id)
        self.frames = {
            new_frame_id: frame
        }
        self.current_frame = new_frame_id
        log('New Frame: {}'.format(new_frame_id))
        return frame

    async def main_loop(self, ctx, debug=False):

        utils.debug.DEBUG = bool(debug)

        await self.init(ctx)

        frame = await self.sync_latest_frame()

        try:
            await asyncio.wait_for(
                self.calculate_global_objectives(frame),
                INIT_MAX_SECONDS
            )
        except asyncio.TimeoutError:
            log('Calculate Flags: !!!!!!!!!!! timed out !!!!!!!!!!!!')

        # this completes INIT window
        await ctx.send(self.name)
        frame = await self.sync_latest_frame()

        while True:
            try:
                await asyncio.wait_for(
                    self.calculate_moves(frame),
                    TURN_MAX_SECONDS
                )
            except asyncio.TimeoutError:
                log('Calculate Moves: !!!!!!!!!!! timed out !!!!!!!!!!!!')

            await self.send_moves(frame.moves, ctx)
            frame = await self.sync_latest_frame()

    def start(self, debug=False):
        with EventLoopContext() as ctx:
            ctx.run(
                self.main_loop(ctx, debug)
            )

    ######################
    # Public API
    ######################

    async def calculate_moves(self, frame):
        """
        Called after each frame is synced up
        :param Frame frame:

        :return: nothing. operate on Frame instance
        """
        pass

    async def calculate_global_objectives(self, frame):
        """
        Called once during init after frame zero is received
        You have 14 seconds to think about that frame

        :param Frame frame:
        :return: nothing. operate on Frame instance
        """
        # for i in range(20):
        #     await yld(1)
        #     log('Calculate Flags second {}'.format(i))
        pass
