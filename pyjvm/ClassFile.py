import struct
from .CPInfo import CPInfo
from .CodeAttr import CodeAttr
from .Frame import Frame
from .FieldInfo import FieldInfo
from .AttributeInfo import AttributeInfo
from .jstdlib.JavaClass import JavaClass
import io

def argumentCount(desc):
    arg = desc.split(')', 2)[0][1:]
    i = 0

    parsingClass = False
    for c in arg:
        if parsingClass:
            if c == ';':
                parsingClass = False
            continue
        if c == 'L':
            parsingClass = True
        i += 1

    return i

class ClassFile(JavaClass):
    def __init__(self):
        super().__init__()

    def canHandleMethod(self, name, desc):
        if super().canHandleMethod(name, desc):
            return True
        for m in self.methods:
            if m.name == name and m.desc == desc:
                return True

    def handleMethod(self, name, desc, frame):
        super().handleMethod(name, desc, frame)
        for m in self.methods:
            if m.name == name and m.desc == desc:
                newCode = m.find_attr('Code').info
                newCode = CodeAttr().from_reader(io.BytesIO(newCode))
                newFrame = Frame(newCode, self, frame.machine)

                for i in range(argumentCount(desc)):
                    newFrame.set_local(i, frame.stack.pop())

                ret = frame.machine.execute_code(newFrame)
                if not desc.endswith('V'):
                    return ret

    def from_file(self, path):
        self.file_path = path
        with open(path, 'rb') as cf:
            self.magic = struct.unpack('!I', cf.read(4))
            self.minor, self.major = struct.unpack('!HH', cf.read(4))

            const_count = struct.unpack('!H', cf.read(2))[0]
            self.const_pool = []

            for i in range(const_count - 1):
                c = CPInfo().from_reader(cf)
                self.const_pool.append(c)

            self.replace_indexes(self.const_pool)

            self.access_flags = struct.unpack('!H', cf.read(2))[0]

            this_class = struct.unpack('!H', cf.read(2))[0]
            self.class_name = self.const_pool[this_class - 1].name

            super_class = struct.unpack('!H', cf.read(2))[0]
            self.super_class = self.const_pool[super_class - 1].name

            interface_count = struct.unpack('!H', cf.read(2))[0]
            self.interfaces = []

            for i in range(interface_count):
                iface_index = struct.unpack('!H', cf.read(2))[0]
                self.interfaces.append(self.const_pool[iface_index - 1].name)

            field_count = struct.unpack('!H', cf.read(2))[0]
            self.fields = []
            for i in range(field_count):
                f = FieldInfo().from_reader(cf)
                self.replace_indexes(f.attributes)
                self.fields.append(f)

            method_count = struct.unpack('!H', cf.read(2))[0]
            self.methods = []
            for i in range(method_count):
                m = FieldInfo().from_reader(cf)
                self.replace_indexes(m.attributes)
                self.methods.append(m)

            attr_count = struct.unpack('!H', cf.read(2))[0]
            self.attributes = []
            for i in range(attr_count):
                a = AttributeInfo().from_reader(cf)
                self.attributes.append(a)

            self.replace_indexes(self.fields)
            self.replace_indexes(self.methods)
            self.replace_indexes(self.attributes)

            return self

    def replace_indexes(self, array):
        for member in array:
            if 'name_index' in member.__dict__:
                member.name = self.const_pool[member.name_index - 1].string

            if 'desc_index' in member.__dict__:
                member.desc = self.const_pool[member.desc_index - 1].string

            if 'string_index' in member.__dict__:
                member.string = self.const_pool[member.string_index - 1].string