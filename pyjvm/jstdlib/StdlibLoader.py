from .JavaClass import JavaClass
from .PrintStream import PrintStream
from .StringBuilder import StringBuilder
from .Rng import Rng
from .System import System
from .String import String
from .Math import Math

libs = [
  JavaClass(),
  PrintStream(),
  StringBuilder(),
  System(),
  Rng(),
  String(),
  Math()
]

def load_stdlib_classes(machine):
    for lib in libs:
        name = lib.name()
        machine.class_files[name] = lib