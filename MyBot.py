import sys
from bots.registry import registry

def start_bot(name='name', bot_type='default', *args):
    Bot = registry[bot_type]
    Bot(name).start(*args)

if __name__ == '__main__':
    start_bot(*sys.argv[1:])
