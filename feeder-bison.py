import zmq
import asyncio

from functions import recv_and_process

ctx = zmq.asyncio.Context()

asyncio.run(recv_and_process(ctx, "7658", "bison"))

