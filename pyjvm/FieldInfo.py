import struct
from .AttributeInfo import AttributeInfo

class FieldInfo:
    def __init__(self):
        pass

    def from_reader(self, r):
        self.access_flags = struct.unpack('!H', r.read(2))[0]
        self.name_index = struct.unpack('!H', r.read(2))[0]
        self.desc_index = struct.unpack('!H', r.read(2))[0]

        self.attr_count = struct.unpack('!H', r.read(2))[0]
        self.attributes = []

        for i in range(self.attr_count):
            a = AttributeInfo().from_reader(r)
            self.attributes.append(a)

        return self

    def find_attr(self, name):
        for a in self.attributes:
            if a.name == name:
                return a