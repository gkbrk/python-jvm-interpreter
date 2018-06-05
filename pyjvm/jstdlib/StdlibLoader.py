from .JavaClass import JavaClass
from .PrintStream import PrintStream
from .StringBuilder import StringBuilder
from .System import System

libs = [
  JavaClass(),
  PrintStream(),
  StringBuilder(),
  System()
]

def load_stdlib_classes(machine):
    for lib in libs:
        name = lib.name()
        machine.class_files[name] = lib