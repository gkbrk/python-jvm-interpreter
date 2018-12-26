from .JavaClass import JavaClass
import random

class Rng(JavaClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'jstdlib/Rng'

    def canHandleMethod(self, name, desc):
        return name in ['generate']

    def handleMethod(self, name, desc, frame, code, machine, ip):
        if name == 'generate':
            frame.stack.append(random.randint(0, 100))
