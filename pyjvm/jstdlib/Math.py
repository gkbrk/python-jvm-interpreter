from .JavaClass import JavaClass
import random
import math

class Math(JavaClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'java/lang/Math'

    def canHandleMethod(self, name, desc):
        return name in ['random']

    def handleStatic(self, name, desc, frame):
        super().handleMethod(name, desc, frame)
        if name == 'random':
            return random.random()
        elif name == 'sqrt':
            val = frame.pop()
            return math.sqrt(val)