import io
import os
import struct
import json
from PIL import Image

from .puppet import *

MAGIC_BYTES = b'TRNSRTS\x00'
TEX_SECTION = b"TEX_SECT"
EXT_SECTION = b"EXT_SECT"

class FormatError(Exception):
    def __init__(self, msg):
        self.msg = msg

class InvalidSectionError(FormatError):
    pass
        
def _tag(stream, magic):
    stream.write(magic)

def _write_size(stream, data_len):
    raw_data_len = struct.pack(">i", data_len)
    stream.write(raw_data_len)

def _write_block(stream, raw_data, data_len = None):
    if data_len is None:
        data_len = len(raw_data)
        _write_size(stream, data_len)
    raw_data = struct.pack(">%ds"%len(raw_data), raw_data)
    stream.write(raw_data)

def dump_json(puppet):
    raise FormatError("Not support JSON format yet.")

def dump_inx(puppet):
    return dump_inp(puppet)


def dump_inp(puppet):
    stream = io.BytesIO()
    _tag(stream, MAGIC_BYTES)

    _write_block(stream, json.dumps(puppet.root).encode('utf-8'))
    
    _tag(stream, TEX_SECTION)
    slots = puppet.textures
    _write_size(stream, len(slots))
    for tex in slots:
        img_stream = io.BytesIO()
        tex.save(img_stream, format="TGA") #TBD, convert PIL.Image to png binary.
        img_data = img_stream.getvalue()
        img_len  = len(img_data)
        _write_size(stream, img_len)
        stream.write(b'\1')
        _write_block(stream, img_data, img_len)
    
    if len(puppet.exts) > 0:
        exts = puppet.exts
        _tag(stream, EXT_SECTION)
        _write_size(stream, len(exts))
        for name, data in exts.items():
            _write_block(stream, name.encode('utf-8'))
            _write_block(stream, data)

    return stream.getvalue()

def dump(filename, puppet):
    name, ext = os.path.splitext(filename)
    data = None
    if ext == ".json":
        data = dump_json(puppet)
    elif ext == ".inx":
        data = dump_inx(puppet)
    elif ext == ".inp":
        data = dump_inp(puppet)
    else:
        raise FormatError("Unknown file format '%s'"%ext)
    if data is not None:
        with open(filename, 'wb') as f:
            f.write(data)
