# the encoding/decoding code for all data types will go here. Will need 
# to a more faster json library in the future.

import json
import struct



# int
def encode_int(x: int) -> bytes:
    byte_length = (x.bit_length() + 7) // 8
    return x.to_bytes(byte_length, 'big')
    
def decode_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


# float
def encode_float(x: float) -> bytes:
    return struct.pack('<d', x)

def decode_float(xbytes: bytes) -> float:
    return struct.unpack('<d', xbytes)[0]


# boolean
def encode_bool(x: bool) -> bytes:
    return struct.pack('?', x)

def decode_bool(xbytes: bytes) -> bool:
    return struct.unpack('?', xbytes)[0]


# str
def encode_str(x: str) -> bytes:
    return bytes(x, 'utf-8')

def decode_str(xbytes: bytes) -> str:
    return str(xbytes.decode())


# array
def encode_array(arr: list) -> bytes:
    # make sure list is not nested 
    if (any(isinstance(i, list) for i in arr)):
        return None

    arr_str = json.dumps(arr)
    arr_bytes = arr_str.encode('utf-8')

    return arr_bytes


def decode_array(arr: bytes) -> list:
    arr_decoded = arr.decode('utf-8')
    arr = json.loads(arr_decoded)
    
    return arr

