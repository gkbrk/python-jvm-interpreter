from .ClassFile import ClassFile
from .CodeAttr import CodeAttr
from .Frame import Frame

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
    LCONST_0      = 0x09
    LCONST_1      = 0x0A
    DCONST_0      = 0x0E
    DCONST_1      = 0x0F
    BIPUSH        = 0x10
    SIPUSH        = 0x11
    LDC           = 0x12
    LDC2_W        = 0x14
    ILOAD         = 0x15
    LLOAD         = 0x16
    DLOAD         = 0x18
    ILOAD_0       = 0x1A
    ILOAD_1       = 0x1B
    ILOAD_2       = 0x1C
    ILOAD_3       = 0x1D
    LLOAD_0       = 0x1E
    LLOAD_1       = 0x1F
    LLOAD_2       = 0x20
    LLOAD_3       = 0x21
    DLOAD_3       = 0x29
    ALOAD_0       = 0x2A
    ALOAD_1       = 0x2B
    ALOAD_2       = 0x2C
    ALOAD_3       = 0x2D
    IALOAD        = 0x2E
    AALOAD        = 0x32
    ISTORE        = 0x36
    LSTORE        = 0x37
    DSTORE        = 0x39
    ISTORE_0      = 0x3B
    ISTORE_1      = 0x3C
    ISTORE_2      = 0x3D
    ISTORE_3      = 0x3E
    LSTORE_0      = 0x3F
    LSTORE_1      = 0x40
    LSTORE_2      = 0x41
    LSTORE_3      = 0x42
    DSTORE_3      = 0x4A
    ASTORE_0      = 0x4B
    ASTORE_1      = 0x4C
    ASTORE_2      = 0x4D
    ASTORE_3      = 0x4E
    IASTORE       = 0x4F
    AASTORE       = 0x53
    POP           = 0x57
    DUP           = 0x59
    IADD          = 0x60
    LADD          = 0x61
    DADD          = 0x63
    ISUB          = 0x64
    DSUB          = 0x67
    IMUL          = 0x68
    DMUL          = 0x6B
    DDIV          = 0x6F
    IREM          = 0x70
    IINC          = 0x84
    I2D           = 0x87
    I2C           = 0x92
    DCMPG         = 0x98
    IFNE          = 0x9A
    IFLT          = 0x9B
    IFGE          = 0x9C
    IFLE          = 0x9E
    IF_ICMPLT     = 0xA1
    IF_ICMPGE     = 0xA2
    IF_ICMPGT     = 0xA3
    IF_ICMPLE     = 0xA4
    GOTO          = 0xA7
    IRET          = 0xAC
    LRET          = 0xAD
    DRETURN       = 0xAF
    ARETURN       = 0xB0
    RETURN        = 0xB1
    GETSTATIC     = 0xB2
    PUTSTATIC     = 0xB3
    GETFIELD      = 0xB4
    PUTFIELD      = 0xB5
    INVOKEVIRTUAL = 0xB6
    INVOKESPECIAL = 0xB7
    INVOKESTATIC  = 0xB8
    NEW           = 0xBB
    NEWARRAY      = 0xBC
    ANEWARRAY     = 0xBD
    ARRAYLENGTH   = 0xBE

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

def read_unsigned_short(frame):
    val = struct.unpack('!H', frame.code[frame.ip+1:frame.ip+3])[0]
    frame.ip += 2
    return val

def read_signed_short(frame):
    val = struct.unpack('!h', frame.code[frame.ip+1:frame.ip+3])[0]
    frame.ip += 2
    return val

def read_byte(frame):
    frame.ip += 1
    return frame.code[frame.ip]

def read_signed_byte(frame):
    frame.ip += 1
    signed = struct.unpack('!b', frame.code[frame.ip:frame.ip+1])[0]
    return signed

OPCODES = {}

def opcode(inst):
    def inner(fn):
        OPCODES[inst] = fn
        return fn

    return inner

@opcode(Inst.ICONST_M1)
def iconst_m1(frame):
    frame.push(-1)

@opcode(Inst.ICONST_0)
@opcode(Inst.LCONST_0)
def iconst_0(frame):
    frame.push(0)

@opcode(Inst.ICONST_1)
@opcode(Inst.LCONST_1)
def iconst_1(frame):
    frame.push(1)

