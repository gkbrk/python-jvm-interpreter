from pyjvm.Machine import Machine

m = Machine()
m.load_class_file('example/Hello.class')
m.load_class_file('example/TestImport.class')
m.dump()

print(m.call_function('com/gkbrk/JVMTest/Hello/main', []))
print(m.call_function('com/gkbrk/JVMTest/Hello/addOne', 11))
print(m.call_function('com/gkbrk/JVMTest/Hello/subtractNum', 12, 10))