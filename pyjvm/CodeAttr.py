import struct

class CodeAttr:
    def __init__(self):
        pass

    def from_reader(self, r):
        self.max_stack = struct.unpack('!H', r.read(2))[0]
        self.max_locals = struct.unpack('!H', r.read(2))[0]
        self.code_len = struct.unpack('!I', r.read(4))[0]
        self.code = r.read(self.code_len)

        return self