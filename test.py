from pyjvm.Machine import Machine

m = Machine()
m.load_class_file('example/Hello.class')
m.load_class_file('example/TestImport.class')
m.dump()

result = m.call_function('com/gkbrk/JVMTest/Hello/addNumbers', 4, 5)
print(result)