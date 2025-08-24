import struct

# 간단한 framing utils: [klen:2][vlen:4][key][value]
HDR_FMT = ">H I"  # klen (unsigned short), vlen (unsigned int)

def pack_record(key: bytes, value: bytes) -> bytes:
    return struct.pack(HDR_FMT, len(key), len(value)) + key + value

def unpack_record(buf: bytes):
    import struct
    klen, vlen = struct.unpack(HDR_FMT, buf[:6])
    key = buf[6:6+klen]
    val = buf[6+klen:6+klen+vlen]
    return key, val