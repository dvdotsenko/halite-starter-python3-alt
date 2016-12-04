from bots.parts.base import BaseBot
from .random_bot import RandomBot
from .overkill_bot import OverkillBot

registry = {
    'default': OverkillBot,
    'overkill': OverkillBot,
    'random': RandomBot
} # type: dict[str, BaseBot]
