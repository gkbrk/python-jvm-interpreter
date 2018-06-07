from enum import Enum
import struct

class CPTag(Enum):
    CLASS       = 7
    FIELDREF    = 9
    METHODREF   = 10
    STRING      = 8
    INTEGER     = 3
    DOUBLE      = 6
    NAMEANDTYPE = 12
    UTF8        = 1

class CPInfo:
    def __init__(self):
        self.tag = None

    def from_reader(self, r):
        tag = struct.unpack('!B', r.read(1))[0]
        self.tag = CPTag(tag)

        if self.tag == CPTag.CLASS:
            self.parse_class(r)
        if self.tag == CPTag.METHODREF:
            self.parse_methodref(r)
        elif self.tag == CPTag.FIELDREF:
            self.parse_methodref(r)
        elif self.tag == CPTag.STRING:
            self.parse_string(r)
        elif self.tag == CPTag.INTEGER:
            self.parse_integer(r)
        elif self.tag == CPTag.DOUBLE:
            self.parse_double(r)
        elif self.tag == CPTag.NAMEANDTYPE:
            self.parse_nameandtype(r)
        elif self.tag == CPTag.UTF8:
            self.parse_utf8(r)

        return self

    def parse_class(self, r):
        self.name_index = struct.unpack('!H', r.read(2))[0]

    def parse_methodref(self, r):
        self.class_index = struct.unpack('!H', r.read(2))[0]
        self.name_and_type_index = struct.unpack('!H', r.read(2))[0]

    def parse_string(self, r):
        self.string_index = struct.unpack('!H', r.read(2))[0]

    def parse_integer(self, r):
        self.integer = struct.unpack('!i', r.read(4))[0]

    def parse_double(self, r):
        self.double = struct.unpack('!d', r.read(8))[0]

    def parse_nameandtype(self, r):
        self.name_index = struct.unpack('!H', r.read(2))[0]
        self.desc_index = struct.unpack('!H', r.read(2))[0]

    def parse_utf8(self, r):
        self.length = struct.unpack('!H', r.read(2))[0]
        self.string = struct.unpack('!{}s'.format(self.length), r.read(self.length))[0].decode('utf-8')