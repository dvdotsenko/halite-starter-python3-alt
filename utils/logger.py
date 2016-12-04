import logging
import logging.handlers
import time

import utils.debug

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


_to_milli = lambda t: int(t*1000)

_start_time = _to_milli(time.time())

_file_added = False


def _add_log_file():
    global _file_added
    if not _file_added:
        log_file = logging.handlers.RotatingFileHandler(
            '{}.log'.format(_start_time)
        )
        logger.addHandler(log_file)
        _file_added = True


def log(message, *args, **kwargs):
    if not utils.debug.DEBUG:
        return

    _add_log_file()

    if args:
        message = message.format(*args)

    if kwargs:
        message = message.format(**kwargs)

    logger.debug(
        '{time_since}: {message}'.format(
            time_since =  _to_milli(time.time()) - _start_time,
            message = message
        )
    )
