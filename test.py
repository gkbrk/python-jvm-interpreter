#!/usr/bin/env python3
from pyjvm.Machine import Machine
from pyjvm.jstdlib.StdlibLoader import load_stdlib_classes

TEST = "monteCarloPi"
RUNS = 10

tests = {
    "iterativeFibonacci": (
        "example/IntegerTest.class",
        "jvmtest/IntegerTest/iterativeFibonacci",
        100,
    ),
    "monteCarloPi": ("example/Hello.class", "com/gkbrk/JVMTest/Hello/monteCarloPi", 5000),
}

m = Machine()

# Load stdlib
load_stdlib_classes(m)

# Load local classes
class_name, func, args = tests[TEST]
m.load_class_file(class_name)

# Dump machine state
# m.dump()

for i in range(RUNS):
    print(m.call_function(func, args))
