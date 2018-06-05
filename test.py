from pyjvm.Machine import Machine
from pyjvm.jstdlib.StdlibLoader import load_stdlib_classes

m = Machine()

# Load stdlib
load_stdlib_classes(m)

# Load local classes
m.load_class_file('example/Hello.class')
m.load_class_file('example/TestImport.class')

# Dump machine state
m.dump()

print(m.call_function('com/gkbrk/JVMTest/Hello/main', []))
#print(m.call_function('com/gkbrk/JVMTest/Hello/addOne', 11))
#print(m.call_function('com/gkbrk/JVMTest/Hello/subtractNum', 12, 10))