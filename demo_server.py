import asyncio
import logging
import math
import time
from typing import AsyncIterable, Iterable
import pyxart_pb2_grpc
import pyxart_servicer

import grpc

async def serve() -> None:
    server = grpc.aio.server()
    pyxart_pb2_grpc.add_PyxartServicer_to_server(
        pyxart_servicer.PyxartServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())