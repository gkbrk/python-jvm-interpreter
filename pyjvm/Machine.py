from .ClassFile import ClassFile
from .CodeAttr import CodeAttr
from .Frame import Frame
from .jstdlib.JavaClass import JavaClass
from .jstdlib.PrintStream import PrintStream
from .jstdlib.StringBuilder import StringBuilder
from .jstdlib.System import System
import struct
import io
from enum import Enum

class Inst(Enum):
    ICONST_M1     = 0x02
    ICONST_0      = 0x03
    ICONST_1      = 0x04
    ICONST_2      = 0x05
    ICONST_3      = 0x06
    ICONST_4      = 0x07
    ICONST_5      = 0x08
    BIPUSH        = 0x10
    LDC           = 0x12
    ILOAD_0       = 0x1A
    ILOAD_1       = 0x1B
    ILOAD_2       = 0x1C
    ILOAD_3       = 0x1D
    ALOAD_0       = 0x2A
    ALOAD_1       = 0x2B
    ISTORE_0      = 0x3B
    ISTORE_1      = 0x3C
    ISTORE_2      = 0x3D
    ISTORE_3      = 0x3E
    ASTORE_0      = 0x4B
    ASTORE_1      = 0x4C
    ASTORE_2      = 0x4D
    ASTORE_3      = 0x4E
    POP           = 0x57
    DUP           = 0x59
    IADD          = 0x60
    IINC          = 0x84
    IF_ICMPGE     = 0xA2
    GOTO          = 0xA7
    IRET          = 0xAC
    RETURN        = 0xB1
    GETSTATIC     = 0xB2
    INVOKEVIRTUAL = 0xB6
    INVOKESPECIAL = 0xB7
    INVOKESTATIC  = 0xB8
    NEW           = 0xBB

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

