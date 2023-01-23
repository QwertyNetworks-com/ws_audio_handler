import asyncio

import websockets


async def handler1(websocket):
    while True:
        message = await websocket.recv()
        print("handler1 :", message)


async def handler2(websocket):
    while True:
        message = await websocket.recv()
        print("handler2 :", message)


async def sock1():
    async with websockets.serve(handler1, "localhost", 8001):
        await asyncio.Future()


async def sock2():
    async with websockets.serve(handler2, "localhost", 8002):
        await asyncio.Future()


async def main():
    await asyncio.gather(sock1(), sock2())


if __name__ == "__main__":
    asyncio.run(main())