@opcode(Inst.ICONST_2)
def iconst_2(frame):
    frame.push(2)

@opcode(Inst.ICONST_3)
def iconst_3(frame):
    frame.push(3)

@opcode(Inst.ICONST_4)
def iconst_4(frame):
    frame.push(4)

@opcode(Inst.ICONST_5)
def iconst_5(frame):
    frame.push(5)

@opcode(Inst.DCONST_0)
def dconst_0(frame):
    frame.push(0.0)

@opcode(Inst.DCONST_1)
def dconst_1(frame):
    frame.push(1.0)

@opcode(Inst.BIPUSH)
def bipush(frame):
    val = read_byte(frame)
    frame.push(val)

@opcode(Inst.SIPUSH)
def sipush(frame):
    val = read_signed_short(frame)
    frame.push(val)

@opcode(Inst.LDC)
def ldc(frame):
    index = read_byte(frame)
    const = frame.current_class.const_pool[index - 1]

    if 'integer' in const.__dict__:
        const = const.integer
    else:
        const = const.string

    frame.push(const)

@opcode(Inst.LDC2_W)
def ldc2_w(frame):
    index = read_unsigned_short(frame)
    const = frame.current_class.const_pool[index - 1].double

    frame.push(const)

@opcode(Inst.ILOAD)
@opcode(Inst.LLOAD)
@opcode(Inst.DLOAD)
def iload(frame):
    index = read_byte(frame)
    frame.push(frame.get_local(index))

@opcode(Inst.ILOAD_0)
@opcode(Inst.LLOAD_0)
@opcode(Inst.ALOAD_0)
def iload_0(frame):
    frame.push(frame.get_local(0))

@opcode(Inst.ILOAD_1)
@opcode(Inst.LLOAD_1)
@opcode(Inst.ALOAD_1)
def iload_1(frame):
    frame.push(frame.get_local(1))

@opcode(Inst.ILOAD_2)
@opcode(Inst.LLOAD_2)
@opcode(Inst.ALOAD_2)
def iload_2(frame):
    frame.push(frame.get_local(2))

@opcode(Inst.ALOAD_3)
def aload_3(frame):
    frame.push(frame.get_local(3))

@opcode(Inst.IALOAD)
def iaload(frame):
    index = frame.pop()
    array = frame.pop()
    frame.push(array[index])

@opcode(Inst.ILOAD_3)
@opcode(Inst.LLOAD_3)
@opcode(Inst.DLOAD_3)
def iload_3(frame):
    frame.push(frame.get_local(3))

@opcode(Inst.ISTORE)
@opcode(Inst.LSTORE)
@opcode(Inst.DSTORE)
def istore(frame):
    index = read_byte(frame)
    val = frame.pop()
    frame.set_local(index, val)

@opcode(Inst.LSTORE_0)
def lstore_0(frame):
    val = frame.pop()
    frame.set_local(0, val)

@opcode(Inst.LSTORE_1)
def lstore_1(frame):
    val = frame.pop()
    frame.set_local(1, val)

@opcode(Inst.LSTORE_2)
def lstore_2(frame):
    val = frame.pop()
    frame.set_local(1, val)

@opcode(Inst.LSTORE_3)
@opcode(Inst.DSTORE_3)
def lstore_3(frame):
    val = frame.pop()
    frame.set_local(3, val)

@opcode(Inst.POP)
def pop(frame):
    frame.pop()

@opcode(Inst.DUP)
def dup(frame):
    val = frame.pop()
    frame.push(val)
    frame.push(val)

@opcode(Inst.IADD)
@opcode(Inst.LADD)
@opcode(Inst.DADD)
def iadd(frame):
    frame.push(frame.pop() + frame.pop())

@opcode(Inst.ISUB)
@opcode(Inst.DSUB)
def isub(frame):
    val2 = frame.pop()
    val1 = frame.pop()

    if type(val1) is str and len(val1) == 1:
        val1 = ord(val1)

    if type(val2) is str and len(val2) == 1:
        val2 = ord(val2)

    frame.push(val1 - val2)

@opcode(Inst.IMUL)
@opcode(Inst.DMUL)
def imul(frame):
    val2 = frame.pop()
    val1 = frame.pop()
    frame.push(val2 * val1)

@opcode(Inst.DDIV)
def ddiv(frame):
    val2 = frame.pop()
    val1 = frame.pop()
    frame.push(val1 / val2)