class Machine:
    def __init__(self):
        self.class_files = {}

        self.class_files['java/lang/Object'] = JavaClass()
        self.class_files['java/io/PrintStream'] = PrintStream()
        self.class_files['java/lang/StringBuilder'] = StringBuilder()
        self.class_files['java/lang/System'] = System()

    def load_class_file(self, path):
        c = ClassFile().from_file(path)
        self.class_files[c.class_name] = c

    def execute_code(self, frame, code):
        ip = 0
        while True:
            inst = Inst(code[ip])
            #print(inst)

            if inst == Inst.ICONST_M1:
                frame.stack.append(-1)
            elif inst == Inst.ICONST_0:
                frame.stack.append(0)
            elif inst == Inst.ICONST_1:
                frame.stack.append(1)
            elif inst == Inst.ICONST_2:
                frame.stack.append(2)
            elif inst == Inst.ICONST_3:
                frame.stack.append(3)
            elif inst == Inst.ICONST_4:
                frame.stack.append(4)
            elif inst == Inst.ICONST_5:
                frame.stack.append(5)
            elif inst == Inst.BIPUSH:
                ip += 1
                byte = code[ip]

                frame.stack.append(byte)
            elif inst == Inst.LDC:
                ip += 1
                index = code[ip]

                frame.stack.append(frame.current_class.const_pool[index - 1].string)
            elif inst == Inst.ILOAD_0:
                frame.stack.append(frame.get_local(0))
            elif inst == Inst.ILOAD_1:
                frame.stack.append(frame.get_local(1))
            elif inst == Inst.ILOAD_2:
                frame.stack.append(frame.get_local(2))
            elif inst == Inst.ILOAD_3:
                frame.stack.append(frame.get_local(3))
            elif inst == Inst.ALOAD_0:
                frame.stack.append(frame.get_local(0))
            elif inst == Inst.ALOAD_1:
                frame.stack.append(frame.get_local(1))
            elif inst == Inst.ISTORE_0:
                val = frame.stack.pop()
                frame.set_local(0, val)
            elif inst == Inst.ISTORE_1:
                val = frame.stack.pop()
                frame.set_local(1, val)
            elif inst == Inst.ISTORE_2:
                val = frame.stack.pop()
                frame.set_local(2, val)
            elif inst == Inst.ISTORE_3:
                val = frame.stack.pop()
                frame.set_local(3, val)
            elif inst == Inst.ASTORE_0:
                obj = frame.stack.pop()
                frame.set_local(0, obj)
            elif inst == Inst.ASTORE_1:
                obj = frame.stack.pop()
                frame.set_local(1, obj)
            elif inst == Inst.POP:
                frame.stack.pop()
            elif inst == Inst.DUP:
                val = frame.stack.pop()
                frame.stack.append(val)
                frame.stack.append(val)
            elif inst == Inst.IADD:
                return frame.stack.pop() + frame.stack.pop()
            elif inst == Inst.IINC:
                ip += 1
                index, const = struct.unpack('!Bb', code[ip:ip+2])
                ip += 1

                #print('iinc', index, const)
                frame.set_local(index, frame.get_local(index) + const)
            elif inst == Inst.IF_ICMPGE:
                v2 = frame.stack.pop()
                v1 = frame.stack.pop()

                ip += 1
                branch = struct.unpack('!h', code[ip:ip+2])[0]
                #print('cmp', branch)

                if v1 >= v2:
                    ip -= 2
                    ip += branch
                else:
                    ip += 1

            elif inst == Inst.GOTO:
                ip += 1
                branch = struct.unpack('!h', code[ip:ip+2])[0]

                ip -= 2
                ip += branch
                #print('goto', branch)
            elif inst == Inst.IRET:
                return frame.stack.pop()
            elif inst == Inst.RETURN:
                return
            elif inst == Inst.GETSTATIC:
                ip += 1
                index = struct.unpack('!H', code[ip:ip+2])[0]
                ip += 1

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(name)
                #print(vars(nat))
                frame.stack.append(PrintStream())
            elif inst == Inst.INVOKEVIRTUAL:
                ip += 1
                index = struct.unpack('!H', code[ip:ip+2])[0]
                ip += 1

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(name)
                #print(vars(nat))

                if name in self.class_files:
                    cl = self.class_files[name]
                    if cl.canHandleMethod(nat.name, nat.desc):
                        cl.handleMethod(nat.name, nat.desc, frame, code, self, ip)
                else:
                    for i in range(argumentCount(nat.desc)):
                        frame.stack.pop()
                    frame.stack.pop()
            elif inst == Inst.INVOKESPECIAL:
                ip += 1
                index = struct.unpack('!H', code[ip:ip+2])[0]
                ip += 1

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(vars(methodRef))
                #print(vars(nat))
                #print(name)

                if name in self.class_files:
                    cl = self.class_files[name]
                    for m in cl.methods:
                        if m.name == nat.name and m.desc == nat.desc:
                            newCode = m.find_attr('Code').info
                            newCode = CodeAttr().from_reader(io.BytesIO(newCode))
                            newFrame = Frame(newCode.max_stack, newCode.max_locals, cl)

                            for i in range(argumentCount(nat.desc)):
                                newFrame.set_local(i, frame.stack.pop())

                            frame.stack.append(self.execute_code(newFrame, newCode.code))
            elif inst == Inst.INVOKESTATIC:
                ip += 1
                method_index = struct.unpack('!H', code[ip:ip+2])[0]
                ip += 1

                methodRef = frame.current_class.const_pool[method_index - 1]
                cname = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(vars(methodRef))
                #print(vars(nat))
                #print(cname)

                cl = self.class_files[cname]
                for m in cl.methods:
                    if m.name == nat.name and m.desc == nat.desc:
                        newCode = m.find_attr('Code').info
                        newCode = CodeAttr().from_reader(io.BytesIO(newCode))
                        newFrame = Frame(newCode.max_stack, newCode.max_locals, cl)

                        for i in range(argumentCount(nat.desc)):
                            newFrame.set_local(i, frame.stack.pop())

                        frame.stack.append(self.execute_code(newFrame, newCode.code))
            elif inst == Inst.NEW:
                ip += 1
                index = struct.unpack('!H', code[ip:ip+2])[0]
                ip += 1

                methodRef = frame.current_class.const_pool[index - 1]

                if methodRef.name in self.class_files:
                    obj = self.class_files[methodRef.name].__class__()
                    frame.stack.append(obj)
                else:
                    frame.stack.append(None)

                #print(vars(methodRef))

            #print(frame.stack, frame.locals)

            ip += 1

    def call_function(self, methodName, *args):
        cname = '/'.join(methodName.split('/')[:-1])
        mname = methodName.split('/')[-1]

        for cn in self.class_files:
            cf = self.class_files[cn]
            for m in cf.methods:
                if m.name == mname:
                    code = m.find_attr('Code').info
                    code = CodeAttr().from_reader(io.BytesIO(code))

                    frame = Frame(code.max_stack, code.max_locals, cf)
                    for i, arg in enumerate(args):
                        frame.set_local(i, arg)
                    return self.execute_code(frame, code.code)

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