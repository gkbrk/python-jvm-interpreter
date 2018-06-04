from .ClassFile import ClassFile
from .CodeAttr import CodeAttr
import struct
import io
from enum import Enum

class Inst(Enum):
    ICONST_4 = 0x07
    ICONST_5 = 0x08
    IRET     = 0xAC

class Machine:
    def __init__(self):
        self.class_files = {}
        self.stack       = []

    def load_class_file(self, path):
        c = ClassFile().from_file(path)
        self.class_files[c.class_name] = c

    def execute_code(self, code):
        while True:
            inst = Inst(code.read(1)[0])
            print(inst)

            if inst == Inst.ICONST_4:
                self.stack.append(4)
            elif inst == Inst.ICONST_5:
                self.stack.append(5)
            elif inst == Inst.IRET:
                return self.stack.pop()

    def call_function(self, methodName, *args):
        cname = '/'.join(methodName.split('/')[:-1])
        mname = methodName.split('/')[-1]

        for cn in self.class_files:
            cf = self.class_files[cn]
            for m in cf.methods:
                if m.name == mname:
                    print(vars(m))
                    code = m.find_attr('Code').info
                    code = CodeAttr().from_reader(io.BytesIO(code)).code
                    return self.execute_code(io.BytesIO(code))
        return cname

    def dump(self):
        print('Machine Dump')

        print('Loaded Classes')
        for name in self.class_files:
            print(' ', name)
            c = self.class_files[name]

            for method in c.methods:
                print('   [METHOD]', method.name, '->', method.desc)
                for attr in method.attributes:
                    print('     [ATTR] {} ({} bytes)'.format(attr.name, len(attr.info)))

                    if attr.name == 'Code':
                        code = CodeAttr().from_reader(io.BytesIO(attr.info))
                        print('     ', vars(code))
            print()

            for field in c.fields:
                print('   [FIELD]', field.name, ':', field.desc)
                for attr in field.attributes:
                    print('     [ATTR] {} ({} bytes)'.format(attr.name, len(attr.info)))
                    if attr.name == 'ConstantValue':
                        index = struct.unpack('!H', attr.info)[0]
                        print('      ', c.const_pool[index - 1].string)
            print()

            for attr in c.attributes:
                print('  [ATTR] {} ({} bytes)'.format(attr.name, len(attr.info)))
            print()