@opcode(Inst.I2D)
def i2d(frame):
    frame.push(float(frame.pop()))

@opcode(Inst.I2C)
def i2c(frame):
    frame.push(chr(frame.pop()))

@opcode(Inst.DCMPG)
def dcmpg(frame):
    val2 = frame.pop()
    val1 = frame.pop()

    if val1 > val2:
        frame.push(1)
    elif val1 == val2:
        frame.push(0)
    else:
        frame.push(-1)

@opcode(Inst.ARRAYLENGTH)
def arraylength(frame):
    array = frame.pop()
    frame.push(len(array))

@opcode(Inst.ANEWARRAY)
def anewarray(frame):
    index = read_unsigned_short(frame)
    ref = frame.current_class.const_pool[index - 1]

    count = frame.pop()
    frame.push(['' for _ in range(count)])

@opcode(Inst.NEWARRAY)
def newarray(frame):
    array_type = read_byte(frame)
    count = frame.pop()

    frame.push([0 for _ in range(count)])

@opcode(Inst.AALOAD)
def aaload(frame):
    index = frame.pop()
    array = frame.pop()

    frame.push(array[index])
    
class Machine:
    def __init__(self):
        self.class_files = {}

    def load_class_file(self, path):
        c = ClassFile().from_file(path)
        self.class_files[c.class_name] = c

    def execute_code(self, frame):
        code = frame.code
        while True:
            inst = Inst(code[frame.ip])
            #print(frame.ip, inst)

            if len(frame.stack) > frame.max_stack + 1:
                print("MAX STACK")
                break

            if inst in OPCODES:
                OPCODES[inst](frame)
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
            elif inst == Inst.ASTORE_2:
                obj = frame.stack.pop()
                frame.set_local(2, obj)
            elif inst == Inst.ASTORE_3:
                obj = frame.stack.pop()
                frame.set_local(3, obj)
            elif inst == Inst.IASTORE or inst == Inst.AASTORE:
                val = frame.stack.pop()
                index = frame.stack.pop()
                array = frame.stack.pop()

                array[index] = val
            elif inst == Inst.IREM:
                v2 = frame.stack.pop()
                v1 = frame.stack.pop()
                frame.stack.append(v1 % v2)
            elif inst == Inst.IINC:
                index = read_byte(frame)
                const = read_signed_byte(frame)

                frame.set_local(index, frame.get_local(index) + const)
            elif inst == Inst.IFNE:
                v1 = frame.stack.pop()

                branch = read_signed_short(frame)

                if v1 != 0:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IFLT:
                v1 = frame.stack.pop()
                branch = read_signed_short(frame)

                if v1 < 0:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IFGE:
                v1 = frame.stack.pop()

                branch = read_signed_short(frame)

                if v1 >= 0:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IFLE:
                v1 = frame.stack.pop()

                branch = read_signed_short(frame)

                if v1 <= 0:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IF_ICMPLT:
                v2 = frame.stack.pop()
                v1 = frame.stack.pop()

                branch = read_signed_short(frame)

                if type(v1) is str and len(v1) == 1:
                    v1 = ord(v1)

                if type(v2) is str and len(v2) == 1:
                    v2 = ord(v2)

                if v1 < v2:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IF_ICMPGE:
                v2 = frame.stack.pop()
                v1 = frame.stack.pop()

                branch = read_signed_short(frame)

                if type(v1) is str and len(v1) == 1:
                    v1 = ord(v1)

                if type(v2) is str and len(v2) == 1:
                    v2 = ord(v2)

                if v1 >= v2:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IF_ICMPGT:
                v2 = frame.stack.pop()
                v1 = frame.stack.pop()

                branch = read_signed_short(frame)

                if type(v1) is str and len(v1) == 1:
                    v1 = ord(v1)

                if type(v2) is str and len(v2) == 1:
                    v2 = ord(v2)

                if v1 > v2:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.IF_ICMPLE:
                v2 = frame.stack.pop()
                v1 = frame.stack.pop()
                branch = read_signed_short(frame)

                if v1 <= v2:
                    frame.ip -= 3
                    frame.ip += branch
            elif inst == Inst.GOTO:
                branch = read_signed_short(frame)

                frame.ip -= 3
                frame.ip += branch
            elif inst == Inst.IRET or inst == Inst.LRET or inst == Inst.ARETURN or inst == Inst.DRETURN:
                return frame.stack.pop()
            elif inst == Inst.RETURN:
                return
            elif inst == Inst.GETSTATIC:
                index = read_unsigned_short(frame)

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                if name in self.class_files:
                    cl = self.class_files[name]
                    if not cl.static_initialized:
                        cl.static_initialized = True
                        cl.handleMethod('<clinit>', '()V', frame)
                    frame.stack.append(cl.get_field(nat.name))

                #print(name)
                #print(vars(nat))
                #frame.stack.append(PrintStream())
            elif inst == Inst.PUTSTATIC:
                index = read_unsigned_short(frame)

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                if name in self.class_files:
                    cl = self.class_files[name]
                    if not cl.static_initialized:
                        cl.static_initialized = True
                        cl.handleMethod('<clinit>', '()V', frame, code, self, ip)
                    cl.set_field(nat.name, frame.stack.pop())
            elif inst == Inst.GETFIELD:
                index = read_unsigned_short(frame)

                ref = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[ref.class_index - 1].name
                natIndex = ref.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(vars(nat))

                obj = frame.stack.pop()
                #print(obj)
                frame.stack.append(obj.get_field(nat.name))
            elif inst == Inst.PUTFIELD:
                index = read_unsigned_short(frame)

                ref = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[ref.class_index - 1].name
                natIndex = ref.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(vars(nat))

                value = frame.stack.pop()
                obj = frame.stack.pop()
                obj.set_field(nat.name, value)
            elif inst == Inst.INVOKEVIRTUAL:
                index = read_unsigned_short(frame)

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(name)
                #print(vars(nat))

                if name in self.class_files:
                    cl = self.class_files[name]
                    if cl.canHandleMethod(nat.name, nat.desc):
                        ret = cl.handleMethod(nat.name, nat.desc, frame)
                        if not nat.desc.endswith('V'):
                            frame.push(ret)
                else:
                    for i in range(argumentCount(nat.desc)):
                        frame.stack.pop()
                    frame.stack.pop()
            elif inst == Inst.INVOKESPECIAL:
                index = read_unsigned_short(frame)

                methodRef = frame.current_class.const_pool[index - 1]
                name = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(vars(methodRef))
                #print(vars(nat))
                #print(name)

                if name in self.class_files:
                    cl = self.class_files[name]
                    if cl.canHandleMethod(nat.name, nat.desc):
                        ret = cl.handleMethod(nat.name, nat.desc, frame)
                    else:
                        frame.stack.pop()
                        
            elif inst == Inst.INVOKESTATIC:
                index = read_unsigned_short(frame)

                methodRef = frame.current_class.const_pool[index - 1]
                cname = frame.current_class.const_pool[methodRef.class_index - 1].name
                natIndex = methodRef.name_and_type_index
                nat = frame.current_class.const_pool[natIndex - 1]

                #print(vars(methodRef))
                #print(vars(nat))
                #print(cname)

                if cname in self.class_files:
                    cl = self.class_files[cname]
                    if cl.canHandleMethod(nat.name, nat.desc):
                        ret = cl.handleStatic(nat.name, nat.desc, frame)
                        if not nat.desc.endswith('V'):
                            frame.push(ret)
            elif inst == Inst.NEW:
                index = read_unsigned_short(frame)
                
                methodRef = frame.current_class.const_pool[index - 1]

                if methodRef.name in self.class_files:
                    obj = self.class_files[methodRef.name].__class__()
                    if self.class_files[methodRef.name].file_path:
                        obj.from_file(self.class_files[methodRef.name].file_path)

                    obj.python_initialize()

                    frame.stack.append(obj)
                else:
                    frame.stack.append(None)

            #print(frame.stack, frame.locals)
            frame.ip += 1

    def call_function(self, methodName, *args):
        cname = '/'.join(methodName.split('/')[:-1])
        mname = methodName.split('/')[-1]

        if cname in self.class_files:
            cf = self.class_files[cname]
            for m in cf.methods:
                if m.name == mname:
                    code = m.find_attr('Code').info
                    code = CodeAttr().from_reader(io.BytesIO(code))

                    frame = Frame(code, cf, self)
                    for i, arg in enumerate(args):
                        frame.set_local(i, arg)
                    return self.execute_code(frame)

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
