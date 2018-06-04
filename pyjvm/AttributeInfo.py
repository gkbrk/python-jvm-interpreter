import struct

class AttributeInfo:
    def __init__(self):
        pass

    def from_reader(self, r):
        self.name_index = struct.unpack('!H', r.read(2))[0]
        self.length = struct.unpack('!I', r.read(4))[0]

        self.info = r.read(self.length)

        return self