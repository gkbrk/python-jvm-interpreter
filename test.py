#!/usr/bin/env python3
from pyjvm.Machine import Machine
from pyjvm.jstdlib.StdlibLoader import load_stdlib_classes

m = Machine()

# Load stdlib
load_stdlib_classes(m)

# Load local classes
m.load_class_file('example/Hello.class')
m.load_class_file('example/TestImport.class')
m.load_class_file('example/IntegerTest.class')
m.load_class_file('example/Rot13.class')
m.load_class_file('example/InstanceTest.class')

# Dump machine state
m.dump()

print(m.call_function('com/gkbrk/JVMTest/Hello/main', []))
print(m.call_function('jvmtest/IntegerTest/doubleNum', 11))
print(m.call_function('jvmtest/InstanceTest/test_single'))
print(m.call_function('jvmtest/Rot13/rot13', 'Test'))