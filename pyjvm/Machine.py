from .ClassFile import ClassFile
from .CodeAttr import CodeAttr
from .Frame import Frame
import struct
import io
from enum import Enum

class Inst(Enum):
    ICONST_4 = 0x07
    ICONST_5 = 0x08
    ILOAD_0  = 0x1A
    ILOAD_1  = 0x1B
    ILOAD_2  = 0x1C
    ILOAD_3  = 0x1D
    IADD     = 0x60
    IRET     = 0xAC

class Machine:
    def __init__(self):
        self.class_files = {}

    def load_class_file(self, path):
        c = ClassFile().from_file(path)
        self.class_files[c.class_name] = c

    def execute_code(self, frame, code):
        while True:
            inst = Inst(code.read(1)[0])

            if inst == Inst.ICONST_4:
                frame.stack.append(4)
            elif inst == Inst.ICONST_5:
                frame.stack.append(5)
            elif inst == Inst.ILOAD_0:
                frame.stack.append(frame.get_local(0))
            elif inst == Inst.ILOAD_1:
                frame.stack.append(frame.get_local(1))
            elif inst == Inst.ILOAD_2:
                frame.stack.append(frame.get_local(2))
            elif inst == Inst.ILOAD_3:
                frame.stack.append(frame.get_local(3))
            elif inst == Inst.IADD:
                return frame.stack.pop() + frame.stack.pop()
            elif inst == Inst.IRET:
                return frame.stack.pop()

    def call_function(self, methodName, *args):
        cname = '/'.join(methodName.split('/')[:-1])
        mname = methodName.split('/')[-1]

        for cn in self.class_files:
            cf = self.class_files[cn]
            for m in cf.methods:
                if m.name == mname:
                    code = m.find_attr('Code').info
                    code = CodeAttr().from_reader(io.BytesIO(code))

                    frame = Frame(code.max_stack, code.max_locals)
                    for i, arg in enumerate(args):
                        frame.set_local(i, arg)
                    return self.execute_code(frame, io.BytesIO(code.code))

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