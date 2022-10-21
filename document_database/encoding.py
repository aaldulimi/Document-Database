# the encoding/decoding code for all data types will go here. Will need 
# to a more faster json library in the future.

import json



def encode_int(number: int) -> bytes:
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, 'big')
    

def decode_int(number_bytes: bytes) -> int:
    return int.from_bytes(number_bytes, 'big')


def encode_array(arr: list) -> bytes:
    # make sure list is not nested 
    if (any(isinstance(i, list) for i in arr)):
        return None

    arr_str = json.dumps(arr)
    arr_bytes = arr_str.encode("utf-8")

    return arr_bytes


def decode_array(arr: bytes) -> list:
    arr_decoded = arr.decode("utf-8")
    arr = json.loads(arr_decoded)
    
    return arr

  
