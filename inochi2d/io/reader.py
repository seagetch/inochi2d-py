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
        
def _verify(stream, magic):
    trial = stream.read(len(magic)) 
    if trial != magic:
        raise InvalidSectionError("Section unmatch: expect '%s', but found '%s'."%(magic,  trial))

def _read_size(stream):
    data_len = int.from_bytes(stream.read(4), byteorder="big")
    return data_len

def _read_block(stream, data_len = None):
    if data_len is None:
        data_len = _read_size(stream)
    raw_data = stream.read(data_len)
    raw_data = struct.unpack(">%ds"%len(raw_data), raw_data)
    return raw_data[0]

def load_json(stream):
    raise FormatError("Not support JSON format yet.")

def load_inx(stream):
    return load_inp(stream)


def load_inp(stream):
    _verify(stream, MAGIC_BYTES)

    puppet_json = json.loads(_read_block(stream).decode('utf-8'))
    
    _verify(stream, TEX_SECTION)
    slots_len = _read_size(stream)
    slots = []
    for i in range(slots_len):
        texture_len = _read_size(stream)
        texture_type = stream.read(1)
        texture = _read_block(stream, texture_len)
        tex_stream = io.BytesIO(texture)
        img = Image.open(tex_stream)
        slots.append(img)
    
    exts = {}
    try:
        _verify(stream, EXT_SECTION)
        section_len = _read_size(stream)
        for i in range(section_len):
            section_name = _read_block(stream).decode('utf-8')
            payload = _read_block(stream)
            exts[section_name] =payload
    except IOError as e:
        pass
    except InvalidSectionError as e:
        pass
    
    return PuppetData(puppet_json, slots, exts)
        

def load(filename):
    name, ext = os.path.splitext(filename)
    with open(filename, 'rb') as f:
        data = f
        if ext == ".json":
            return load_json(data)
        elif ext == ".inx":
            return load_inx(data)
        elif ext == ".inp":
            return load_inp(data)
        else:
            raise FormatError("Unknown file format '%s'"%ext)
