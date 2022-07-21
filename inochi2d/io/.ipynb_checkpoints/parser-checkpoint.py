import io
import os
import struct
import json
from PIL import Image

MAGIC_BYTES = b'TRNSRTS\x00'
TEX_SECTION = b"TEX_SECT"
EXT_SECTION = b"EXT_SECT"

class Puppet:
    def __init__(self, puppet_json, textures, exts):
        self.puppet_json = puppet_json
        self.textures    = textures
        self.exts        = exts

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

def _load_json(data):
    raise FormatError("Not support JSON format yet.")

def _load_inx(data):
    return _load_inp(data)


def _load_inp(data):
    _verify(data, MAGIC_BYTES)

    puppet_json = json.loads(_read_block(data).decode('utf-8'))
    
    _verify(data, TEX_SECTION)
    slots_len = _read_size(data)
    slots = []
    for i in range(slots_len):
        texture_len = _read_size(data)
        texture_type = data.read(1)
        texture = _read_block(data, texture_len)
        tex_stream = io.BytesIO(texture)
        img = Image.open(tex_stream)
        slots.append(img)
    
    exts = {}
    try:
        _verify(data, EXT_SECTION)
        section_len = _read_size(data)
        for i in range(section_len):
            section_name = _read_block(data).decode('utf-8')
            payload = _read_block(data)
            exts[section_name] =payload
    except IOError as e:
        pass
    except InvalidSectionError as e:
        pass
    
    return Puppet(puppet_json, slots, exts)
        

def load(filename):
    name, ext = os.path.splitext(filename)
    with open(filename, 'rb') as f:
        data = f
        if ext == ".json":
            return _load_json(data)
        elif ext == ".inx":
            return _load_inx(data)
        elif ext == ".inp":
            return _load_inp(data)
        else:
            raise FormatError("Unknown file format '%s'"%ext)
