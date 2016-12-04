import os
import asyncio
import asyncio.streams
import sys


async def get_stdout(loop, exit_callbacks):
    """

    :param loop:
    :param exit_callbacks: A list of async callables to run before loop.close()
    :return:
    :rtype: asyncio.StreamWriter
    """

    stdout_fio = os.fdopen(os.dup(sys.stdout.fileno()), 'wb')
    writer_transport, writer_protocol = await loop.connect_write_pipe(
        asyncio.streams.FlowControlMixin,
        stdout_fio
    )

    # async def _close_fio():
    #     stdout_fio.close()
    #
    # exit_callbacks.append(
    #     _close_fio
    # )

    # async def _close_transport():
    #     writer_transport.close()
    #
    # exit_callbacks.append(
    #     _close_transport
    # )

    stdout = asyncio.StreamWriter(writer_transport, writer_protocol, None, loop)
    return stdout


async def get_stdin(loop, exit_callbacks):
    """
    !!!! Super super important !!!!
     Must create stdout ***before*** stdin. Otherwise deadlock.

    :param loop:
    :return:
    :rtype: asyncio.StreamReader
    """

    stdin = asyncio.StreamReader()
    stdin_fio = os.fdopen(os.dup(sys.stdin.fileno()), 'rb')

    reader_protocol = asyncio.StreamReaderProtocol(stdin)
    read_transport, read_protocol = await loop.connect_read_pipe(
        lambda: reader_protocol,
        stdin_fio
    )

    # async def _close_transport():
    #     read_transport.close()
    #
    # exit_callbacks.append(
    #     _close_transport
    # )

    return stdin
