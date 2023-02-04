import json
import logging

import time
import pathlib
import ssl
import asyncio
from asyncio.exceptions import TimeoutError

import websockets
from websockets.exceptions import ConnectionClosedOK

from video_audio_handler.stream import WriteStream, WriteChunkLength
from video_audio_handler.utils import ParsePath

# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
ssl_context.load_cert_chain(localhost_pem)


async def consumer_handler(websocket):
    try:
        while True:
            path = websocket.path
            path_data = ParsePath(path=path)
            username = path_data.username
            user_role = path_data.user_status
            speaker = path_data.speaker
            connection_data = dict(username=username, user_role=user_role, speaker=speaker, path=path)
            if user_role == "speaker":
                # if not any(connection_data["username"] == username for c in connections):
                if websocket not in connected_users:
                    connections.append(connection_data)
                message = await websocket.recv()
                for c in connections:
                    if c["username"] == username:
                        c["bytes"] = message
                connected_users.add(websocket)
            elif user_role == "viewer":
                for c in connections:
                    if c["speaker"] == speaker:
                        try:
                            await websocket.send(c["bytes"])
                        except KeyError:
                            pass
    finally:
        connected_users.remove(websocket)
        # Удаляем соединение из словаря с данными по соединениям.
        for i in range(len(connections)):
            if connections[i]["path"] == websocket.path:
                del connections[i]


async def audio_handler1(websocket):
    while True:
        message = await websocket.recv()
        print(message)

        if isinstance(message, bytes) is True:

            WriteChunkLength(chunk_len=len(message))
            WriteStream(stream=message)


async def audio_handler2(websocket):
    while True:
        file = "./files/test"

        chunk_lengths = []
        chunk_len_file = "./files/test.txt"
        with open(chunk_len_file, "r") as text_file:
            text_data = text_file.readlines()
        for t in text_data:
            chunk_lengths.append(int(t.strip()))

        current_bytes = 0
        print(len(chunk_lengths))
        for chunk_len in chunk_lengths:
            offset = current_bytes
            print("Offset: ", offset)
            time.sleep(0.01)
            with open(file, "rb") as f:
                f.seek(offset)
                chunk = f.read(chunk_len)
            # file_read = open(file, "rb")
            # byte = file_read.read(file_read.seek(offset) + chunk_len)
            current_bytes += chunk_len
            print(f"Sent: {chunk_len}B")

            await websocket.send(chunk)


async def video_handler1(websocket):
    await asyncio.gather(consumer_handler(websocket))


async def sock1():
    async with websockets.serve(audio_handler1, "88.198.81.136", 5001, ssl=ssl_context):
        await asyncio.Future()


async def sock2():
    async with websockets.serve(audio_handler2, "88.198.81.136", 5002, ssl=ssl_context):
        await asyncio.Future()


async def sock3():
    async with websockets.serve(video_handler1, "88.198.81.136", 5003, ssl=ssl_context,):
        await asyncio.Future()


async def main():
    await asyncio.gather(sock1(), sock2(), sock3())

if __name__ == "__main__":
    connected_users = set()
    connections = []
    asyncio.run(main())
