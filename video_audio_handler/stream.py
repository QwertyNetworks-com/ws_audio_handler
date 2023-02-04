import io
import numpy as np


class WriteStream:
    def __init__(self, stream):

        new_file = open("./files/test", "ab")
        new_file.write(stream)


class WriteChunkLength:
    def __init__(self, chunk_len):
        with open("./files/test.txt", "a+") as text_file:
            text_file.write(str(chunk_len) + "\n")


# class ParseBytes:
#     def __init__(self, stream):
#         mapping = {
#             "0": "auth",
#             "1": "audio",
#             "2": "video",
#             "3": "userid",
#             "4": "room"
#         }
#         stream_data = io.BytesIO(stream).read()
#
#         stream_array = np.array(np.frombuffer(stream_data, dtype=np.uint8))
#         float32_number = stream_array.view(dtype=np.float32)
#
#         self.commands = float32_number
