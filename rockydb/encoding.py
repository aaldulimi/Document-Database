# the encoding/decoding code for all data types will go here. Will need
# to a more faster json library in the future.

import json
import struct
from typing import Union


def encode_this(x: Union[int, float, bool, str, list]) -> bytes:
    if type(x) == int:
        xbytes = encode_int(x)
        return xbytes

    if type(x) == float:
        xbytes = encode_float(x)
        return xbytes

    if type(x) == bool:
        xbytes = encode_bool(x)
        return xbytes

    if type(x) == str:
        xbytes = encode_str(x)
        return xbytes

    if type(x) == list:
        xbytes = encode_array(x)
        return xbytes

    # raise some sort of error if its none of the listed types


def decode_this(
    data_type: Union[int, float, bool, str, list], xbytes: bytes
) -> Union[int, float, bool, str, list]:
    if data_type == int:
        x = decode_int(xbytes)
        return x

    if data_type == float:
        x = decode_float(xbytes)
        return x

    if data_type == bool:
        x = decode_bool(xbytes)
        return x

    if data_type == str:
        x = decode_str(xbytes)
        return x

    if data_type == list:
        x = decode_array(xbytes)
        return x


# int
def encode_int(x: int) -> bytes:
    byte_length = (x.bit_length() + 7) // 8
    return x.to_bytes(byte_length, "big")


def decode_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, "big")


# float
def encode_float(x: float) -> bytes:
    return struct.pack("<d", x)


def decode_float(xbytes: bytes) -> float:
    return struct.unpack("<d", xbytes)[0]


# boolean
def encode_bool(x: bool) -> bytes:
    return struct.pack("?", x)


def decode_bool(xbytes: bytes) -> bool:
    return struct.unpack("?", xbytes)[0]


# str
def encode_str(x: str) -> bytes:
    return bytes(x, "utf-8")


def decode_str(xbytes: bytes) -> str:
    return str(xbytes.decode())


# array
def encode_array(arr: list) -> bytes:
    # make sure list is not nested
    if any(isinstance(i, list) for i in arr):
        return None

    arr_str = json.dumps(arr)
    arr_bytes = arr_str.encode("utf-8")

    return arr_bytes


def decode_array(arr: bytes) -> list:
    arr_decoded = arr.decode("utf-8")
    arr = json.loads(arr_decoded)

    return arr
