import sys

from halitelib.hlt import *
from halitelib.networking import *

from bots.parts.base import BaseBot

class RandomBot(BaseBot):

    def start(self):
        myID, gameMap = getInit()
        sendInit(self.name)

        while True:
            moves = []
            gameMap = getFrame()
            for y in range(gameMap.height):
                for x in range(gameMap.width):
                    location = Location(x, y)
                    if gameMap.getSite(location).owner == myID:
                        moves.append(Move(location, random.choice(DIRECTIONS)))
            sendFrame(moves)
